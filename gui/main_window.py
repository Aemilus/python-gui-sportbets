import tkinter as tk
import os

from core.genereaza_bilete import GenereazaBilete
from gui.adauga_semn_window import AdaugaSemnWindow


class MainWindow:
    def __init__(self, app):
        self.app = app
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
        self.user_input_frame = tk.Frame(self.root)
        self.user_input_frame.grid(row=0, column=0, padx=10, pady=10)
        self._init_label_nr_meciuri()
        self._init_entry_nr_meciuri()
        self._init_label_semne()
        self._init_listbox_semne()
        self._init_button_adauga_semn()

    def _init_label_nr_meciuri(self):
        self.label_nr_meciuri = tk.Label(self.user_input_frame, text="Numar meciuri")
        self.label_nr_meciuri.grid(row=0, column=0)

    def _init_entry_nr_meciuri(self):
        self.entry_nr_meciuri = tk.Entry(self.user_input_frame, width=20, justify=tk.CENTER)
        self.entry_nr_meciuri.grid(row=1, column=0)

    def _init_label_semne(self):
        self.label_semne = tk.Label(self.user_input_frame, text="Semne")
        self.label_semne.grid(row=2, column=0)

    def _init_listbox_semne(self):
        self.listbox_semne = tk.Listbox(self.user_input_frame, width=50, justify=tk.CENTER)
        self.listbox_semne.grid(row=3, column=0, sticky="NSEW")

    def _set_nr_meciuri(self):
        try:
            nr_meciuri = int(self.entry_nr_meciuri.get().strip())
            if nr_meciuri > 1:
                self.app.nr_meciuri = nr_meciuri
                return self.app.nr_meciuri
            raise ValueError(f"Nr meciuri: {nr_meciuri}")
        except ValueError:
            return None

    def _adauga_semn(self):
        if self._set_nr_meciuri():
            self.root.wm_attributes('-disabled', 'True')
            self.win_adauga_semn = AdaugaSemnWindow(self.app)

    def _init_button_adauga_semn(self):
        self.button_adauga_semn = tk.Button(self.user_input_frame, text="Adauga semn", command=self._adauga_semn)
        self.button_adauga_semn.grid(row=4, column=0)

    def refresh_listbox_semne(self):
        self.listbox_semne.delete(0, tk.END)
        for semn in self.app.semne:
            self.listbox_semne.insert("end", str(semn))

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
        if self.app.semne:
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
        self.app.reset()
        self.entry_nr_meciuri.delete(0, tk.END)
        self.listbox_semne.delete(0, tk.END)

    def _init_button_reset(self):
        self.button_reset = tk.Button(
            self.procesare_frame,
            text="Reset",
            command=self._reset
        )
        self.button_reset.grid(row=3, column=0, pady=20)
