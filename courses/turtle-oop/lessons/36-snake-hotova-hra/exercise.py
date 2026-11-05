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
        # Nová generace, nová partie, smazání čekající zatáčky a první snímek.
        pass

    def naplanuj(self):
        # Jen pro běžící partii; callback si pamatuje číslo této generace.
        pass

    def tik_generace(self, generace):
        if generace == self.generace:
            self.tik()

    def tik(self):
        # Použijte zatáčku, proveďte jeden krok partie a obnovte snímek.
        # Ukončená partie už nepokračuje.
        pass

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
