class CoreSportBets:
    def __init__(self, app):
        self.app = app
        self.nr_meciuri = None
        self.excel = None
        self.semne = None

    def reset(self):
        self.nr_meciuri = None
        self.excel = None
        self.semne = list()
