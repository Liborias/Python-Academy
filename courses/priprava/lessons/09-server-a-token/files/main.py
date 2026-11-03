"""Pevně určený program, který smí výukový server spustit."""
import sys

print("Ahoj z projektu spuštěného přes token!")
print("Použitý Python:", sys.executable)
print("Virtuální prostředí:", sys.prefix != sys.base_prefix)
