# Hotová hra spojuje model, pravidla, zobrazení a ovládání.
# Enter obnoví partii a staré časovače už do ní nezasáhnou.
import random
from had_model import Had
from had_ovladani import RizenaHra
from had_partie import Partie
from had_panel import priprav_hriste, vykresli_partii


class SnakeHra(RizenaHra):
    def __init__(self, okno, pero, jidlo, text, body, sirka=20, vyska=16, interval=160, vyber=random.choice):
        self.zacatek = list(body)
        self.sirka = sirka
        self.vyska = vyska
        self.vyber = vyber
        self.jidlo = jidlo
        self.text = text
        self.partie = None
        self.generace = 0
        super().__init__(okno, Had(body, sirka, vyska), pero, interval)

    def obnov(self):
        vykresli_partii(self.partie, self.pero, self.jidlo, self.text)
        self.okno.update()

    def spust(self):
        if not self.spusteno:
            self.restart()

    def restart(self):
        self.generace += 1
        self.partie = Partie(self.zacatek, self.sirka, self.vyska, self.vyber)
        self.had = self.partie.had
        self.cekajici = None
        self.spusteno = True
        generace = self.generace
        self.obnov()
        if generace == self.generace:
            self.naplanuj()

    def naplanuj(self):
        if self.partie.stav == "hra":
            generace = self.generace
            self.okno.ontimer(lambda: self.tik_generace(generace), self.interval)

    def tik_generace(self, generace):
        if generace == self.generace:
            self.tik()

    def tik(self):
        if self.partie.stav != "hra":
            return
        if self.cekajici is not None:
            self.had.smer = self.cekajici
        self.cekajici = None
        self.partie.krok()
        generace = self.generace
        self.obnov()
        if generace == self.generace:
            self.naplanuj()

    def nastav_smer(self, smer):
        if self.partie is None or self.partie.stav != "hra":
            return False
        return super().nastav_smer(smer)

    def pripoj(self):
        super().pripoj()
        self.okno.onkey(self.restart, "Return")


if __name__ == "__main__":
    okno, pero, jidlo, text = priprav_hriste(20, 16)
    hra = SnakeHra(okno, pero, jidlo, text, [(8, 8), (7, 8), (6, 8)])
    hra.pripoj()
    hra.spust()
    okno.mainloop()
