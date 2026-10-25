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
  pku-wojewodztwa.json                  słownik: PKU → województwo (filtr Województwo na stronie działa wg PKU, nie wg dziennika)
  wolynskie/
    1925.json                           numery 5–12 (wydania wgrane przez użytkowniczkę, 37 wpisów)
    1926.json                           numery 1, 2 i 5 (jedyne dotąd wgrane, 32 wpisy)
    1927.json                           nr 1 (4 wpisy)
  nowogrodzkie/
    1925.json                           numery 5–12 (edykty PKU Słonim, 11 wpisów PKU Baranowicze i 1 PKU Mołodeczno, 169 wpisów)
    1926.json                           numery 1–11 (edykty PKU Słonim, 40 wpisów PKU Baranowicze i 7 PKU Mołodeczno, 324 wpisy)
  poleskie/
    1925.json                           numery 7–12 (edykty PKU Pińsk, Łuniniec, Brześć i Łuck, 99 wpisów)
    1926.json                           numery 1, 3–11 (edykty PKU Pińsk, Łuniniec, Brześć, Łuck i Kowel, 241 wpisów)
    1927.json                           nr 2 (1 wpis, PKU Kowel)
  krakowskie/
    1924.json                           nr 8 (2 wpisy, Referat Inwalidzki PKU Wadowice)
    1925.json                           numery 1, 2, 3, 4, 5, 7 (616 wpisów: PKU Biała-Bielsko, Nowy Sącz, Rzeszów, Tarnów, Kraków, Nowy Targ, Wadowice oraz 97 edyktów Sądu Okręgowego w Jaśle z nr 3, oznaczonych jako „brak PKU”)
    1926.json                           numery 1–5 (214 wpisy)
  lubelskie/
    1925.json                           numery 2, 4, 5, 6, 7, 8, 10, 11, 12, 13 (pierwsza tura, 220 wpisów: PKU Zamość, Biłgoraj, Chełm, Biała Podlaska, Puławy, Hrubieszów, Lublin, Siedlce, Łuków)
    1926.json                           numery 1–12 (235 wpisów: PKU Zamość, Biłgoraj, Chełm, Biała Podlaska, Puławy, Hrubieszów, Lublin, Siedlce, Łuków, Ostrów Mazowiecka)
  monitorpolski/
    1925.json                           Monitor Polski, numery 2, 6, 10, 12, 15, 16, 17, 18, 21, 22, 24, 27, 28, 29, 30, 32, 33, 34, 35, 36, 39, 40, 41, 43, 194, 199, 243, 256, 257, 266, 271, 278, 285, 291 (318 wpisów; edykty różnych PKU w całym kraju)
    1926.json                           Monitor Polski, numery 19, 44, 51, 63, 65, 74, 93, 117, 126, 141, 166, 173, 176, 177, 183, 207, 219, 239, 243, 264 (403 wpisy)
  lodzkie/
    1925.json                           tylko numery z edyktami PKU (22 z 26 opracowane)
    1926.json                           kompletny: wszystkie numery z edyktami PKU
docs/
  zestawienie-wydan-1925-1926.md        zestawienie wydań dzienników i Monitora Polskiego ze statusem opracowania
  nieczytelne-tarnopolskie-1925.md      miejsca, w których druk jest nieczytelny
  nieczytelne-tarnopolskie-1926.md
  nieczytelne-lwowskie-1925.md
  nieczytelne-lwowskie-1926.md
  nieczytelne-lodzkie-1925.md
  nieczytelne-lodzkie-1926.md
  nieczytelne-stanislawowskie-1925.md
  nieczytelne-stanislawowskie-1926.md
  nieczytelne-wolynskie-1926.md
  nieczytelne-poleskie-1925.md
  nieczytelne-poleskie-1926.md
  nieczytelne-krakowskie-1925.md
  nieczytelne-krakowskie-1926.md
  nieczytelne-lubelskie-1925.md
  nieczytelne-lubelskie-1926.md
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
- Dziennik Urzędowy Województwa Nowogródzkiego, rocznik 1925 – opracowane nr 5–12 (30 V – 31 XII 1925), skany w Jagiellońskiej Bibliotece Cyfrowej; numery 1–4 zostały przejrzane ręcznie przez autorkę i nie zawierają edyktów. Edykty Referatu Inwalidzkiego PKU Słonim (157 wpisów, o zasiłkach dla rodzin zaginionych żołnierzy armii rosyjskiej), PKU Baranowicze (11 wpisów w nr 11, str. 16–17, edykty o uznaniu za zaginionych) i PKU Mołodeczno w Wilejce (1 wpis, nr 12, str. 22). Pominięto ogłoszenia o zagubionych dokumentach. W nr 5 i 6 druk nie podaje liczby dziennika (L. dz.). Cechy druku zachowano bez poprawek, m.in. Kozak Michał, L. dz. »8273|35« (nr 8), Stećko Stefan »ur. w roku 1903« (nr 8), Sierbin Michał »ur. w 1785« (nr 10).
- Dziennik Urzędowy Województwa Nowogródzkiego, rocznik 1926 – opracowane nr 1–11 (31 I – 30 XII 1926), skany w Jagiellońskiej Bibliotece Cyfrowej; to numery z edyktami wskazane przez użytkowniczkę. Edykty Referatu Inwalidzkiego PKU Słonim (277 wpisów, o zasiłkach dla rodzin zaginionych żołnierzy armii rosyjskiej), PKU Baranowicze (40 wpisów, edykty o uznaniu za zaginionych) i PKU Mołodeczno w Wilejce (7 wpisów). Pominięto ogłoszenia o zagubionych dokumentach, a wspólną końcówkę edyktów („Wzywa się wszystkich, ktoby wiedział…”) pominięto w polu tekstu (w nr 1 druk jej nie podaje). W druku nr 1 sprostowanie redakcji (s. 39) poprawia wpisy Jermak Tomasz (ldz i baon), Gryn Dawid (wyznanie) i Korzeniewski Teodor (brak L. dz.); w polu uwaga zachowano zapis z druku.
- Dziennik Urzędowy Województwa Warszawskiego, rocznik 1925 – opracowane nr 1–8 i 10–14 (31 I – 31 XII 1925; nr 9 nie został dostarczony), skany w Jagiellońskiej Bibliotece Cyfrowej; wydania przejrzane ręcznie przez autorkę, wpisano tylko numery z edyktami. Edykty PKU Warszawa Powiat (66 wpisów), Płock (34), Kutno (18), Mińsk Mazowiecki (16), Pułtusk (15), Ciechanów (11), Modlin (9) i Łomża (1) o zaginionych żołnierzach armii rosyjskiej i polskiej. Pominięto komasacje gruntów, ogłoszenia stowarzyszeń, ogłoszenia o zgubionych dokumentach i komunikat policyjny; wspólną końcówkę zbiorczych list (nr 10–14) pominięto w polu tekstu.
- Dziennik Urzędowy Województwa Warszawskiego, rocznik 1926 – opracowane nr 2–11 (28 II – 30 XI 1926; nr 1 nie został dostarczony), skany w Jagiellońskiej Bibliotece Cyfrowej; wydania przejrzane ręcznie przez autorkę. Edykty PKU Warszawa Powiat (62 wpisy), Włocławek (25), Ciechanów (15), Modlin (13), Kutno (13), Pułtusk (12) i Płock (5) o zaginionych żołnierzach armii rosyjskiej, polskiej i niemieckiej. Dodatkowo 47 wpisów o osobach cywilnych (zaginieni, poszukiwani przez Starostwa, Policję, MSW i Wojewodę, listy gończe, odwołania poszukiwań; „brak PKU”), w tym wszystkie 5 z nr 11. Pominięto komasacje gruntów, ogłoszenia stowarzyszeń, sądowe i o zgubionych dokumentach; wspólną końcówkę list („UWAGA! Wzywa się wszystkich…”) pominięto w polu tekstu.
- Dziennik Urzędowy Województwa Wileńskiego, rocznik 1926 – opracowane nr 1, 2, 4, 5, 8, 9, 10 i 11-a (31 I – 31 X 1926), skany w Jagiellońskiej Bibliotece Cyfrowej; wydania przejrzane ręcznie przez autorkę, wpisano tylko numery z ogłoszeniami PKU (23 wpisy: PKU Wilno, Święciany, Mołodeczno w Wilejce). Pominięto komasacje gruntów, ogłoszenia sądowe i o zgubionych dokumentach.
- Dziennik Urzędowy Województwa Kieleckiego, rocznik 1925 – opracowane nr 2–12 (21 II – 28 XII 1925), skany w Jagiellońskiej Bibliotece Cyfrowej (111 wpisów: PKU Radom, Sosnowiec, Końskie, Częstochowa, Ostrowiec, Miechów, Pińczów). Pominięto komasacje gruntów, ogłoszenia stowarzyszeń i o zgubionych dokumentach.
- Dziennik Urzędowy Województwa Kieleckiego, rocznik 1926 – opracowane nr 2, 5, 7–13 (27 II – 30 XII 1926), skany w Jagiellońskiej Bibliotece Cyfrowej; to numery z edyktami wskazane przez użytkowniczkę (170 wpisów: PKU Radom, Kielce, Sosnowiec, Końskie, Pińczów, Częstochowa). Pominięto komasacje gruntów i ogłoszenia o zgubionych dokumentach.
- Dziennik Urzędowy Województwa Białostockiego, rocznik 1925 – opracowane nr 3, 4, 5, 8, 9, 10 i 11 (20 III – 16 XI 1925), skany w Podlaskiej Bibliotece Cyfrowej; to numery wskazane przez użytkowniczkę (20 wpisów: PKU Ostrów Łomżyński, Suwałki, Łomża, Grodno oraz tabele zaginionych żołnierzy w nr 8, 9 i 11). Pominięto zagubione dokumenty i pozostałe ogłoszenia.
- Dziennik Urzędowy Województwa Białostockiego, rocznik 1926 – opracowane nr 1, 7, 8, 9, 10, 11 i 12 (8 I – 1 XII 1926), skany w Podlaskiej Bibliotece Cyfrowej; to numery wskazane przez użytkowniczkę (58 wpisów: PKU Grodno, Łomża, Bielsk Podlaski, Suwałki, Ostrów Łomżyński, Sokółka i Ostrów Mazowiecka; nr 7 w formie tabeli). Pominięto komasacje, zagubione dokumenty i pozostałe ogłoszenia.
- Dziennik Urzędowy Województwa Poleskiego, rocznik V (1925) – opracowane nr 7–12 (1 VII – 1 XII 1925), skany w Jagiellońskiej Bibliotece Cyfrowej; to numery wskazane przez użytkowniczkę jako zawierające edykty, numery 1–6 nie zostały wgrane. Edykty PKU Pińsk, Łuniniec i Brześć nad Bugiem oraz PKU Łuck (4 wpisy, w filtrze Województwo trafiają do wołyńskiego). Pominięto ogłoszenia o zgubionych dokumentach, wykazy zabytków i listy poszukiwanych w sprawach karnych. Edykt o Chaimie Czyżu (nr 9, str. 9) wydrukowano dwukrotnie, w bazie jest raz.
- Dziennik Urzędowy Województwa Poleskiego, rocznik VI (1926) – opracowane nr 1, 3–11 (1 I – 15 XII 1926) oraz rocznik 1927 nr 2 (16 II 1927), skany w Jagiellońskiej Bibliotece Cyfrowej; nr 2 z 1926 i pozostałe numery nie zostały wgrane (wg użytkowniczki edykty są tylko w wybranych numerach). PKU Pińsk, Łuniniec i Brześć nad Bugiem oraz PKU Łuck (8 wpisów) i PKU Kowel (6 wpisów, w tym 1 z 1927), które w filtrze Województwo trafiają do wołyńskiego. Pominięto ogłoszenia o zgubionych dokumentach i komunikaty. Cechy druku zachowano bez poprawek, m.in. Nowak Dymitr »ur. w 1785« (nr 6), Stachiejko Samuel »23 sierpnia 1792« (nr 11), Hudyn Filip, L. dz. »177719/III« (nr 10), Bajko Grzegorz z dwiema różnymi datami urodzenia (nr 11).
- Dziennik Urzędowy Województwa Krakowskiego, rocznik V (1925) – opracowane nr 1, 2, 3, 4, 5 i 7 (1 II – 1 XI 1925), skany w Jagiellońskiej Bibliotece Cyfrowej; nr 3 (1 VI 1925) zawiera wyłącznie edykty Sądu Okręgowego w Jaśle (Oddz. IV, sygn. „T. IV.”, 97 wpisów, str. 10–14), które w bazie mają wartość „brak PKU” (przypisane do województwa krakowskiego). Edykty PKU Biała-Bielsko, Nowy Sącz, Tarnów, Nowy Targ, Wadowice, Kraków-Miasto i Kraków-Powiat oraz PKU Rzeszów (w filtrze Województwo trafiają do lwowskiego). Pominięto pozostałe edykty sądowe o uznaniu za zmarłych, ogłoszenia o zgubionych dokumentach i komunikaty. Skan nr 2 jest miejscami uszkodzony (docs/nieczytelne-krakowskie-1925.md).
- Dziennik Urzędowy Województwa Krakowskiego, rocznik VI (1926) – opracowane nr 1–5 (15 II – 20 X 1926), skany w JBC; zasady jak wyżej. Rocznik IV (1924) – tylko nr 8 (25 X 1924), 2 edykty Referatu Inwalidzkiego PKU Wadowice.
- Dziennik Urzędowy Województwa Lubelskiego, rocznik 1925 – opracowane nr 2, 4, 5, 6, 7, 8, 10, 11, 12 i 13 (11 II – 29 XII 1925), skany w Jagiellońskiej Bibliotece Cyfrowej (pierwsza tura; numery 1, 3 i 9 nie zostały dostarczone). Edykty PKU Zamość, Biłgoraj, Chełm, Biała Podlaska, Puławy, Hrubieszów, Lublin, Siedlce i Łuków. Pominięto edykty sądowe o uznaniu za zmarłych, ogłoszenia o hipotekach i zgubionych dokumentach oraz komunikaty (np. komunikat DOK II w Lublinie o Płaczkowskim w nr 10 oraz o Krasnodębskim w nr 4). Edykty nr 2, 4 i 5 częściowo się powtarzają (przedruki), każdy druk jest osobnym wpisem. Zbiorcze edykty PKU Hrubieszów (kilka osób w jednym druku) rozbito na osobne wpisy. Miejsca nieczytelne lub z widoczną omyłką druku: docs/nieczytelne-lubelskie-1925.md.
- Dziennik Urzędowy Województwa Lubelskiego, rocznik 1926 – opracowane nr 1–12 (26 I – 30 XI 1926), skany w Jagiellońskiej Bibliotece Cyfrowej. Edykty PKU Zamość, Biłgoraj, Chełm, Biała Podlaska, Puławy, Hrubieszów, Lublin, Siedlce, Łuków oraz Referatu Inwalidzkiego PKU Ostrów Mazowiecka (poszukiwani z powiatów Węgrów i Sokołów). Pominięto edykty sądowe o uznaniu za zmarłych, ogłoszenia o hipotekach i zgubionych dokumentach, ogłoszenia o scaleniu gruntów oraz komunikaty. Część edyktów powtarza się w kolejnych numerach (przedruki), każdy druk jest osobnym wpisem. Zbiorcze edykty (kilka osób w jednym druku: PKU Hrubieszów, Zamość, Radzyń/Łuków, Puławy, Biłgoraj, Chełm, Lublin) rozbito na osobne wpisy. Miejsca nieczytelne lub z widoczną omyłką druku: docs/nieczytelne-lubelskie-1926.md.
- Monitor Polski 1925, nr 2, 6, 10, 12, 15, 16, 17, 18, 21, 22, 24, 27, 28, 29, 30, 32, 33, 34, 35, 36, 39, 40, 41, 43, 194, 199, 243, 256, 257, 266, 271, 278, 285, 291 (3 I – 16 XII 1925), skany z monitorpolski.gov.pl. Rubryka „Edykty o zaginięciu i poszukiwaniu osób wojskowych”; pominięto kopię „Obwieszczeń sądowych”, zgubione dokumenty i inne ogłoszenia. W nr 291 edykt PKU Kołomyja nie ma w druku wymienionych osób, więc nie dał wpisów.
- Monitor Polski 1926, nr 19, 44, 51, 63, 65, 74, 93, 117, 126, 141 (25 I – 24 VI 1926), skany z monitorpolski.gov.pl. Rubryka „Edykty o zaginięciu i poszukiwaniu osób wojskowych”; pominięto ogłoszenia sądowe i zgubione dokumenty. Nr 65 nie zawiera edyktów PKU, więc nie dał wpisów. Dwa wpisy mają adnotację o nieczytelnym druku (docs/nieczytelne-monitorpolski-1926.md).

## Listy według województw (dla wyszukiwarek)

`python3 tools/build_wojewodztwa.py` generuje statyczne strony `wojewodztwo/<slug>/index.html` (tabela: nazwisko, imię, rok ur., miejscowość, przycisk „Przeczytaj edykt" → `index.html?id=<id wpisu>`), przegląd `wojewodztwo/index.html`, `sitemap.xml` oraz blok linków w `index.html` (między `<!--WOJ-START-->` a `<!--WOJ-END-->`). Uruchom skrypt po każdym dopisaniu rocznika i wypchnij zmienione pliki. Sitemap zgłoś w Google Search Console (`sitemap.xml`).
