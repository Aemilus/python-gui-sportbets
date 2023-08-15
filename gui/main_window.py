import os
import tkinter as tk

from core.genereaza_bilete import GenereazaBilete
from gui.user_input_frame import UserInputFrame


class MainWindow:
    def __init__(self, app):
        self.app = app
        self.root = None
        self.user_input_frame = None
        self.procesare_frame = None

    def configure(self):
        self._init_root()
        self._init_user_input_frame()
        self._init_procesare_frame()

    def _init_root(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.geometry("400x420")
        self.root.title("Sportbets")

    def _init_user_input_frame(self):
        self.user_input_frame = UserInputFrame(self.app)
        self.user_input_frame.configure()

    def _init_procesare_frame(self):
        self.procesare_frame = tk.Frame(self.root)
        self.procesare_frame.grid(row=1, column=0, padx=10, pady=10)
        self._init_label_progres_generare()
        self._init_button_genereaza_bilete()
        self._init_button_afiseaza_bilete()
        self._init_button_reset()

    def _init_label_progres_generare(self):
        self.label_progres_generare = tk.Label(self.procesare_frame, text="")
        self.label_progres_generare.grid(row=0, column=0)

    def _genereaza_bilete(self):
        if self.app.core.semne:
            gen = GenereazaBilete(self.app)
            gen.genereaza_bilete()

    def _init_button_genereaza_bilete(self):
        self.button_genereaza_bilete = tk.Button(
            self.procesare_frame,
            text="Genereaza bilete",
            command=self._genereaza_bilete
        )
        self.button_genereaza_bilete.grid(row=1, column=0)

    def _afiseaza_bilete(self):
        if self.app.excel:
            os.startfile(self.app.excel)

    def _init_button_afiseaza_bilete(self):
        self.button_afiseaza_bilete = tk.Button(
            self.procesare_frame,
            text="Afiseaza bilete",
            command=self._afiseaza_bilete
        )
        self.button_afiseaza_bilete.grid(row=2, column=0)

    def _reset(self):
        self.app.core.reset()
        self.user_input_frame.reset()

    def _init_button_reset(self):
        self.button_reset = tk.Button(
            self.procesare_frame,
            text="Reset",
            command=self._reset
        )
        self.button_reset.grid(row=3, column=0, pady=20)
