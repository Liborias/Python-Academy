class Zaklad:
    def cesta(self):
        pass


class Levy(Zaklad):
    def cesta(self):
        # Připojte vlastní část před výsledek super().
        pass


class Pravy(Zaklad):
    def cesta(self):
        pass


class Oba(Levy, Pravy):
    pass


class Obracene(Pravy, Levy):
    pass
