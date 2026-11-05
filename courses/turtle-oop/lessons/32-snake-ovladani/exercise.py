from had_model import Had
from had_pohled import priprav_okno
from had_hra import Hra


class RizenaHra(Hra):
    def __init__(self, okno, had, pero, interval=160):
        super().__init__(okno, had, pero, interval)
        self.cekajici = None

    def nastav_smer(self, smer):
        # Přijměte nejvýš jednu kolmou změnu mezi dvěma tiky.
        pass

    def tik(self):
        # Použijte čekající směr, vyprázdněte ho a navázejte přes super.
        pass

    def nahoru(self):
        return self.nastav_smer((0, 1))

    def dolu(self):
        return self.nastav_smer((0, -1))

    def vlevo(self):
        return self.nastav_smer((-1, 0))

    def vpravo(self):
        return self.nastav_smer((1, 0))

    def pripoj(self):
        # Zaregistrujte čtyři metody bez závorek a zapněte příjem kláves.
        pass


if __name__ == "__main__":
    had = Had([(8, 8), (7, 8), (6, 8)])
    okno, pero = priprav_okno(had)
    okno.title("Snake — šipky; přes okraj projdete na druhou stranu")
    hra = RizenaHra(okno, had, pero)
    hra.pripoj()
    hra.spust()
    okno.mainloop()
