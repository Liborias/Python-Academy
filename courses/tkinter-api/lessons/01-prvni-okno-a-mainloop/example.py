import tkinter as tk

# Tk vytvoří hlavní okno na grafické ploše počítače.
okno = tk.Tk()
okno.title("Moje první okno")
okno.geometry("420x240")
okno.minsize(320, 180)
# Hlavní smyčka zpracovává události, dokud uživatel okno nezavře.
okno.mainloop()
