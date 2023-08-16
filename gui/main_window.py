import tkinter as tk

from gui.user_input_frame import UserInputFrame
from gui.procesare_frame import ProcesareFrame


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
        self.procesare_frame = ProcesareFrame(self.app)
        self.procesare_frame.configure()

    def reset(self):
        self.user_input_frame.reset()
        self.procesare_frame.reset()
