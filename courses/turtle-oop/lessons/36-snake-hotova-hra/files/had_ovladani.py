from had_model import Had
from had_pohled import priprav_okno
from had_hra import Hra


class RizenaHra(Hra):
    def __init__(self, okno, had, pero, interval=160):
        super().__init__(okno, had, pero, interval)
        self.cekajici = None

    def nastav_smer(self, smer):
        if smer not in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            return False
        if self.cekajici is not None or smer == self.had.smer:
            return False
        dx, dy = self.had.smer
        if smer == (-dx, -dy):
            return False
        self.cekajici = smer
        return True

    def tik(self):
        if self.cekajici is not None:
            self.had.smer = self.cekajici
        self.cekajici = None
        super().tik()

    def nahoru(self):
        return self.nastav_smer((0, 1))

    def dolu(self):
        return self.nastav_smer((0, -1))

    def vlevo(self):
        return self.nastav_smer((-1, 0))

    def vpravo(self):
        return self.nastav_smer((1, 0))

    def pripoj(self):
        self.okno.onkey(self.nahoru, "Up")
        self.okno.onkey(self.dolu, "Down")
        self.okno.onkey(self.vlevo, "Left")
        self.okno.onkey(self.vpravo, "Right")
        self.okno.listen()


if __name__ == "__main__":
    had = Had([(8, 8), (7, 8), (6, 8)])
    okno, pero = priprav_okno(had)
    okno.title("Snake — šipky; přes okraj projdete na druhou stranu")
    hra = RizenaHra(okno, had, pero)
    hra.pripoj()
    hra.spust()
    okno.mainloop()
