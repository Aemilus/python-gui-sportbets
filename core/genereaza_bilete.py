import itertools
import os
import time
from pathlib import Path
from threading import Thread

from openpyxl import Workbook
from openpyxl.styles import PatternFill


class GenereazaBilete:
    def __init__(self, app):
        self.app = app
        self.thread = None
        self.style1 = PatternFill(start_color="afd9fa", end_color="afd9fa", fill_type="solid")
        self._reset()

    def _reset(self):
        self.bilete = None
        self.cap_tabel = list()
        self.tabel_bilete = list()

    def _genereaza_bilete(self):
        self._reset()
        self.bilete = itertools.product(self.app.core.semne, repeat=self.app.core.nr_meciuri)
        for _ in range(self.app.core.nr_meciuri):
            self.tabel_bilete.append(list())
        varianta = 0
        bilete_valide = 0
        wb = Workbook()
        ws = wb.active
        for bilet in self.bilete:
            varianta += 1
            bilet_valid = True
            for semn_info in self.app.core.semne:
                nr_semne = len([semn_meci for semn_meci in bilet if semn_meci.semn == semn_info.semn])
                if nr_semne < semn_info.minim:
                    bilet_valid = False
                    break
                if nr_semne > semn_info.maxim:
                    bilet_valid = False
                    break
            if bilet_valid:
                bilete_valide += 1
                self.cap_tabel.append(f"Bilet {bilete_valide}")
                self.cap_tabel.append("")
                self.app.main_win.procesare_frame.label_progres_generare.config(text=str(bilete_valide))
                for meci in range(self.app.core.nr_meciuri):
                    self.tabel_bilete[meci].append(bilet[meci].semn)
        ws.append(self.cap_tabel)
        for row in self.tabel_bilete:
            ws.append(row)
        # styling
        culori_semne = dict()
        base_semn_color = int("fafcb1", base=16)
        for ratio, semn in enumerate(self.app.core.semne):
            color_pattern = hex(base_semn_color + ratio * 100000)[2:8]
            culori_semne[semn.semn] = PatternFill(start_color=color_pattern, end_color=color_pattern, fill_type="solid")
        if self.tabel_bilete:
            for row in ws.iter_rows(min_row=1, max_row=1, min_col=1, max_col=len(self.tabel_bilete[0])):
                for cell in row:
                    if cell.value:
                        cell.fill = self.style1
        if self.tabel_bilete:
            for row in ws.iter_rows(
                    min_row=2, max_row=len(self.tabel_bilete) + 1, min_col=1, max_col=len(self.tabel_bilete[0])):
                for cell in row:
                    if cell.value:
                        cell.fill = culori_semne[cell.value]
        # finished
        path_excel = str(Path(os.getcwd()) / "bilete.xlsx")
        wb.save(path_excel)
        self.app.core.excel = path_excel
        time.sleep(2)
        self.app.main_win.procesare_frame.label_progres_generare.config(text=f"Am generat {bilete_valide} bilete")

    def genereaza_bilete(self):
        if not self.thread:
            self.thread = Thread(target=self._genereaza_bilete, name="Thread-genereaza-bilete")
            self.thread.start()
