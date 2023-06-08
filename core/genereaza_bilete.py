import itertools
import os
from pathlib import Path
from threading import Thread

from openpyxl import Workbook


class GenereazaBilete:
    def __init__(self, app):
        self.app = app
        self.bilete = None
        self.thread = None

    def _genereaza_bilete(self):
        self.bilete = itertools.product(self.app.semne, repeat=self.app.nr_meciuri)
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
                self.app.main_win.label_progres_generare.config(text=str(bilete_valide))
                ws.append([semn_meci.semn for semn_meci in bilet])
        # finished
        path_excel = str(Path(os.getcwd()) / "bilete.xlsx")
        wb.save(path_excel)
        self.app.excel = path_excel
        self.app.main_win.label_progres_generare.config(text=f"Am generat {bilete_valide} bilete")

    def genereaza_bilete(self):
        if not self.thread:
            self.thread = Thread(target=self._genereaza_bilete, name="Thread-genereaza-bilete")
            self.thread.start()
