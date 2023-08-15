import itertools
import os
import time
from pathlib import Path
from threading import Thread

from openpyxl import Workbook
from openpyxl.styles import PatternFill

from core.bilet import Bilet


class GenereazaBilete:
    HEADER_COLOR = PatternFill(start_color="afd9fa", end_color="afd9fa", fill_type="solid")
    NR_BILETE_VALIDE = 0

    def __init__(self, app):
        self.app = app
        self.thread = None
        self.combinatii = None
        self.bilete_valide = None
        self.cap_tabel = None
        self.tabel_bilete = None
        self._reset()

    def _reset(self):
        self.combinatii = None
        self.cap_tabel = list()

    def _init_tabel_bilete(self):
        """
        O lista de liste ce reprezinta un tabel.
        Scopul este ca ulterior:
        - pe primul rand se vor afla meciurile de pe pozitia 1 din toate biletele.
        - pe al doilea rand se vor afla meciurile de pe pozitia 2 din toate biletele.
        s.a.m.d.
        """
        self.tabel_bilete = list()
        for _ in range(self.app.core.nr_meciuri + 1):
            self.tabel_bilete.append(list())

    def genereaza_toate_combinatiile(self):
        self.combinatii = itertools.product(self.app.core.semne, repeat=self.app.core.nr_meciuri)

    def _genereaza_bilete(self):
        self._reset()
        self.genereaza_toate_combinatiile()
        self._init_tabel_bilete()
        wb = Workbook()
        ws = wb.active
        for combinatie in self.combinatii:
            bilet = Bilet(self.app, combinatie)
            if bilet.is_valid():
                self.NR_BILETE_VALIDE += 1
                bilet.nr_bilet = self.NR_BILETE_VALIDE
                self.cap_tabel.append(f"Bilet {bilet.nr_bilet}")
                self.cap_tabel.append("")
                self.app.main_win.procesare_frame.label_progres_generare.config(text=str(self.NR_BILETE_VALIDE))
                for meci in range(self.app.core.nr_meciuri):
                    self.tabel_bilete[meci].append(combinatie[meci].semn)
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
                        cell.fill = self.HEADER_COLOR
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
        self.app.main_win.procesare_frame.label_progres_generare.config(text=f"Am generat {self.NR_BILETE_VALIDE} bilete")

    def genereaza_bilete(self):
        if not self.thread:
            self.thread = Thread(target=self._genereaza_bilete, name="Thread-genereaza-bilete")
            self.thread.start()
