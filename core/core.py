class CoreSportBets:
    def __init__(self, app):
        self.app = app
        self.nr_meciuri = None
        self.excel = None
        self.semne = None
        print("Create core.")

    def reset(self):
        self.nr_meciuri = None
        self.excel = None
        self.semne = list()
        print("Reset core.")
