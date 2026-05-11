import tkinter as tk
#=============================================
#--- Wymiary i Nazwa Panelu sterowania ---
#=============================================
#KOD MICHAŁA
root = tk.Tk()
root.title("Restauracja - Panel Sterowania")
root.geometry("1080x720")
root.resizable(False,False)
szerokość_ekranu = root.winfo_screenwidth()
wysokość_ekranu = root.winfo_screenheight()
x = (szerokość_ekranu // 2) - 540
y = (wysokość_ekranu // 2) - 360
root.geometry(f"1080x720+{x}+{y}")
root.config(bg="#F0F2F5")
#=============================================
#--- TYTUŁ PANELU ---
#=============================================
#KOD MICHAŁA
tytuł = tk.Label(root,
                 text="System Zarządzania Stolikami",
                 font=("Segoe UI", 32 , "bold"),
                 bg="#F0F2F5" ,
                 fg="#1C1E21")
tytuł.pack(pady=(80,40))
#=============================================
#--- FUNKCJA OTWIERANIA MAPY SALI ---
#=============================================
#MIEJSCE NA KOD OSKARA
def funkcja_rezerwacji(n):
    print(f"Kliknięto stolik nr {n}")
    ## --- OSKAR: TUTAJ WPISZ SWÓJ KOD ---
    # Tutaj stwórz okno (Toplevel), Entry do wpisania imienia itp.
    # Użyj zmiennej 'n', żeby wiedzieć który to stolik.


#===========================================================================================================
#MIEJSCE NA KOD FILIPA
def otworz_liste_gosci():
    # --- FILIP: TUTAJ WPISZ SWÓJ KOD ---
    # Tutaj stwórz okno, które wczyta dane z pliku .txt i je wyświetli.
    print("Filip otwiera listę gości...")
#===========================================================================================================
#KOD MICHAŁA
def otwórz_mape():
    mapa_okno = tk.Toplevel(root)
    mapa_okno.title("Mapa Sali - Status Stolików")
    mapa_okno.geometry("800x600")
    mapa_okno.config(bg="white")

    tk.Label(mapa_okno, text="WYBIERZ STOLIK" , font=("Segoe UI", 20 , "bold"), bg="white").pack(pady=10)

    for i in range(6):
        numer_stolika = i + 1

        if numer_stolika % 2 == 0:
            kolor = "#e74c3c"
            text_statusu = f"Stolik {numer_stolika}\n(ZAJĘTY)"

        else:
            kolor = "#2ecc71"
            text_statusu = f"Stolik {numer_stolika}\n(WOLNY)"

        przycisk_stolika = tk.Button(mapa_okno,
                                     text=text_statusu,
                                     bg=kolor,
                                     fg="white",
                                     width=15,
                                     height=5,
                                     bd=0,
                                     highlightthickness=0,
                                     cursor="hand2",
                                     command=lambda n=numer_stolika: funkcja_rezerwacji(n))

        kolumna = i % 3
        rząd = i // 3

        przycisk_stolika.place(x=100 + (kolumna * 200) , y=100 + (rząd * 150))

#=================================================================================
#--- PRZYCISK REZERWACJI (MAPA SALI) ---
#=================================================================================
#KOD MICHAŁA
przycisk_rezerwacje = tk.Button(root,
                               text="Otwórz Mapę Sali",
                               font=("Segoe UI", 14 , "bold"),
                               bg="#007BFF",
                               fg="white",
                               width=25,
                               height=2,
                               bd=0,
                               cursor="hand2",
                               activebackground="#0056b3",
                                command=otwórz_mape)
przycisk_rezerwacje.pack(pady=10)
#=======================================================================
#--- PODŚWIETLENIE PRZYCISKU REZERWACJI (MAPA SALI) ---
#=======================================================================
#KOD MICHAŁA
def na_wejscie_przycisku_rezerwacji(e):
    przycisk_rezerwacje["bg"] = "#0056b3"

def na_wyjscie_przycisku_rezerwacji(e):
    przycisk_rezerwacje["bg"] = "#007BFF"

przycisk_rezerwacje.bind("<Enter>", na_wejscie_przycisku_rezerwacji)
przycisk_rezerwacje.bind("<Leave>", na_wyjscie_przycisku_rezerwacji)
#=======================================================================
#--- PRZYCISK LISTA GOŚCI ---
#=======================================================================
#KOD MICHAŁA
przycisk_lista_gości = tk.Button(root,
                                 text="Lista Gości",
                                 font=("Segoe UI", 14 , "bold"),
                                 bg="#007BFF",
                                 fg="white",
                                 width=25,
                                 height=2,
                                 bd=0,
                                 cursor="hand2",
                                 activebackground="#0056b3",
                                 command=otworz_liste_gosci())
przycisk_lista_gości.pack(pady=10)
#==================================================================
#--- PODSWIETLENIE PRZYCISKU LISTA GOŚCI ---
#==================================================================
#KOD MICHAŁA
def na_wejscie_listy_gości(e):
    przycisk_lista_gości["bg"] = "#0056b3"

def na_wyjscie_listy_gości(e):
    przycisk_lista_gości["bg"] = "#007BFF"

przycisk_lista_gości.bind("<Enter>", na_wejscie_listy_gości)
przycisk_lista_gości.bind("<Leave>", na_wyjscie_listy_gości)
#===================================================================
#--- PRZYCISK WYJŚCIA ---
#===================================================================
#KOD MICHAŁA
przycisk_wyjscia = tk.Button(root,
                             text="Wyjście",
                             font=("Segoe UI", 14 , "bold"),
                             bg="#E41E3F",
                             fg="white",
                             width=25,
                             height=2,
                             bd=0,
                             highlightthickness=0,
                             cursor="hand2",
                             activebackground="#B91833",
                             command=root.destroy)
przycisk_wyjscia.pack(pady=10)
#========================================
#--- PODŚWIETLENIE PRZYCISKU WYJŚCIA ---
#========================================
#KOD MICHAŁA
def na_wejscie_przycisku_wyjscia(e):
    przycisk_wyjscia["bg"] = "#B91833"

def na_wyjscie_przycisku_wyjscia(e):
    przycisk_wyjscia["bg"] = "#E41E3F"

przycisk_wyjscia.bind("<Enter>", na_wejscie_przycisku_wyjscia)
przycisk_wyjscia.bind("<Leave>", na_wyjscie_przycisku_wyjscia)


root.mainloop()