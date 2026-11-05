from had_potrava import HladovyHad


class BezpecnyHad(HladovyHad):
    def krok(self, potrava=None):
        # Před pohybem posuďte kolizi. Odcházející ocas nemusí překážet.
        # Při kolizi vyvolejte ValueError a ponechte tělo beze změny.
        pass


if __name__ == "__main__":
    had = BezpecnyHad([(1, 1), (1, 0), (0, 0), (0, 1)], 3, 3)
    had.smer = (-1, 0)
    print("Do odcházejícího ocasu:", had.krok())
    had.smer = (1, 0)
    try:
        had.krok()
    except ValueError:
        print("Kolize zachycena; tělo:", had.body)
