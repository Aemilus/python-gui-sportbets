import tkinter as tk

from core.setari_semn import SetariSemn


class AdaugaSemnWindow:
    def __init__(self, app):
        self.app = app
        self.win = None
        self.user_input_frame = None
        self.label_semn = None
        self.entry_semn = None
        self.label_minim = None
        self.entry_minim = None
        self.label_maxim = None
        self.entry_maxim = None
        self.button_save = None

    def configure(self):
        self._init_win()
        self._init_user_input_frame()
        self._init_button_save()

    def _init_win(self):
        self.win = tk.Toplevel(self.app.main_win.root)
        self.win.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.win.wm_attributes('-toolwindow', 'True')
        self.win.wm_attributes('-topmost', 'True')
        self.win.title("Adauga semn")

    def _init_user_input_frame(self):
        self.user_input_frame = tk.Frame(self.win)
        self.user_input_frame.grid(row=0, column=0, ipadx=10, ipady=10)
        self._init_entry_semn()
        self._init_entry_minim()
        self._init_entry_maxim()

    def _init_entry_semn(self):
        self.label_semn = tk.Label(self.user_input_frame, text="Semn")
        self.label_semn.grid(row=0, column=0)
        self.entry_semn = tk.Entry(self.user_input_frame, justify=tk.CENTER)
        self.entry_semn.grid(row=0, column=1)

    def _init_entry_minim(self):
        self.label_minim = tk.Label(self.user_input_frame, text="Minim")
        self.label_minim.grid(row=1, column=0)
        self.entry_minim = tk.Entry(self.user_input_frame, justify=tk.CENTER)
        self.entry_minim.grid(row=1, column=1)

    def _init_entry_maxim(self):
        self.label_maxim = tk.Label(self.user_input_frame, text="Maxim")
        self.label_maxim.grid(row=2, column=0)
        self.entry_maxim = tk.Entry(self.user_input_frame, justify=tk.CENTER)
        self.entry_maxim.grid(row=2, column=1)

    def _on_closing(self):
        self.win.destroy()
        self.app.main_win.root.wm_attributes('-disabled', 'False')
        self.app.main_win.root.wm_attributes('-topmost', 'True')

    def _salveaza_semn(self):
        try:
            semn = SetariSemn(self.app)
            semn.configure()
            if semn.is_valid():
                self.app.core.semne.append(semn)
                self.app.main_win.user_input_frame.refresh_listbox_semne()
                self._on_closing()
            else:
                raise ValueError(f"Setari semn: {semn}")
        except ValueError:
            return

    def _init_button_save(self):
        self.button_save = tk.Button(self.win, text="Salveaza", command=self._salveaza_semn)
        self.button_save.grid(row=1, column=0)
