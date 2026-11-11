# Vstup hry i testy používají stejné třídy ze společného modelu.
from model_hry import Hra
from herni_okno import spustit

if __name__ == '__main__':
    spustit(Hra())
