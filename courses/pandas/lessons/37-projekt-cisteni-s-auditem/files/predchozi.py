# Ověřené kroky předchozích lekcí; zdroj se nemění.
from pathlib import Path
import pandas as pd

def over_schema(tabulka, povinne):
    return isinstance(tabulka, pd.DataFrame) and tabulka.columns.is_unique and set(povinne).issubset(tabulka.columns)
