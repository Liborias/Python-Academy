import mimetypes
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from zpravy import vytvor_zpravu, nahled_zpravy

MAX_PRILOHA = 1_000_000


# Nejdřív načteme a ověříme soubor, až pak měníme zprávu.
def pridej_prilohu(zprava, cesta):
    cesta = Path(cesta)
    # Načtěte omezený počet bajtů a přidejte přílohu s názvem bez cesty.
    return zprava


def hlavni():
    okno = tk.Tk()
    okno.title("Příloha před odesláním")
    okno.geometry("680x420")
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(0, weight=1)
    def nova_zprava():
        return vytvor_zpravu("eva@example.test", "jan@example.test", "Poznámky z Pythonu", "Dobrý den,\npřikládám cvičný soubor.")
    aktualni = [nova_zprava()]
    nahled = tk.Text(okno, wrap="word", width=60, height=10)
    nahled.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
    soubor_text = ttk.Label(okno, text="Příloha zatím není vybraná.")
    soubor_text.grid(row=1, column=0, pady=8)
    stav = ttk.Label(okno, text="Zpráva se pouze připravuje, nic se neodesílá.")
    stav.grid(row=3, column=0, pady=8)

    def zobraz():
        nahled.configure(state="normal")
        nahled.delete("1.0", "end")
        nahled.insert("1.0", nahled_zpravy(aktualni[0]))
        nahled.configure(state="disabled")

    def vyber():
        cesta = filedialog.askopenfilename(parent=okno, title="Vyberte cvičnou přílohu")
        if not cesta:
            stav.configure(text="Výběr přílohy zrušen.")
            return
        try:
            kandidat = nova_zprava()
            pridej_prilohu(kandidat, cesta)
        except (OSError, ValueError):
            stav.configure(text="Soubor nelze přiložit.")
            return
        aktualni[:] = [kandidat]
        prilohy = list(kandidat.iter_attachments())
        priloha = prilohy[0]
        soubor_text.configure(text=f"Příloha: {priloha.get_filename()} | {priloha.get_content_type()} | {len(priloha.get_payload(decode=True))} B")
        zobraz()
        stav.configure(text="Příloha je připravená. Zpráva nebyla odeslána.")

    ttk.Button(okno, text="Vybrat přílohu", command=vyber).grid(row=2, column=0, pady=8)
    zobraz()
    okno.mainloop()


if __name__ == "__main__":
    # Volba souboru a náhled ještě nejsou SMTP přenos.
    hlavni()
