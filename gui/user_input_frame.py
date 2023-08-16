import tkinter as tk

from gui.adauga_semn_window import AdaugaSemnWindow


class UserInputFrame:
    def __init__(self, app):
        self.app = app
        self.frame = None
        self.label_nr_meciuri = None
        self.entry_nr_meciuri = None
        self.label_semne = None
        self.listbox_semne = None
        self.button_adauga_semn = None
        self.win_adauga_semn = None

    def configure(self):
        self.frame = tk.Frame(self.app.main_win.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self._init_label_nr_meciuri()
        self._init_entry_nr_meciuri()
        self._init_label_semne()
        self._init_listbox_semne()
        self._init_button_adauga_semn()

    def _init_label_nr_meciuri(self):
        self.label_nr_meciuri = tk.Label(self.frame, text="Numar meciuri")
        self.label_nr_meciuri.grid(row=0, column=0)

    def _init_entry_nr_meciuri(self):
        self.entry_nr_meciuri = tk.Entry(self.frame, width=20, justify=tk.CENTER)
        self.entry_nr_meciuri.grid(row=1, column=0)

    def _init_label_semne(self):
        self.label_semne = tk.Label(self.frame, text="Semne")
        self.label_semne.grid(row=2, column=0)

    def _init_listbox_semne(self):
        self.listbox_semne = tk.Listbox(self.frame, width=50, justify=tk.CENTER)
        self.listbox_semne.grid(row=3, column=0, sticky="NSEW")

    def get_nr_meciuri(self):
        try:
            nr_meciuri = int(self.entry_nr_meciuri.get().strip())
            if nr_meciuri > 1:
                return nr_meciuri
            raise ValueError(f"Nr meciuri: {nr_meciuri}")
        except ValueError as ve:
            return None

    def _adauga_semn(self):
        nr_meciuri = self.get_nr_meciuri()
        if nr_meciuri:
            self.app.core.nr_meciuri = nr_meciuri
            self.app.main_win.root.wm_attributes('-disabled', 'True')
            self.win_adauga_semn = AdaugaSemnWindow(self.app)
            self.win_adauga_semn.configure()

    def _init_button_adauga_semn(self):
        self.button_adauga_semn = tk.Button(self.frame, text="Adauga semn", command=self._adauga_semn)
        self.button_adauga_semn.grid(row=4, column=0)

    def refresh_listbox_semne(self):
        self.listbox_semne.delete(0, tk.END)
        for semn in self.app.core.semne:
            self.listbox_semne.insert("end", str(semn))

    def reset(self):
        self.entry_nr_meciuri.delete(0, tk.END)
        self.listbox_semne.delete(0, tk.END)
