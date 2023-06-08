from gui.main_window import MainWindow


# noinspection PyAttributeOutsideInit
class AppSportBets:
    def __init__(self):
        self.main_win = MainWindow(self)
        self.reset()

    def reset(self):
        self.nr_meciuri = None
        self.excel = None
        self.semne = list()


if __name__ == '__main__':
    app = AppSportBets()
    app.main_win.root.mainloop()
