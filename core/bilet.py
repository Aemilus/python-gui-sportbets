class Bilet:
    def __init__(self, app, combinatie):
        self.app = app
        self.combinatie = combinatie
        self.nr_bilet = None

    def is_valid(self):
        for semn_obj in self.app.core.semne:
            nr_semne = len([semn_comb for semn_comb in self.combinatie if semn_comb.semn == semn_obj.semn])
            if nr_semne < semn_obj.minim:
                return False
            if nr_semne > semn_obj.maxim:
                return False
        return True
