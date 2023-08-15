import os
import tkinter as tk

from core.genereaza_bilete import GenereazaBilete


class ProcesareFrame:
    def __init__(self, app):
        self.app = app
        self.frame = None
        self.label_progres_generare = None
        self.button_genereaza_bilete = None
        self.button_afiseaza_bilete = None
        self.button_reset = None

    def configure(self):
        self.frame = tk.Frame(self.app.main_win.root)
        self.frame.grid(row=1, column=0, padx=10, pady=10)
        self._init_label_progres_generare()
        self._init_button_genereaza_bilete()
        self._init_button_afiseaza_bilete()
        self._init_button_reset()
        print("Create procesare frame.")

    def _init_label_progres_generare(self):
        self.label_progres_generare = tk.Label(self.frame, text="")
        self.label_progres_generare.grid(row=0, column=0)

    def _genereaza_bilete(self):
        if self.app.core.semne:
            gen = GenereazaBilete(self.app)
            gen.genereaza_bilete()

    def _init_button_genereaza_bilete(self):
        self.button_genereaza_bilete = tk.Button(
            self.frame,
            text="Genereaza bilete",
            command=self._genereaza_bilete
        )
        self.button_genereaza_bilete.grid(row=1, column=0)

    def _afiseaza_bilete(self):
        if self.app.core.excel:
            os.startfile(self.app.core.excel)

    def _init_button_afiseaza_bilete(self):
        self.button_afiseaza_bilete = tk.Button(
            self.frame,
            text="Afiseaza bilete",
            command=self._afiseaza_bilete
        )
        self.button_afiseaza_bilete.grid(row=2, column=0)

    def _reset(self):
        self.app.core.reset()
        self.app.main_win.user_input_frame.reset()

    def _init_button_reset(self):
        self.button_reset = tk.Button(
            self.frame,
            text="Reset",
            command=self._reset
        )
        self.button_reset.grid(row=3, column=0, pady=20)
