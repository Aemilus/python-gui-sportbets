import itertools
import os
import time
from pathlib import Path
from threading import Thread

from openpyxl import Workbook


class GenereazaBilete:
    def __init__(self, app):
        self.app = app
        self.thread = None
        self._reset()

    def _reset(self):
        self.bilete = None
        self.excel_nr = list()
        self.bilete_excel = list()

    def _genereaza_bilete(self):
        self._reset()
        self.bilete = itertools.product(self.app.semne, repeat=self.app.nr_meciuri)
        for _ in range(self.app.nr_meciuri):
            self.bilete_excel.append(list())
        varianta = 0
        bilete_valide = 0
        wb = Workbook()
        ws = wb.active
        for bilet in self.bilete:
            varianta += 1
            bilet_valid = True
            for semn_info in self.app.semne:
                nr_semne = len([semn_meci for semn_meci in bilet if semn_meci.semn == semn_info.semn])
                if nr_semne < semn_info.minim:
                    bilet_valid = False
                    break
                if nr_semne > semn_info.maxim:
                    bilet_valid = False
                    break
            if bilet_valid:
                bilete_valide += 1
                self.excel_nr.append(bilete_valide)
                self.app.main_win.label_progres_generare.config(text=str(bilete_valide))
                for meci in range(self.app.nr_meciuri):
                    self.bilete_excel[meci].append(bilet[meci].semn)
        ws.append(self.excel_nr)
        for row in self.bilete_excel:
            ws.append(row)
        # finished
        path_excel = str(Path(os.getcwd()) / "bilete.xlsx")
        wb.save(path_excel)
        self.app.excel = path_excel
        time.sleep(2)
        self.app.main_win.label_progres_generare.config(text=f"Am generat {bilete_valide} bilete")

    def genereaza_bilete(self):
        if not self.thread:
            self.thread = Thread(target=self._genereaza_bilete, name="Thread-genereaza-bilete")
            self.thread.start()
