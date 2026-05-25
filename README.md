# 🍽️ System Zarządzania Stolikami
 
Desktopowa aplikacja do zarządzania rezerwacjami stolików w restauracji, napisana w języku Python z wykorzystaniem biblioteki tkinter.
 
---
 
## Spis treści
 
- [Dokumentacja użytkownika](#dokumentacja-użytkownika)
  - [Uruchomienie aplikacji](#uruchomienie-aplikacji)
  - [Panel sterowania](#panel-sterowania)
  - [Wykonaj rezerwację](#wykonaj-rezerwację)
  - [Anuluj rezerwację](#anuluj-rezerwację)
  - [Lista gości](#lista-gości)
  - [Cennik](#cennik)
- [Dokumentacja techniczna](#dokumentacja-techniczna)
  - [Wymagania](#wymagania)
  - [Struktura projektu](#struktura-projektu)
  - [Opis modułów](#opis-modułów)
  - [Funkcje publiczne](#funkcje-publiczne)
  - [Format danych — JSON](#format-danych--json)
  - [Konfiguracja stałych](#konfiguracja-stałych)
  - [Znane ograniczenia i TODO](#znane-ograniczenia-i-todo)
---
 
## Dokumentacja użytkownika
 
### Uruchomienie aplikacji
 
1. Upewnij się, że masz zainstalowanego **Pythona 3.8+**.
2. Sklonuj repozytorium lub pobierz pliki projektu.
3. Przejdź do katalogu projektu i uruchom plik główny:
```bash
python Panel-wyboru.py
```
 
> Przy pierwszym uruchomieniu aplikacja automatycznie tworzy folder `rezerwacje/`, w którym przechowywane są wszystkie dane.
 
---
 
### Panel sterowania
 
Po uruchomieniu aplikacji pojawia się główne okno **„Restauracja – Panel Sterowania"** (1080×720 px), wyśrodkowane na ekranie. Zawiera cztery przyciski:
 
| Przycisk | Kolor | Działanie |
|---|---|---|
| **Wykonaj Rezerwacje** | Niebieski | Otwiera formularz nowej rezerwacji |
| **Anuluj Rezerwację** | Pomarańczowy | Otwiera okno anulowania rezerwacji |
| **Lista Gości** | Niebieski | Otwiera widok dostępności wszystkich stolików |
| **Wyjście** | Czerwony | Zamknięcie aplikacji |
 
Wszystkie przyciski mają efekt podświetlenia po najechaniu kursorem.
 
---
 
### Wykonaj rezerwację
 
Kliknięcie przycisku **„Wykonaj Rezerwacje"** otwiera formularz rezerwacji. Należy wypełnić następujące pola:
 
- **Imię i nazwisko** – pełne imię i nazwisko gościa (wymagane)
- **Liczba osób** – liczba całkowita większa od 0 (wymagane)
- **Stolik** – wybór z listy numerów 1–6 (wymagane)
- **Godzina** – wybór z listy dostępnych godzin dla wybranego stolika (format `HH:00`)
- **Uwagi** – opcjonalne uwagi do rezerwacji (dodają 20 PLN do ceny)
Po wyborze stolika i godziny aplikacja automatycznie aktualizuje wyświetlaną **cenę rezerwacji**. Na liście godzin widoczne są tylko te, które są jeszcze wolne dla wybranego stolika.
 
Kliknięcie **„Zatwierdź"** zapisuje rezerwację i wyświetla potwierdzenie z numerem rezerwacji i ceną.
 
> ⚠️ Aplikacja nie pozwoli zarezerwować stolika zajętego w danej godzinie.
 
---
 
### Anuluj rezerwację
 
Kliknięcie przycisku **„Anuluj Rezerwację"** otwiera okno wyszukiwania rezerwacji. Aby anulować rezerwację:
 
1. Wpisz **imię i nazwisko** gościa (dokładnie tak, jak przy rezerwacji — wyszukiwanie jest nierozróżniające wielkości liter).
2. Kliknij **„Szukaj"**.
3. Na liście pojawią się wszystkie znalezione rezerwacje w formacie:
   ```
   Rez. #001 | Stolik 3 | 18:00 | 4 osób | 50 PLN
   ```
4. Zaznacz rezerwację, którą chcesz usunąć, i kliknij **„Anuluj Rezerwację"**.
Po potwierdzeniu rezerwacja jest trwale usuwana z systemu.
 
---
 
### Lista gości
 
Kliknięcie **„Lista Gości"** otwiera widok **„Dostępność Stolików"** — tabelę o wymiarach:
 
- **Wiersze** – stoliki 1–6
- **Kolumny** – godziny od 11:00 do 22:00
Każda komórka wskazuje status stolika w danej godzinie:
 
| Symbol | Kolor | Znaczenie |
|---|---|---|
| `○` | Zielony | Stolik dostępny |
| `✓` | Czerwony | Stolik zajęty |
 
Widok posiada poziomy pasek przewijania. Najechanie kursorem na komórkę daje wizualny efekt (raised border).
 
---
 
### Cennik
 
| Godzina | Cena bazowa | Dodatek za uwagi | Razem |
|---|---|---|---|
| 11:00 – 20:00 | 50 PLN | +20 PLN | 50–70 PLN |
| 21:00 – 22:00 | 100 PLN | +20 PLN | 100–120 PLN |
 
---
 
## Dokumentacja techniczna
 
### Wymagania
 
- **Python** 3.8 lub nowszy
- Biblioteki standardowe (brak zewnętrznych zależności):
  - `tkinter` – interfejs graficzny
  - `json` – zapis/odczyt rezerwacji
  - `os` – operacje na plikach
  - `datetime` – znacznik czasu rezerwacji
> Biblioteka `tkinter` jest wbudowana w standardową dystrybucję Pythona dla Windows i macOS. Na Linuxie może wymagać instalacji: `sudo apt-get install python3-tk`.
 
---
 
### Struktura projektu
 
```
fluffy-giggle2/
│
├── Panel-wyboru.py        # Punkt wejścia — główne okno aplikacji
├── Podaj_Dane_rez.py      # Logika rezerwacji, anulowania i widoku dostępności
├── .gitignore
│
└── rezerwacje/            # Tworzony automatycznie przy pierwszym uruchomieniu
    ├── rezerwacja_001.json
    ├── rezerwacja_002.json
    └── ...
```
 
---
 
### Opis modułów
 
#### `Panel-wyboru.py`
 
Punkt wejścia aplikacji. Odpowiada za:
 
- Inicjalizację i konfigurację głównego okna `tk.Tk` (1080×720 px, wyśrodkowane, nieresizowalne).
- Renderowanie czterech przycisków nawigacyjnych z efektami hover.
- Funkcję `otwórz_mape()` – prototypowy widok mapy sali z 6 stolikiami kolorowanymi na zielono (wolne, nieparzyste) lub czerwono (zajęte, parzyste). Widok ten jest w fazie developmentu i nie korzysta jeszcze z rzeczywistych danych.
- Import i wywołanie funkcji z modułu `Podaj_Dane_rez`.
#### `Podaj_Dane_rez.py`
 
Moduł zawierający całą logikę biznesową i trzy główne okna aplikacji. Definiuje stałe konfiguracyjne oraz sześć funkcji publicznych.
 
---
 
### Funkcje publiczne
 
#### `get_next_rezerwacja_number() → int`
Skanuje folder `rezerwacje/` i zwraca kolejny numer rezerwacji (max istniejący + 1). Przy pustym folderze zwraca `1`.
 
---
 
#### `get_dostepne_stoliki(godzina_str: str) → list[int]`
Zwraca listę numerów stolików (1–6), które **nie mają** jeszcze rezerwacji na podaną godzinę.
 
- Parametr: `godzina_str` w formacie `"HH:00"` (np. `"18:00"`).
- Odczytuje wszystkie pliki JSON z folderu `rezerwacje/` i filtruje po polu `godzina`.
---
 
#### `get_dostepne_godziny(stolik_str: str) → list[str]`
Zwraca listę dostępnych godzin (format `"HH:00"`) dla podanego stolika.
 
- Parametr: `stolik_str` – numer stolika jako string (np. `"3"`).
- Przeszukuje JSON-y i wyklucza godziny już zarezerwowane dla danego stolika.
---
 
#### `oblicz_cene(godzina_str: str, uwagi_str: str) → int`
Oblicza cenę rezerwacji w PLN.
 
- Cena bazowa: `50 PLN` (godziny 11–20), `100 PLN` (godziny 21–22).
- Jeśli pole uwag jest niepuste: `+20 PLN`.
---
 
#### `otworz_okno_rezerwacji()`
Tworzy nowe okno `tk.Tk` (450×600 px) z formularzem rezerwacji. Po zatwierdzeniu:
 
1. Waliduje dane (imię, liczba osób > 0, wybór stolika i godziny, dostępność).
2. Oblicza cenę.
3. Serializuje dane do JSON i zapisuje plik `rezerwacje/rezerwacja_NNN.json`.
4. Wyświetla `messagebox` z potwierdzeniem i zamyka okno.
---
 
#### `otworz_okno_anulowania_rezerwacji()`
Tworzy okno (550×400 px) z wyszukiwarką rezerwacji po imieniu i nazwwisku. Wyszukiwanie jest **case-insensitive**. Po wyborze pozycji z listy i kliknięciu „Anuluj" plik JSON jest trwale usuwany z dysku (`os.remove`).
 
---
 
#### `otworz_widok_dostepnosci_stolikow()`
Tworzy okno (1000×550 px) z tabelą `tkinter.Grid`. Wczytuje wszystkie rezerwacje do słownika `{stolik: {godzina: imię}}` i renderuje komórki z kolorowaniem: zielony = wolny, czerwony = zajęty. Widok posiada poziomy `ttk.Scrollbar`.
 
---
 
### Format danych — JSON
 
Każda rezerwacja zapisywana jest jako osobny plik `rezerwacja_NNN.json` (NNN = numer z wiodącymi zerami, np. `001`):
 
```json
{
    "numer": 1,
    "imie_nazwisko": "Jan Kowalski",
    "liczba_osob": 4,
    "stolik": 3,
    "godzina": "18:00",
    "uwagi": "alergia na gluten",
    "cena_pln": 70,
    "data_rezerwacji": "2026-05-25T19:30:00.123456"
}
```
 
| Pole | Typ | Opis |
|---|---|---|
| `numer` | `int` | Unikalny numer porządkowy rezerwacji |
| `imie_nazwisko` | `str` | Pełne imię i nazwisko gościa |
| `liczba_osob` | `int` | Liczba osób przy stoliku |
| `stolik` | `int` | Numer stolika (1–6) |
| `godzina` | `str` | Godzina w formacie `HH:00` |
| `uwagi` | `str` | Opcjonalne uwagi (może być pusty string) |
| `cena_pln` | `int` | Cena rezerwacji w PLN |
| `data_rezerwacji` | `str` | Timestamp ISO 8601 momentu złożenia rezerwacji |
 
---
 
### Konfiguracja stałych
 
Wszystkie parametry biznesowe zdefiniowane są na początku pliku `Podaj_Dane_rez.py`:
 
```python
REZERWACJE_DIR    = "rezerwacje"  # Ścieżka do folderu z danymi
LICZBA_STOLIKOW   = 6             # Liczba stolików w restauracji
GODZINY_OTWARCIA  = (11, 23)      # Zakres godzin (od, do — wyłącznie)
CENA_PODSTAWOWA   = 50            # PLN — godziny standardowe
CENA_NOCNA        = 100           # PLN — godziny 21:00–22:00
DODATEK_ZA_UWAGI  = 20            # PLN — doliczany gdy pole uwag niepuste
```
 
Aby zmienić np. liczbę stolików lub godziny otwarcia, wystarczy edytować te wartości — reszta aplikacji dostosuje się automatycznie.
 
---
 
### Znane ograniczenia i TODO
 
- **Brak bazy danych** – dane przechowywane są jako pliki JSON. Przy dużej liczbie rezerwacji operacje wyszukiwania mogą być wolne.
- **Brak obsługi daty** – system nie rozróżnia rezerwacji na różne dni; wszystkie rezerwacje traktowane są jako obowiązujące.
- **Mapa sali** (`otwórz_mape` w `Panel-wyboru.py`) – funkcja w trakcie implementacji (komentarz `#MIEJSCE NA KOD OSKARA`); status stolików jest generowany statycznie (parzyste = zajęte), a nie na podstawie rzeczywistych danych.
- **Brak edycji rezerwacji** – zmiana danych wymaga anulowania i ponownego złożenia rezerwacji.
- **Wielokrotne okna `tk.Tk`** – każda funkcja tworzy nowe `tk.Tk()` zamiast `tk.Toplevel`. Może to powodować problemy przy intensywnym użytkowaniu; rekomendowane jest refaktorowanie do jednego okna głównego z widokami `Toplevel`.
---
 
*Projekt tworzony zespołowo — autorzy: Michał, Filip, Oskar.*
 
