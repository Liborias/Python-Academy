from dataclasses import dataclass, field


@dataclass
class Vyprava:
    cil: str
    ucastnici: list[str] = field(default_factory=list)  # Nový výchozí seznam.


les = Vyprava("Les")
hory = Vyprava("Hory")
print(les)                            # Automaticky vytvořený repr.
les.ucastnici.append("Ema")
print(les.ucastnici)                   # ['Ema']
print(hory.ucastnici)                  # []: jiný objekt má vlastní seznam.
print(les == Vyprava("Les", ["Ema"]))  # True: stejné hodnoty polí.
