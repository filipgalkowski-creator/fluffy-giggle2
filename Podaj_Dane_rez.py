import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime, time

REZERWACJE_DIR = "rezerwacje"
LICZBA_STOLIKOW = 6
GODZINY_OTWARCIA = (11, 23)  # 11:00 do 23:00
CENA_PODSTAWOWA = 50  # PLN
CENA_NOCNA = 100  # PLN (dla godzin 21:00-23:00)
DODATEK_ZA_UWAGI = 20  # PLN (jeśli są uwagi)

# Utwórz folder na rezerwacje jeśli nie istnieje
if not os.path.exists(REZERWACJE_DIR):
    os.makedirs(REZERWACJE_DIR)

def get_next_rezerwacja_number():
    """Zwraca następny numer rezerwacji"""
    files = [f for f in os.listdir(REZERWACJE_DIR) if f.startswith("rezerwacja_") and f.endswith(".json")]
    if not files:
        return 1
    numbers = []
    for f in files:
        try:
            num = int(f.replace("rezerwacja_", "").replace(".json", ""))
            numbers.append(num)
        except:
            pass
    return max(numbers) + 1 if numbers else 1

def get_dostepne_stoliki(godzina_str):
    """Zwraca listę dostępnych stolikow na podaną godzinę"""
    try:
        godzina = int(godzina_str.split(":")[0])
    except:
        return list(range(1, LICZBA_STOLIKOW + 1))
    
    zarezerwowane = set()
    files = [f for f in os.listdir(REZERWACJE_DIR) if f.startswith("rezerwacja_") and f.endswith(".json")]
    
    for file in files:
        try:
            with open(os.path.join(REZERWACJE_DIR, file), 'r', encoding='utf-8') as f:
                rez = json.load(f)
                rez_godzina = int(rez.get("godzina", "").split(":")[0])
                if rez_godzina == godzina:
                    zarezerwowane.add(rez.get("stolik", -1))
        except:
            pass
    
    dostepne = [s for s in range(1, LICZBA_STOLIKOW + 1) if s not in zarezerwowane]
    return dostepne

def get_dostepne_godziny(stolik_str):
    """Zwraca listę dostępnych godzin dla podanego stolika"""
    try:
        stolik = int(stolik_str)
    except:
        return [f"{h}:00" for h in range(GODZINY_OTWARCIA[0], GODZINY_OTWARCIA[1])]
    
    zarezerwowane = set()
    files = [f for f in os.listdir(REZERWACJE_DIR) if f.startswith("rezerwacja_") and f.endswith(".json")]
    
    for file in files:
        try:
            with open(os.path.join(REZERWACJE_DIR, file), 'r', encoding='utf-8') as f:
                rez = json.load(f)
                if rez.get("stolik") == stolik:
                    zarezerwowane.add(rez.get("godzina", ""))
        except:
            pass
    
    dostepne = [f"{h}:00" for h in range(GODZINY_OTWARCIA[0], GODZINY_OTWARCIA[1]) 
                if f"{h}:00" not in zarezerwowane]
    return dostepne

def oblicz_cene(godzina_str, uwagi_str):
    """Oblicza cenę rezerwacji na podstawie godziny i uwag"""
    try:
        godzina = int(godzina_str.split(":")[0])
    except:
        godzina = 11
    
    cena = CENA_PODSTAWOWA
    
    # Nocna taryfa dla ostatnich 3 godzin (21:00, 22:00, 23:00)
    if godzina >= 21:
        cena = CENA_NOCNA
    
    # Dodatek za uwagi
    if uwagi_str.strip():
        cena += DODATEK_ZA_UWAGI
    
    return cena

def otworz_okno_rezerwacji():
    okno = tk.Tk()
    okno.title("Rezerwacja Stolika")
    okno.geometry("450x600")
    okno.config(bg="#F0F2F5")

    # Tytuł
    tk.Label(okno, text="Rezerwacja Stolika", font=("Segoe UI", 18, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(20, 20))

    tk.Label(okno, text="Imię i nazwisko", font=("Segoe UI", 11, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(10, 0))
    entry_imie = tk.Entry(okno, width=45, font=("Segoe UI", 10), bg="white", fg="#1C1E21", relief="solid", bd=1)
    entry_imie.pack(pady=(0, 10))

    tk.Label(okno, text="Liczba osób", font=("Segoe UI", 11, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(10, 0))
    entry_osoby = tk.Entry(okno, width=45, font=("Segoe UI", 10), bg="white", fg="#1C1E21", relief="solid", bd=1)
    entry_osoby.pack(pady=(0, 10))

    tk.Label(okno, text="Stolik", font=("Segoe UI", 11, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(10, 0))
    combo_stolik = ttk.Combobox(okno, values=list(range(1, LICZBA_STOLIKOW + 1)), width=42, state="readonly", font=("Segoe UI", 10))
    combo_stolik.pack(pady=(0, 10))

    tk.Label(okno, text="Godzina (format HH:00)", font=("Segoe UI", 11, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(10, 0))
    combo_godzina = ttk.Combobox(okno, width=42, state="readonly", font=("Segoe UI", 10))
    combo_godzina.pack(pady=(0, 10))

    tk.Label(okno, text="Uwagi (opcjonalnie)", font=("Segoe UI", 11, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(10, 0))
    entry_uwagi = tk.Entry(okno, width=45, font=("Segoe UI", 10), bg="white", fg="#1C1E21", relief="solid", bd=1)
    entry_uwagi.pack(pady=(0, 10))

    # Label do wyświetlenia ceny
    label_cena = tk.Label(okno, text="Cena: 0 PLN", font=("Segoe UI", 12, "bold"), bg="#F0F2F5", fg="#007BFF")
    label_cena.pack(pady=(10, 0))

    def aktualizuj_cene(event=None):
        """Aktualizuje wyświetlaną cenę"""
        godzina = combo_godzina.get()
        uwagi = entry_uwagi.get()
        if godzina:
            cena = oblicz_cene(godzina, uwagi)
            label_cena.config(text=f"Cena: {cena} PLN")

    # Aktualizuj dostępne godziny gdy zmieni się stolik
    def on_stolik_change(event=None):
        stolik = combo_stolik.get()
        if stolik:
            godziny = get_dostepne_godziny(stolik)
            combo_godzina['values'] = godziny
            if godziny:
                combo_godzina.set(godziny[0])
                aktualizuj_cene()

    combo_stolik.bind("<<ComboboxSelected>>", on_stolik_change)
    combo_godzina.bind("<<ComboboxSelected>>", aktualizuj_cene)
    entry_uwagi.bind("<KeyRelease>", aktualizuj_cene)
    
    # Ustaw początkowe godziny
    combo_godzina['values'] = [f"{h}:00" for h in range(GODZINY_OTWARCIA[0], GODZINY_OTWARCIA[1])]
    if combo_godzina['values']:
        combo_godzina.set(combo_godzina['values'][0])
        aktualizuj_cene()

    def zatwierdz():
        imie = entry_imie.get().strip()
        osoby = entry_osoby.get().strip()
        stolik = combo_stolik.get()
        godzina = combo_godzina.get()
        uwagi = entry_uwagi.get().strip()

        if not imie:
            messagebox.showerror("Błąd", "Podaj imię i nazwisko")
            return

        if not osoby.isdigit() or int(osoby) < 1:
            messagebox.showerror("Błąd", "Liczba osób musi być liczbą większą od 0")
            return

        if not stolik:
            messagebox.showerror("Błąd", "Wybierz stolik")
            return

        if not godzina:
            messagebox.showerror("Błąd", "Wybierz godzinę")
            return

        # Sprawdź czy stolik i godzina są dostępne
        if int(stolik) not in get_dostepne_stoliki(godzina):
            messagebox.showerror("Błąd", f"Stolik {stolik} nie jest dostępny o {godzina}")
            return

        # Oblicz cenę
        cena = oblicz_cene(godzina, uwagi)

        # Utwórz rezerwację
        numer_rezerwacji = get_next_rezerwacja_number()
        rezerwacja = {
            "numer": numer_rezerwacji,
            "imie_nazwisko": imie,
            "liczba_osob": int(osoby),
            "stolik": int(stolik),
            "godzina": godzina,
            "uwagi": uwagi,
            "cena_pln": cena,
            "data_rezerwacji": datetime.now().isoformat()
        }

        # Zapisz do osobnego pliku
        filename = os.path.join(REZERWACJE_DIR, f"rezerwacja_{numer_rezerwacji:03d}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rezerwacja, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sukces", f"Rezerwacja #{numer_rezerwacji:03d} dodana\nStolik {stolik} o {godzina}\nCena: {cena} PLN")

        okno.destroy()

    tk.Button(okno, text="Zatwierdź", command=zatwierdz, font=("Segoe UI", 12, "bold"), bg="#007BFF", fg="white", width=45, height=2, bd=0, cursor="hand2", activebackground="#0056b3").pack(pady=15)

    okno.mainloop()

def otworz_okno_anulowania_rezerwacji():
    """Okno do anulowania rezerwacji - wyświetla listę i pozwala kliknąć aby usunąć"""
    okno = tk.Tk()
    okno.title("Anulowanie Rezerwacji")
    okno.geometry("900x550")
    okno.config(bg="#F0F2F5")

    # Tytuł
    tk.Label(okno, text="Anulowanie Rezerwacji - Kliknij aby usunąć", font=("Segoe UI", 18, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(15, 10))

    # Ramka do scrollowania
    canvas_frame = tk.Frame(okno, bg="#F0F2F5")
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Canvas z scrollbarem
    canvas = tk.Canvas(canvas_frame, bg="#F0F2F5", highlightthickness=0)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F0F2F5")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Pobierz dane rezerwacji
    rezerwacje = []
    files = [f for f in os.listdir(REZERWACJE_DIR) if f.startswith("rezerwacja_") and f.endswith(".json")]
    
    for file in sorted(files):
        try:
            with open(os.path.join(REZERWACJE_DIR, file), 'r', encoding='utf-8') as f:
                rez = json.load(f)
                rezerwacje.append((file, rez))
        except:
            pass

    # Utwórz nagłówek tabeli
    table_frame = tk.Frame(scrollable_frame, bg="#F0F2F5")
    table_frame.pack(fill=tk.X)

    header_bg = "#007BFF"
    header_fg = "white"
    
    tk.Label(table_frame, text="Nr", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=6, anchor="center", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)
    tk.Label(table_frame, text="Imię i Nazwisko", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=20, anchor="w", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)
    tk.Label(table_frame, text="Stolik", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=8, anchor="center", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)
    tk.Label(table_frame, text="Godzina", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=10, anchor="center", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)
    tk.Label(table_frame, text="Osoby", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=8, anchor="center", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)
    tk.Label(table_frame, text="Uwagi", font=("Segoe UI", 10, "bold"), bg=header_bg, fg=header_fg, width=25, anchor="w", relief="solid", bd=1).pack(side=tk.LEFT, padx=1, pady=1)

    # Wyświetl każdą rezerwację jako clickable row
    for idx, (filename, rez) in enumerate(rezerwacje):
        row_frame = tk.Frame(scrollable_frame, bg="#F0F2F5", height=40)
        row_frame.pack(fill=tk.X)

        numer = rez.get("numer", 0)
        imie = rez.get("imie_nazwisko", "")
        stolik = rez.get("stolik", "")
        godzina = rez.get("godzina", "")
        osoby = rez.get("liczba_osob", "")
        uwagi = rez.get("uwagi", "")

        bg_color = "#E8F4F8" if idx % 2 == 0 else "white"

        def create_delete_function(file_to_delete, rez_num):
            def delete_reservation():
                if messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz anulować rezerwację #{rez_num:03d}?"):
                    try:
                        os.remove(os.path.join(REZERWACJE_DIR, file_to_delete))
                        messagebox.showinfo("Sukces", f"Rezerwacja #{rez_num:03d} została anulowana")
                        okno.destroy()
                        otworz_okno_anulowania_rezerwacji()
                    except Exception as e:
                        messagebox.showerror("Błąd", f"Nie udało się usunąć rezerwacji: {str(e)}")
            return delete_reservation

        # Tworzymy clickable elementy
        tk.Label(row_frame, text=f"{numer:03d}", font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=6, anchor="center", relief="flat", bd=1, cursor="hand2").pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=False)
        
        imie_label = tk.Label(row_frame, text=imie, font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=20, anchor="w", relief="flat", bd=1, cursor="hand2")
        imie_label.pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=False)
        
        tk.Label(row_frame, text=str(stolik), font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=8, anchor="center", relief="flat", bd=1, cursor="hand2").pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=False)
        tk.Label(row_frame, text=godzina, font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=10, anchor="center", relief="flat", bd=1, cursor="hand2").pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=False)
        tk.Label(row_frame, text=str(osoby), font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=8, anchor="center", relief="flat", bd=1, cursor="hand2").pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=False)
        tk.Label(row_frame, text=uwagi[:25] if uwagi else "-", font=("Segoe UI", 9), bg=bg_color, fg="#1C1E21", width=25, anchor="w", relief="flat", bd=1, cursor="hand2").pack(side=tk.LEFT, padx=1, pady=1, fill=tk.BOTH, expand=True)

        delete_func = create_delete_function(filename, numer)

        for widget in row_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: delete_func())
            def on_enter(event):
                event.widget.config(relief="raised")
            def on_leave(event):
                event.widget.config(relief="flat")
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    # Info
    info_label = tk.Label(okno, text="Kliknij na rezerwację aby ją usunąć", font=("Segoe UI", 10, "italic"), bg="#F0F2F5", fg="#666666")
    info_label.pack(pady=10)

    okno.mainloop()

def otworz_widok_dostepnosci_stolikow():
    """Wyświetla dostępność stolików na każdą godzinę"""
    okno = tk.Tk()
    okno.title("Dostępność Stolików")
    okno.geometry("1000x550")
    okno.config(bg="#F0F2F5")

    # Tytuł
    tk.Label(okno, text="Status Dostępności Stolików", font=("Segoe UI", 18, "bold"), bg="#F0F2F5", fg="#1C1E21").pack(pady=(15, 10))

    # Ramka do scrollowania
    canvas_frame = tk.Frame(okno, bg="#F0F2F5")
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Canvas z scrollbarem
    canvas = tk.Canvas(canvas_frame, bg="#F0F2F5", highlightthickness=0)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, bg="#F0F2F5")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    # Pobierz dane rezerwacji
    rezerwacje_dict = {}
    files = [f for f in os.listdir(REZERWACJE_DIR) if f.startswith("rezerwacja_") and f.endswith(".json")]
    
    for file in files:
        try:
            with open(os.path.join(REZERWACJE_DIR, file), 'r', encoding='utf-8') as f:
                rez = json.load(f)
                stolik = rez.get("stolik", 0)
                godzina = rez.get("godzina", "")
                imie = rez.get("imie_nazwisko", "Nieznany")
                if stolik not in rezerwacje_dict:
                    rezerwacje_dict[stolik] = {}
                rezerwacje_dict[stolik][godzina] = imie
        except:
            pass

    # Utwórz tabelę (grid) z nagłówkami godzin i rzędami dla stolików
    table_frame = tk.Frame(scrollable_frame, bg="#F0F2F5")
    table_frame.pack()

    # Nagłówek: pierwszy pusty / "Stolik"
    tk.Label(table_frame, text="Stolik", font=("Segoe UI", 10, "bold"), bg="#F0F2F5", fg="#1C1E21", width=12, anchor="w")\
        .grid(row=0, column=0, padx=2, pady=3)

    # Nagłówki godzin (kolumny)
    for col, h in enumerate(range(GODZINY_OTWARCIA[0], GODZINY_OTWARCIA[1]), start=1):
        tk.Label(table_frame, text=f"{h}:00", font=("Segoe UI", 9, "bold"), bg="#F0F2F5", fg="#1C1E21", width=10, anchor="center")\
            .grid(row=0, column=col, padx=2, pady=3)

    # Wiersze dla każdego stolika
    for row, stolik_num in enumerate(range(1, LICZBA_STOLIKOW + 1), start=1):
        tk.Label(table_frame, text=f"Stolik {stolik_num}", font=("Segoe UI", 10, "bold"), bg="#F0F2F5", fg="#1C1E21", width=12, anchor="w")\
            .grid(row=row, column=0, padx=2, pady=3)

        for col, h in enumerate(range(GODZINY_OTWARCIA[0], GODZINY_OTWARCIA[1]), start=1):
            godzina_str = f"{h}:00"
            if stolik_num in rezerwacje_dict and godzina_str in rezerwacje_dict[stolik_num]:
                imie = rezerwacje_dict[stolik_num][godzina_str]
                bg_color = "#E74C3C"
                fg_color = "white"
                text = "✓"
                tooltip = imie
            else:
                bg_color = "#2ECC71"
                fg_color = "white"
                text = "○"
                tooltip = "Dostępny"

            cell = tk.Label(table_frame, text=text, font=("Segoe UI", 11, "bold"), bg=bg_color, fg=fg_color, width=10, anchor="center", relief="solid", bd=1)
            cell.grid(row=row, column=col, padx=2, pady=3)

            def on_enter(event, tip=tooltip):
                event.widget.config(relief="raised")
            def on_leave(event):
                event.widget.config(relief="solid")
            cell.bind("<Enter>", on_enter)
            cell.bind("<Leave>", on_leave)

    # Legenda
    legend_frame = tk.Frame(okno, bg="#F0F2F5")
    legend_frame.pack(pady=10)

    tk.Label(legend_frame, text="○", font=("Segoe UI", 12, "bold"), bg="#2ECC71", fg="white", width=3, relief="solid", bd=1).pack(side=tk.LEFT, padx=5)
    tk.Label(legend_frame, text="Dostępny", font=("Segoe UI", 10), bg="#F0F2F5", fg="#1C1E21").pack(side=tk.LEFT, padx=5)

    tk.Label(legend_frame, text="✓", font=("Segoe UI", 12, "bold"), bg="#E74C3C", fg="white", width=3, relief="solid", bd=1).pack(side=tk.LEFT, padx=5)
    tk.Label(legend_frame, text="Zajęty", font=("Segoe UI", 10), bg="#F0F2F5", fg="#1C1E21").pack(side=tk.LEFT, padx=5)

    okno.mainloop()