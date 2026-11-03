class Zaklad:
    def cesta(self):
        return ["Zaklad"]


class Levy(Zaklad):
    def cesta(self):
        return ["Levy"] + super().cesta()


class Pravy(Zaklad):
    def cesta(self):
        return ["Pravy"] + super().cesta()


class Oba(Levy, Pravy):
    pass


class Obracene(Pravy, Levy):
    pass
