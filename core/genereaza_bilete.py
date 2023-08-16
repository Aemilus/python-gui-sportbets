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
        self.tabel_bilete = None
        self._reset()

    def _reset(self):
        self.combinatii = None

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
                self.app.main_win.procesare_frame.label_progres_generare.config(text=str(self.NR_BILETE_VALIDE))
                for row in range(self.app.core.nr_meciuri):
                    self.tabel_bilete[row].append(bilet.combinatie[row].semn)
                    self.tabel_bilete[row].append("")
                self.tabel_bilete[self.app.core.nr_meciuri].append(f"Bilet {bilet.nr_bilet}")
                self.tabel_bilete[self.app.core.nr_meciuri].append("")
        for row in self.tabel_bilete:
            ws.append(row)
        # styling
        culori_semne = dict()
        for semn in self.app.core.semne:
            culori_semne[semn.semn] = semn.color
        if self.tabel_bilete:
            for row in ws.iter_rows(
                    min_row=self.app.core.nr_meciuri+1,
                    max_row=self.app.core.nr_meciuri+1,
                    min_col=1,
                    max_col=len(self.tabel_bilete[0])
            ):
                for cell in row:
                    if cell.value:
                        cell.fill = self.HEADER_COLOR
        if self.tabel_bilete:
            for row in ws.iter_rows(
                    min_row=1, max_row=self.app.core.nr_meciuri, min_col=1, max_col=len(self.tabel_bilete[0])):
                for cell in row:
                    if str(cell.value):
                        cell.fill = culori_semne[str(cell.value)]
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
