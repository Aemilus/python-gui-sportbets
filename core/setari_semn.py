from openpyxl.styles import PatternFill


class SetariSemn:
    BASE_COLOR = int("fafcb1", base=16)

    def __init__(self, app):
        self.app = app
        self.semn = None
        self.minim = None
        self.maxim = None
        self.color = None

    def configure(self):
        self._init_semn()
        self._init_minim()
        self._init_maxim()

    def _init_semn(self):
        semn = self.app.main_win.user_input_frame.win_adauga_semn.entry_semn.get().strip()
        if semn:
            self.semn = semn
        else:
            raise ValueError(f"Semn: {semn}")

    def _init_minim(self):
        minim = int(self.app.main_win.user_input_frame.win_adauga_semn.entry_minim.get().strip())
        if minim >= 0:
            self.minim = minim
        else:
            raise ValueError(f"Minim: {minim}")

    def _init_maxim(self):
        maxim = int(self.app.main_win.user_input_frame.win_adauga_semn.entry_maxim.get().strip())
        if maxim >= 0:
            self.maxim = maxim
        else:
            raise ValueError(f"Maxim: {maxim}")

    def set_color(self):
        color = hex(self.BASE_COLOR + len(self.app.core.semne) * 100000)[2:8]
        self.color = PatternFill(start_color=color, end_color=color, fill_type="solid")

    def _is_unique(self):
        for semn_obj in self.app.core.semne:
            if semn_obj.semn == self.semn:
                return False
        else:
            return True

    def is_valid(self):
        if self.minim > self.maxim:
            return False
        if self.maxim > self.app.core.nr_meciuri:
            return False
        return self._is_unique()

    def __str__(self):
        return str({"semn": self.semn, "minim": self.minim, "maxim": self.maxim})
