import os
import queue
import threading
import smtplib
import tkinter as tk
from tkinter import ttk
from email.parser import BytesParser
from email.policy import default
from cvicna_posta import cvicna_posta
from zpravy import vytvor_zpravu, nahled_zpravy
from odesilani import over_spojeni, odesli_do_zachytu


def nacti_nastaveni(prostredi, vychozi_port):
    # Přečtěte tři proměnné, převeďte typy a použijte over_spojeni.
    raise ValueError("Nastavení ještě není hotové.")


def hlavni(posta):
    okno = tk.Tk()
    okno.title("Nastavení a výsledek SMTP")
    okno.geometry("780x560")
    okno.columnconfigure(0, weight=1)
    okno.rowconfigure(3, weight=1)
    vysledky = queue.Queue()
    rezim = tk.StringVar(okno, value="prijmout")
    stav = ttk.Label(okno, text="Zpráva zatím nebyla předána.")
    stav.grid(row=0, column=0, padx=12, pady=10)
    nastaveni_text = ttk.Label(okno, text="Nastavení se ověří před spojením.")
    nastaveni_text.grid(row=1, column=0, pady=6)
    pocet = ttk.Label(okno, text="Zachyceno: 0")
    pocet.grid(row=2, column=0, pady=6)
    nahled = tk.Text(okno, wrap="word", height=8, width=65)
    nahled.grid(row=3, column=0, padx=12, pady=10, sticky="nsew")

    def zkontroluj():
        zpravy = posta.zpravy
        pocet.configure(text=f"Zachyceno: {len(zpravy)}")
        nahled.configure(state="normal")
        nahled.delete("1.0", "end")
        if zpravy:
            zprava = BytesParser(policy=default).parsebytes(zpravy[-1].data)
            nahled.insert("1.0", nahled_zpravy(zprava))
        else:
            nahled.insert("1.0", "Místní záchyt je prázdný.")
        nahled.configure(state="disabled")

    def pracovnik(zprava, nastaveni):
        try:
            odesli_do_zachytu(zprava, nastaveni["host"], nastaveni["port"], nastaveni["timeout"])
            vysledky.put("prijato")
        except smtplib.SMTPRecipientsRefused:
            vysledky.put("odmitnuto")
        except (smtplib.SMTPServerDisconnected, TimeoutError):
            vysledky.put("nejiste")
        except (smtplib.SMTPException, OSError):
            vysledky.put("chyba")

    def vyzvedni():
        try:
            vysledek = vysledky.get_nowait()
        except queue.Empty:
            okno.after(25, vyzvedni)
            return
        odeslat.configure(state="normal")
        for volba in volby:
            volba.configure(state="normal")
        zpravy = {"prijato": "Zprávu převzal místní záchyt.",
                  "odmitnuto": "Příjemce byl odmítnut. Zpráva nebyla převzata.",
                  "nejiste": "Přenos není potvrzený. Před novým pokusem zkontrolujte záchyt.",
                  "chyba": "Spojení nebo SMTP služba selhaly. Ověřte nastavení."}
        stav.configure(text=zpravy[vysledek])
        zkontroluj()

    def odesli():
        # Prostředí i Tk volby čteme v hlavním vlákně před spuštěním pracovníka.
        try:
            nastaveni = nacti_nastaveni(os.environ, posta.port)
        except ValueError:
            stav.configure(text="Neplatné nastavení. Opravte proměnné prostředí a spusťte program znovu.")
            return
        nastaveni_text.configure(text=f"Nastavení: {nastaveni['host']}:{nastaveni['port']} | timeout {nastaveni['timeout']:g} s")
        posta.nastav_rezim(rezim.get())
        zprava = vytvor_zpravu("eva@example.test", "jan@example.test", "Zkouška nastavení", "Dobrý den,\nzkouším místní záchyt.")
        stav.configure(text="Předávám zprávu místnímu záchytu...")
        odeslat.configure(state="disabled")
        for volba in volby:
            volba.configure(state="disabled")
        threading.Thread(target=pracovnik, args=(zprava, nastaveni), daemon=True).start()
        okno.after(25, vyzvedni)

    volby = []
    for text, hodnota in [("Přijetí", "prijmout"), ("Odmítnutí příjemce", "odmitnout"), ("Opožděné potvrzení", "pomalu")]:
        volba = ttk.Radiobutton(okno, text=text, variable=rezim, value=hodnota)
        volba.grid(row=4 + len(volby), column=0)
        volby.append(volba)
    odeslat = ttk.Button(okno, text="Předat místnímu záchytu", command=odesli)
    odeslat.grid(row=7, column=0, pady=10)
    ttk.Button(okno, text="Zkontrolovat záchyt", command=zkontroluj).grid(row=8, column=0, pady=6)
    zkontroluj()
    okno.mainloop()


if __name__ == "__main__":
    # Nic se neodesílá automaticky; přenos spustí až tlačítko a jen na loopback.
    with cvicna_posta() as posta:
        hlavni(posta)
