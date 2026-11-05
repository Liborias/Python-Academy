from had_potrava import HladovyHad


class BezpecnyHad(HladovyHad):
    def krok(self, potrava=None):
        x, y = self.body[0]
        dx, dy = self.smer
        nova = ((x + dx) % self.sirka, (y + dy) % self.vyska)
        if nova == potrava:
            obsazene = self.body
        else:
            obsazene = self.body[:-1]
        if nova in obsazene:
            raise ValueError("Had narazil do těla")
        return super().krok(potrava)


if __name__ == "__main__":
    had = BezpecnyHad([(1, 1), (1, 0), (0, 0), (0, 1)], 3, 3)
    had.smer = (-1, 0)
    print("Do odcházejícího ocasu:", had.krok())
    had.smer = (1, 0)
    try:
        had.krok()
    except ValueError:
        print("Kolize zachycena; tělo:", had.body)
