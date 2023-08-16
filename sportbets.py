from core.core import CoreSportBets
from gui.main_window import MainWindow


# noinspection PyAttributeOutsideInit
class AppSportBets:
    def __init__(self):
        self.core = None
        self.main_win = None

    def reset(self):
        self.core.reset()
        self.main_win.reset()

    def start(self):
        self.core = CoreSportBets(self)
        self.main_win = MainWindow(self)
        self.main_win.configure()
        self.reset()
        try:
            self.main_win.root.mainloop()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = AppSportBets()
    app.start()
