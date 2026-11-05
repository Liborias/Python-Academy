# Spustí se samostatné okno Turtle na počítači s Pythonem.
# Potřebné soubory projektu jsou připravené vedle tohoto programu.
from had_model import Had
from had_pohled import priprav_okno, vykresli


class Hra:
    def __init__(self, okno, had, pero, interval=160):
        self.okno = okno
        self.had = had
        self.pero = pero
        self.interval = interval
        self.spusteno = False

    def spust(self):
        if self.spusteno:
            return
        self.spusteno = True
        vykresli(self.had, self.pero)
        self.okno.update()
        self.okno.ontimer(self.tik, self.interval)

    def tik(self):
        self.had.krok()
        vykresli(self.had, self.pero)
        self.okno.update()
        self.okno.ontimer(self.tik, self.interval)


if __name__ == "__main__":
    had = Had([(8, 8), (7, 8), (6, 8)])
    okno, pero = priprav_okno(had)
    okno.title("Snake — pohyb přes okraj; zavřete okno pro konec")
    hra = Hra(okno, had, pero)
    hra.spust()
    okno.mainloop()
