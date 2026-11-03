from dataclasses import dataclass, field


@dataclass
class ZaznamHrace:
    jmeno: str
    body: int = 0
    udalosti: list[str] = field(default_factory=list)

    def zapis(self, text):
        self.udalosti.append(text)
        return len(self.udalosti)
