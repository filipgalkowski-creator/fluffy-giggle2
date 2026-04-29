import tkinter as tk
from tkinter import messagebox

rezerwacje = []

def otworz_okno_rezerwacji():
    okno = tk.Tk()
    okno.title("Rezerwacja stolika")
    okno.geometry("300x300")

    tk.Label(okno, text="Imię i nazwisko").pack()
    entry_imie = tk.Entry(okno)
    entry_imie.pack()

    tk.Label(okno, text="Liczba osób").pack()
    entry_osoby = tk.Entry(okno)
    entry_osoby.pack()

    tk.Label(okno, text="Godzina").pack()
    entry_godzina = tk.Entry(okno)
    entry_godzina.pack()

    tk.Label(okno, text="Uwagi").pack()
    entry_uwagi = tk.Entry(okno)
    entry_uwagi.pack()

    def zatwierdz():
        imie = entry_imie.get().strip()
        osoby = entry_osoby.get().strip()
        godzina = entry_godzina.get().strip()
        uwagi = entry_uwagi.get().strip()

        if not imie:
            messagebox.showerror("Błąd", "Podaj imię i nazwisko")
            return

        if not osoby.isdigit():
            messagebox.showerror("Błąd", "Liczba osób musi być liczbą")
            return

        if not godzina:
            messagebox.showerror("Błąd", "Podaj godzinę")
            return

        rezerwacja = {
            "imie_nazwisko": imie,
            "liczba_osob": int(osoby),
            "godzina": godzina,
            "uwagi": uwagi
        }

        rezerwacje.append(rezerwacja)

        messagebox.showinfo("Sukces", "Rezerwacja dodana")

        print(rezerwacje)

        okno.destroy()

    tk.Button(okno, text="Zatwierdź", command=zatwierdz).pack()

    okno.mainloop()


otworz_okno_rezerwacji()