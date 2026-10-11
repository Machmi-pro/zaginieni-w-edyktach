# Zaginieni i poszukiwani w edyktach

Wyszukiwarka osób z edyktów Powiatowych Komend Uzupełnień, ogłaszanych w dziennikach urzędowych województw II Rzeczypospolitej. Strona jest statyczna (GitHub Pages), bez serwera i bez bazy: dane leżą w plikach JSON, a wyszukiwanie działa w przeglądarce.

## Struktura

```
index.html                              strona: wygląd i wyszukiwarka w jednym pliku
favicon.svg                             ikona strony
img/                                    ikony PNG i grafika do udostępniania (og.png)
data/
  manifest.json                         spis źródeł i roczników (strona czyta go jako pierwszy)
  tarnopolskie/
    1925.json                           jeden rocznik: wydania + wpisy
    1926.json
    1927.json                           przejrzany, bez edyktów
  lwowskie/
    1925.json                           numery 3–12
    1926.json                           numery 1–12
  stanislawowskie/
    1925.json                           numery 3, 6–12 (z edyktami PKU)
    1926.json                           numery 1–7 (komplet wydań dostępnych w JBC, wychodzi co drugi miesiąc)
    1927.json                           nr 1 (jedyny dotąd wgrany numer, 3 edykty)
  wolynskie/
    1925.json                           numery 5–12 (wydania wgrane przez użytkowniczkę, 37 wpisów)
    1926.json                           numery 1, 2 i 5 (jedyne dotąd wgrane, 32 wpisy)
    1927.json                           nr 1 (4 wpisy)
  lodzkie/
    1925.json                           tylko numery z edyktami PKU (22 z 26 opracowane)
    1926.json                           kompletny: wszystkie numery z edyktami PKU
docs/
  nieczytelne-tarnopolskie-1925.md      miejsca, w których druk jest nieczytelny
  nieczytelne-tarnopolskie-1926.md
  nieczytelne-lwowskie-1925.md
  nieczytelne-lwowskie-1926.md
  nieczytelne-lodzkie-1925.md
  nieczytelne-lodzkie-1926.md
  nieczytelne-stanislawowskie-1925.md
  nieczytelne-stanislawowskie-1926.md
  nieczytelne-wolynskie-1926.md
README.md
```

Zasada: **jeden plik na rocznik, jeden folder na województwo.**

## Jak dodać rocznik

1. Wgraj plik `data/<województwo>/<rok>.json`.
2. Dopisz rocznik w `data/manifest.json`:

```json
{"rok": 1926, "plik": "data/tarnopolskie/1926.json", "wpisy": 0}
```

Strony nie trzeba zmieniać. Filtr „Rocznik” pojawi się sam, gdy roczników będzie więcej niż jeden.

## Jak dodać województwo

1. Załóż folder `data/<województwo>/` i wgraj pliki roczników.
2. Dopisz źródło w `data/manifest.json`:

```json
{"id": "lwowskie", "wojewodztwo": "lwowskie", "roczniki": [
  {"rok": 1925, "plik": "data/lwowskie/1925.json", "wpisy": 0}
]}
```

Filtr „Województwo” pojawi się sam, gdy województw będzie więcej niż jedno.

## Format pliku rocznika

Nagłówek:

| Pole | Znaczenie |
|---|---|
| `zrodlo` | identyfikator źródła, taki jak nazwa folderu |
| `wojewodztwo` | nazwa pokazywana w filtrze |
| `rok` | rocznik |
| `dziennik`, `dziennik_skrot` | tytuł dziennika w tym roczniku (tytuł może się zmieniać między rocznikami) |

`wydania` – po jednym wierszu na numer: `nr`, `data` (RRRR-MM-DD), `link` (stały adres PDF w bibliotece cyfrowej), `wpisy` (liczba osób).

`wpisy` – po jednym wierszu na osobę:

| Pole | Znaczenie |
|---|---|
| `id` | `<źródło>-<rok>-<nr>-<kolejność w numerze>` |
| `nr`, `strona` | numer wydania i strona; z nich powstaje link do skanu |
| `oglasza` | komenda ogłaszająca, np. `PKU Tarnopol` |
| `ldz` | liczba dziennika z edyktu |
| `nazwisko`, `imie` | osoba poszukiwana |
| `data_ur`, `rok_ur` | data w zapisie `3 X 1885`, `X 1885` albo `1885`; rok osobno jako liczba |
| `miejsce_ur`, `powiat_ur` | miejsce urodzenia |
| `miejsce_zam`, `powiat_zam` | miejsce zamieszkania |
| `ojciec`, `matka` | rodzice, matka z nazwiskiem panieńskim, jeśli jest w edykcie |
| `wyznanie`, `zawod`, `zona` | jeśli są w edykcie |
| `jednostka` | pułk lub oddział |
| `poszukuje` | wnioskodawca: żona, matka, ojciec itd. |
| `tekst` | dosłowna treść wpisu w pisowni druku |
| `uwaga` | tylko gdy druk jest nieczytelny |

Puste pole oznacza, że edykt tej informacji nie podaje.

Link do skanu strona składa sama: `link` wydania + `#page=` + `strona`. Wpis, którego numeru nie ma w `wydania`, nie jest pokazywany, bo nie miałby źródła.

## Zasady przepisywania

- Źródłem jest dziennik. Pola idą za drukiem, także tam, gdzie druk wygląda na pomyłkę.
- Zmieniany jest tylko przypadek (mianownik: „w Budzanowie” → Budzanów) i pisownia typu Marja → Maria.
- `tekst` zachowuje pisownię druku bez zmian.
- `uwaga` pojawia się wyłącznie przy druku wyblakłym, nieostrym lub uszkodzonym.

## Uruchomienie

Na GitHubie: Settings → Pages → Deploy from a branch → `main`, folder `/ (root)`.

Lokalnie strona wymaga serwera (otwarta wprost z dysku nie wczyta danych), np. `python3 -m http.server` w folderze repozytorium.

## Źródła

- Dziennik Urzędowy Województwa Tarnopolskiego, roczniki 1925–1926 – skany w Jagiellońskiej Bibliotece Cyfrowej.
- Rocznik 1927 tego dziennika przejrzano w całości: nie zawiera edyktów o zaginionych, więc plik `1927.json` ma tylko listę wydań.
- Dziennik Urzędowy Województwa Lwowskiego, rocznik 1925, numery 3–12 – skany w Jagiellońskiej Bibliotece Cyfrowej. Numery 1–2 nie zostały jeszcze opracowane.
- Dziennik Urzędowy Województwa Łódzkiego, rocznik 1925 – tylko numery z edyktami PKU, skany w Wojewódzkiej Bibliotece Publicznej w Łodzi (nr 39 – Jagiellońska Biblioteka Cyfrowa). Opracowane: nr 8, 14, 16, 18, 19, 24, 26, 27, 28, 31, 33, 34, 36, 39, 41, 42, 44, 45, 46, 49, 50, 51. Nr 35, 43, 47, 48 nie zostały wgrane (według wskazania powtarzają edykty z opracowanych numerów).
- Dziennik Urzędowy Województwa Łódzkiego, rocznik 1926 – opracowane wszystkie numery z edyktami PKU (nr 1–4, 6, 9–17, 19–39, 41, 43–50, 52), skany w Jagiellońskiej Bibliotece Cyfrowej.
- Dziennik Urzędowy Województwa Stanisławowskiego, rocznik 1925 – opracowane wszystkie numery z edyktami/ogłoszeniami PKU (nr 3, 6–12), skany w Jagiellońskiej Bibliotece Cyfrowej. Pominięto cywilne ogłoszenia o poszukiwaniu dzieci i zwłok (nr 7, 10, 11, 12).
- Dziennik Urzędowy Województwa Stanisławowskiego, rocznik 1926 – opracowane wszystkie wydania, jakie były dostępne (nr 1–7, wychodzi co drugi miesiąc), skany w Jagiellońskiej Bibliotece Cyfrowej.
- Dziennik Urzędowy Województwa Stanisławowskiego, rocznik 1927 – dotąd tylko nr 1 (1 I 1927, 3 edykty PKU Kałusz na str. 8), skan w Jagiellońskiej Bibliotece Cyfrowej.
- Dziennik Urzędowy Województwa Wołyńskiego, rocznik V (1925) – opracowane nr 5–12 (5 VI 1925 – 15 I 1926), skany w Jagiellońskiej Bibliotece Cyfrowej. Pominięto ogłoszenia o zgubionych dokumentach i wykazy unieważnionych kart ewidencyjnych.
- Dziennik Urzędowy Województwa Wołyńskiego, rocznik VI (1926) – opracowane nr 1 (15 V 1926), nr 2 (1 VI 1926) i nr 5 (10 I 1927, za listopad i grudzień 1926), oraz rocznik VII (1927) – nr 1 (18 I 1927). Są to numery, które zawierają edykty; pozostałe numery nie zostały dotąd wgrane. Pominięto ogłoszenia o zgubionych dokumentach i wykazy unieważnionych kart ewidencyjnych.
