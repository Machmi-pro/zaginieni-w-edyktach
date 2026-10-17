#!/usr/bin/env python3
"""Generuje statyczne strony list osób według województw (dla wyszukiwarek i do przeglądania).

Uruchomienie z korzenia repo:  python3 tools/build_wojewodztwa.py

Tworzy:
  wojewodztwo/index.html            przegląd województw
  wojewodztwo/<slug>/index.html     lista osób z filtrem (tabela: nazwisko, imię, rok ur., miejscowość, link do edyktu)
  wojewodztwo/style.css             wspólne style
  sitemap.xml
oraz odświeża blok linków w index.html między znacznikami <!--WOJ-START--> i <!--WOJ-END-->.

Województwo wpisu wynika z PKU (data/pku-wojewodztwa.json), tak samo jak filtr na stronie głównej.
Wpisy bez wydania (czyli bez linku do skanu) są pomijane, tak samo jak na stronie głównej.
"""
import datetime
import html
import json
import pathlib
import re
import unicodedata
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://machmi-pro.github.io/zaginieni-w-edyktach/"
TODAY = datetime.date.today().isoformat()
PL = "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
SLUG_SPECIAL = {"warszawskie i m. st. Warszawa": "warszawskie"}
MIES = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def norm(s):
    """Ta sama normalizacja co w index.html (bez polskich znaków, Marja = Maria)."""
    s = (s or "").lower().replace("ł", "l")
    s = unicodedata.normalize("NFD", s)
    s = re.sub("[̀-ͯ]", "", s)
    s = re.sub(r"j(?=[aeiou])", "i", s)
    s = s.replace("ii", "i")
    return s.strip()


def pku_key(s):
    return re.sub(r"[^a-z0-9]", "", norm(s))


def pl_key(s):
    return [PL.index(c) if c in PL else len(PL) + ord(c) for c in (s or "").lower()]


def slugify(name):
    if name in SLUG_SPECIAL:
        return SLUG_SPECIAL[name]
    s = unicodedata.normalize("NFD", name.lower().replace("ł", "l"))
    s = re.sub("[̀-ͯ]", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def esc(s):
    return html.escape(str(s), quote=True)


def plural_osob(n):
    return "osoba" if n == 1 else ("osoby" if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else "osób")


def load():
    man = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
    dz = json.loads((ROOT / "data/pku-wojewodztwa.json").read_text(encoding="utf-8"))
    pmap = {}
    for w, lst in dz["wojewodztwa"].items():
        for p in lst:
            pmap[pku_key(p)] = w
    for a, p in dz.get("aliasy", {}).items():
        pmap[pku_key(a)] = pmap.get(pku_key(p))
    recs = []
    for z in man["zrodla"]:
        for y in z["roczniki"]:
            d = json.loads((ROOT / y["plik"]).read_text(encoding="utf-8"))
            wyd = {w["nr"]: w for w in d["wydania"]}
            for r in d["wpisy"]:
                if r["nr"] not in wyd:
                    continue
                r["_rok"] = d["rok"]
                r["_zrodlo"] = z["id"]
                r["_pku"] = re.sub(r"^PKU\s+", "", r["oglasza"])
                if r["oglasza"] == "brak PKU":  # komunikat spoza PKU: województwo wg źródła
                    r["_woj"] = next((w for w in dz["wojewodztwa"] if slugify(w).startswith(slugify(d["wojewodztwo"]))), "(nieprzypisane)")
                else:
                    r["_woj"] = pmap.get(pku_key(r["_pku"])) or "(nieprzypisane)"
                recs.append(r)
    return recs


def hits(path):
    """Licznik wejść (hits.sh), osobny dla każdej strony, w tym samym stylu co na stronie głównej."""
    src = ("https://hits.sh/machmi-pro.github.io/zaginieni-w-edyktach/" + path +
           ".svg?style=flat&amp;label=wy%C5%9Bwietle%C5%84&amp;color=55388a")
    return f'<p><img alt="Liczba wyświetleń" src="{src}" style="border:0;vertical-align:middle;"></p>'


def woj_label(w):
    return "województwo " + w


def place_cell(r):
    zam = ", ".join(x for x in [r.get("miejsce_zam"), r.get("powiat_zam") and "pow. " + r["powiat_zam"]] if x)
    ur = ", ".join(x for x in [r.get("miejsce_ur"), r.get("powiat_ur") and "pow. " + r["powiat_ur"]] if x)
    main = zam or ur
    out = esc(main) if main else '<span class="none">brak w edykcie</span>'
    if zam and ur and ur != zam:
        out += f'<small>ur. w {esc(ur)}</small>'
    return out


def row(r):
    search = norm(" ".join([r["nazwisko"], r["imie"], str(r.get("data_ur") or ""), str(r.get("rok_ur") or ""),
                            r.get("miejsce_zam", ""), r.get("powiat_zam", ""),
                            r.get("miejsce_ur", ""), r.get("powiat_ur", "")]))
    ur = esc(r["data_ur"]) if r.get("data_ur") else "—"
    return (f'<tr data-s="{esc(search)}"><td class="n">{esc(r["nazwisko"])}{' <span class="cyw">cywil</span>' if r.get("cywil") else ""}</td><td class="i">{esc(r["imie"])}</td>'
            f'<td class="u">{ur}</td><td class="m">{place_cell(r)}</td>'
            f'<td class="b"><a class="btn" href="../../index.html?id={esc(r["id"])}">Przeczytaj edykt</a></td></tr>')


CSS = """:root{--bg:#eceeed;--surface:#fafbfa;--ink:#1b2024;--muted:#5c666c;--line:#cfd5d3;--stamp:#55388a;--stamp-soft:#e9e3f3;
--f-head:"Archivo Narrow","Arial Narrow",Arial,sans-serif;--f-body:"Archivo",system-ui,Arial,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#14181a;--surface:#1c2225;--ink:#e6eae8;--muted:#98a3a7;--line:#333c40;--stamp:#bda8ea;--stamp-soft:#2c2540;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:15px;line-height:1.45}
.wrap{max-width:900px;margin:0 auto;padding:20px 16px 48px;display:flex;flex-direction:column;gap:18px}
.crumb{font-family:var(--f-head);font-weight:600;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.crumb a,.nav a,footer a{color:var(--stamp)}
h1{font-family:var(--f-head);font-weight:700;font-size:32px;line-height:1.08;letter-spacing:.02em;text-transform:uppercase;margin:4px 0 8px;text-wrap:balance}
h2{font-family:var(--f-head);font-size:18px;letter-spacing:.04em;text-transform:uppercase;margin:0 0 8px}
p{margin:0 0 8px;max-width:68ch}
.lead{font-size:16px}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px 12px}
.stat b{display:block;font-family:var(--f-head);font-size:26px;color:var(--stamp);font-variant-numeric:tabular-nums}
.stat span{font-size:13px;color:var(--muted)}
.box{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:14px}
label{display:flex;flex-direction:column;gap:6px;font-family:var(--f-head);font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
input[type=search]{font:inherit;font-family:var(--f-body);font-size:16px;letter-spacing:0;text-transform:none;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:3px;padding:12px;width:100%}
input:focus-visible,a:focus-visible{outline:2px solid var(--stamp);outline-offset:2px}
.count{font-family:var(--f-head);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:13px;color:var(--muted);margin:10px 0 0}
table{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line)}
th{font-family:var(--f-head);font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:10px;border-bottom:2px solid var(--line)}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
td.n{font-weight:700}
td.u{white-space:nowrap;font-variant-numeric:tabular-nums}
td small{display:block;color:var(--muted);font-size:12.5px}
.none{color:var(--muted)}
.btn{display:inline-block;font-family:var(--f-head);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--surface);background:var(--stamp);border-radius:4px;padding:10px 14px;text-decoration:none;white-space:nowrap}
.sr{position:absolute;left:-9999px}
.empty{padding:20px 14px;color:var(--muted)}
.nav ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}
.nav li a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:12px;text-decoration:none;font-weight:600}
.nav li a span{display:block;font-weight:400;font-size:13px;color:var(--muted)}
footer{border-top:1px solid var(--line);padding-top:14px;color:var(--muted);font-size:13.5px}
@media (max-width:640px){
 h1{font-size:26px}
 .stats{grid-template-columns:1fr 1fr 1fr}.stat b{font-size:21px}
 thead{display:none}
 table,tbody{display:block;border:0;background:none}
 tr{display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-areas:"n i" "u m" "b b";gap:3px 8px;align-items:baseline;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:12px;margin-bottom:8px}
 tr[hidden]{display:none}
 td{display:block;padding:0;border:0}
 td.n{grid-area:n;font-size:17px}td.i{grid-area:i;font-size:17px}
 td.u{grid-area:u;color:var(--muted)}td.m{grid-area:m;min-width:0}
 td.b{grid-area:b;margin-top:8px}
 .btn{padding:12px 12px;white-space:normal;text-align:center;overflow-wrap:normal;word-break:normal;display:block;font-size:13px}
}
.cyw{font-size:11px;font-weight:600;letter-spacing:.05em;color:#0b6b73;border:1px solid #0b6b73;border-radius:3px;padding:1px 5px;margin-left:6px;white-space:nowrap}
@media (prefers-color-scheme:dark){.cyw{color:#5fc3cc;border-color:#5fc3cc}}
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700'
         '&family=Archivo+Narrow:wght@500;600;700&display=swap">')

FILTER_JS = """<script>
const norm=s=>(s||"").toLowerCase().replace(/ł/g,"l").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/j(?=[aeiou])/g,"i").replace(/ii/g,"i").trim();
const rows=[...document.querySelectorAll("#t tbody tr")],q=document.getElementById("q"),c=document.getElementById("c"),e=document.getElementById("e"),full=document.getElementById("full");
function f(){const t=norm(q.value).split(/\\s+/).filter(Boolean);let n=0;
 for(const r of rows){const ok=t.every(x=>r.dataset.s.includes(x));r.hidden=!ok;if(ok)n++;}
 c.textContent=t.length?`Znaleziono: ${n} z ${rows.length}`:`Wszystkie wpisy: ${rows.length}`;
 e.hidden=n>0;
 const p=q.value.trim().split(/\\s+/);full.href="../../index.html?n="+encodeURIComponent(p[0]||"")+(p[1]?"&i="+encodeURIComponent(p[1]):"");}
q.addEventListener("input",f);q.closest("form").addEventListener("submit",ev=>ev.preventDefault());f();
</script>"""


def page_woj(w, rs, all_wojs):
    slug = slugify(w)
    n = len(rs)
    years = sorted({r["_rok"] for r in rs})
    yr_txt = f"{years[0]}–{years[-1]}" if len(years) > 1 else str(years[0])
    by_year = Counter(r["_rok"] for r in rs)
    pkus = sorted({r["_pku"] for r in rs}, key=pl_key)
    srcs = Counter("Monitor Polski" if r["_zrodlo"] == "monitorpolski" else "dziennik urzędowy" for r in rs)
    label = woj_label(w)
    title = f"Zaginieni po I wojnie światowej – {label}, edykty PKU {yr_txt}"
    desc = (f"Lista {n} osób poszukiwanych w edyktach Powiatowych Komend Uzupełnień ({label}, {yr_txt}): "
            f"zaginieni żołnierze po I wojnie światowej – nazwisko, imię, rok urodzenia, miejscowość, odnośnik do skanu.")
    url = f"{BASE}wojewodztwo/{slug}/"
    ld = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": f"Zaginieni i poszukiwani w edyktach PKU – {label}",
        "description": desc, "url": url, "inLanguage": "pl",
        "temporalCoverage": f"{years[0]}/{years[-1]}" if len(years) > 1 else str(years[0]),
        "spatialCoverage": label,
        "isPartOf": {"@type": "WebSite", "name": "Zaginieni i poszukiwani w edyktach", "url": BASE},
    }
    year_li = " · ".join(f"{y}: {by_year[y]}" for y in years)
    src_txt = ", ".join(f"{k} ({v})" for k, v in srcs.most_common())
    body = "\n".join(row(r) for r in sorted(rs, key=lambda r: (pl_key(r["nazwisko"]), pl_key(r["imie"]), r["_rok"], r["nr"])))
    others = "".join(f'<li><a href="../{slugify(o)}/">{esc(o)}<span>{cnt} {plural_osob(cnt)}</span></a></li>'
                     for o, cnt in all_wojs if o != w)
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#55388a">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}img/og.png">
{FONTS}
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<div class="crumb"><a href="../../">Zaginieni i poszukiwani w edyktach</a> · <a href="../">Województwa</a></div>
<header>
<h1>Zaginieni po I wojnie światowej – {esc(label)}</h1>
<p class="lead">Lista osób poszukiwanych w edyktach Powiatowych Komend Uzupełnień ogłaszanych w dziennikach urzędowych II Rzeczypospolitej: zaginionych żołnierzy, o których losach rodziny nie miały wiadomości, a także komunikatów o zaginionych i poszukiwanych osobach cywilnych (oznaczonych etykietą „cywil”). Przy każdej osobie jest przycisk prowadzący do pełnej karty wpisu z treścią edyktu i odnośnikiem do skanu.</p>
</header>
<section aria-label="Podsumowanie">
<div class="stats">
<div class="stat"><b>{n}</b><span>{plural_osob(n)} w bazie</span></div>
<div class="stat"><b>{esc(yr_txt)}</b><span>{'roczniki' if len(years) > 1 else 'rocznik'}</span></div>
<div class="stat"><b>{len(pkus)}</b><span>{'komend PKU' if len(pkus) != 1 else 'komenda PKU'}</span></div>
</div>
<p class="count" style="text-transform:none;letter-spacing:0;font-weight:400;font-family:inherit;margin-top:10px">Według roczników: {esc(year_li)}. Źródła: {esc(src_txt)}. Komendy: {esc(", ".join(pkus))}. Baza jest uzupełniana o kolejne wydania, więc lista nie jest jeszcze kompletna.</p>
</section>
<form class="box" role="search">
<label for="q">Filtruj listę: nazwisko, imię, rok urodzenia lub miejscowość<input type="search" id="q" placeholder="np. Kowalski Jan 1885 Brzeżany" autocomplete="off"></label>
<p class="count" id="c" aria-live="polite"></p>
</form>
<table id="t">
<thead><tr><th>Nazwisko</th><th>Imię</th><th>Ur.</th><th>Miejscowość</th><th><span class="sr">Edykt</span></th></tr></thead>
<tbody>
{body}
</tbody>
</table>
<div class="empty box" id="e" hidden>Brak takich osób na tej liście. <a id="full" href="../../index.html">Szukaj w całej bazie</a> (wszystkie województwa, także wśród rodziców, żon i wnioskodawców).</div>
<nav class="nav" aria-label="Inne województwa"><h2>Inne województwa</h2><ul>{others}</ul></nav>
<footer><p>Źródło: skany dzienników urzędowych (Jagiellońska Biblioteka Cyfrowa, Wojewódzka Biblioteka Publiczna w Łodzi) i „Monitora Polskiego”. Pisownia za drukiem, z ujednoliconym przypadkiem. Województwo wynika z komendy PKU ogłaszającej edykt. <a href="../../">Strona główna z wyszukiwarką</a>.</p>
{hits("wojewodztwo/"+slug)}</footer>
</div>
{FILTER_JS}
</body>
</html>
"""


def page_index(all_wojs):
    total = sum(c for _, c in all_wojs)
    title = "Zaginieni po I wojnie światowej – lista osób z edyktów PKU według województw"
    desc = (f"Przeglądaj {total} osób poszukiwanych w edyktach Powiatowych Komend Uzupełnień po I wojnie światowej, "
            "według województw II Rzeczypospolitej: zaginieni żołnierze, nazwisko, imię, rok urodzenia, miejscowość.")
    url = f"{BASE}wojewodztwo/"
    items = "".join(f'<li><a href="{slugify(w)}/">{esc(woj_label(w))}<span>{c} {plural_osob(c)}</span></a></li>'
                    for w, c in all_wojs)
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#55388a">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}img/og.png">
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
<div class="crumb"><a href="../">Zaginieni i poszukiwani w edyktach</a></div>
<header>
<h1>Zaginieni po I wojnie światowej – według województw</h1>
<p class="lead">Edykty Powiatowych Komend Uzupełnień z dzienników urzędowych II Rzeczypospolitej. Wybierz województwo, aby zobaczyć listę osób (nazwisko, imię, rok urodzenia, miejscowość) z odnośnikiem do pełnego wpisu i skanu.</p>
</header>
<nav class="nav" aria-label="Województwa"><ul>{items}</ul></nav>
<footer><p><a href="../">Strona główna z wyszukiwarką</a></p>
{hits("wojewodztwo")}</footer>
</div>
</body>
</html>
"""


def update_index_links(all_wojs):
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    lis = "".join(f'<li><a href="wojewodztwo/{slugify(w)}/">{esc(woj_label(w))} ({c})</a></li>' for w, c in all_wojs)
    block = ('<!--WOJ-START-->\n  <nav class="browse" aria-label="Listy według województw"><h2>Przeglądaj według województw</h2>'
             f'<ul>{lis}</ul></nav>\n  <!--WOJ-END-->')
    if "<!--WOJ-START-->" in s:
        s = re.sub(r"<!--WOJ-START-->.*?<!--WOJ-END-->", lambda m: block, s, flags=re.S)
    else:
        s = s.replace("  <footer>", f"  {block}\n\n  <footer>", 1)
    p.write_text(s, encoding="utf-8")


def sitemap(all_wojs):
    urls = [BASE, BASE + "wojewodztwo/"] + [f"{BASE}wojewodztwo/{slugify(w)}/" for w, _ in all_wojs]
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        x.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    x.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(x), encoding="utf-8")


def main():
    recs = load()
    by = defaultdict(list)
    for r in recs:
        by[r["_woj"]].append(r)
    unassigned = by.pop("(nieprzypisane)", [])
    all_wojs = sorted(((w, len(rs)) for w, rs in by.items()), key=lambda x: pl_key(x[0]))
    out = ROOT / "wojewodztwo"
    out.mkdir(exist_ok=True)
    (out / "style.css").write_text(CSS, encoding="utf-8")
    (out / "index.html").write_text(page_index(all_wojs), encoding="utf-8")
    for w, rs in by.items():
        d = out / slugify(w)
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page_woj(w, rs, all_wojs), encoding="utf-8")
    update_index_links(all_wojs)
    sitemap(all_wojs)
    print(f"Wpisów: {len(recs)}; stron województw: {len(by)}; nieprzypisane PKU: {len(unassigned)}")
    for w, c in all_wojs:
        print(f"  {w}: {c}")
    if unassigned:
        print("UWAGA – PKU bez województwa w słowniku:", sorted({r["_pku"] for r in unassigned}))


if __name__ == "__main__":
    main()
