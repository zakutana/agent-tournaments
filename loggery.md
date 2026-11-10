# Teplotní dataloggery do termosky 0,5 l – ověření v českých e-shopech

Datum ověření: 2026-11-10. Prohlížeč: Playwright / Chromium (cs-CZ), JavaScript vykreslen. Screenshoty: `screenshots/` (název = doména + začátek cesty; `*_kosik_2ks` = košík se 2 ks, `*_parametry` = rozbalené parametry).
Nic jsem neobjednával, nevyplňoval formuláře ani neposílal e-mail/osobní údaje. Do košíku jsem jen vložil 2 ks (košík je jen v mé relaci).
„nenalezeno" = na stránce jsem to nenašel. Citace jsou doslovné ze stránek. Údaje označené (výpočet) jsou moje aritmetika, ne ze stránky.

## 1. Kandidáti, které prošly sítem (rozlišení ≤ 0,1 °C, přesnost ≤ ±0,5 °C v použitelném rozsahu)

| Odkaz | Model | Cena za kus (s DPH) | Rozlišení | Přesnost | Interval | Paměť | Rozměr | Software / export | Baterie | Skladem (2 ks v košíku) | Poznámky |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Voltworld](https://www.voltworld.cz/dataloggery/voltcraft-teplotni-datalogger--datalogger-vzdusne-vlhkosti-teplota--vlhkost-vzduchu-30-do--60-c-0-do-100-rf-funkce-pdf/) | **Voltcraft DL-210TH** (kód produktu 1435091, „Typ (výrobce): DL-210TH") | **1 649 Kč** (1 363 Kč bez DPH) | „Rozlišení teploty: 0.1 °C" | „Přesnost měření teploty: 0.5 °C" (rozsah platnosti nenalezeno) | „Interval měření: 1 min. - 24 hod." | „Počet míst v paměti (naměřené hodnoty): 20010" | „(d x š x v) 19 x 37 x 86 mm" | „přiloženého softwaru Voltsoft nebo browseru"; „Automatické vypracování zpráv ve formátu PDF"; CSV: nenalezeno; samostatné stažení SW: nenalezeno | „Lithiová baterie (CR2450)", „Životnost baterie: 1 rok"; výměnnost: nenalezeno (stránka píše „Zabudovaná knoflíková baterie") | „Skladem"; **2 ks v košíku: „1 649 Kč / ks … 3 298 Kč"** | rozsah „-30 do +60 °C"; měří i vlhkost; „Odolný proti prachu a vodě (IP65)"; start: „až 13 různých startovacích režimů … start po stisknutí tlačítka" |
| [SmartElektro](https://www.smartelektro.cz/merice-teploty-a-vlhkosti/datalogger-uni-t-ut330c-usb/) (také [AtosElektro](https://shop.atoselektro.cz/datalogger-teplomer-uni-t-ut330c-usb_d110896.html) 1 890 Kč, [Svářečky-obchod](https://www.svarecky-obchod.cz/93687-datalogger-uni-t-ut330c-usb) 1 852 Kč) | **UNI-T UT330C** (teplota + vlhkost + tlak) | **1 631 Kč** (1 348 Kč bez DPH) | „Rozlišení: 0,1°C" | „± 0,5°C (0°C ~ 40°C)"; „±1°C (-30°C ~ 0°C, 40°C ~ 70°C)" | **nenalezeno** | „Možno uložit až 60000 hodnot" | „Rozměry: 122x30x24 mm" | „Software k analýze naměřených hodnot ZDARMA", v balení „CD se softwarem"; výrobce (meters.uni-trend.com): „PC software", „Trend capture to BMP/CSV/TXT files", odkaz „Click here for product software"; USB | „Napájení: 3,6V/1/2 AA lithiová baterie", „vydrží mnoho měsíců"; výměnnost: nenalezeno | „skladem"; **2 ks v košíku: „1 631 Kč / ks … 3 262 Kč"** | rozsah „-40°C ~ 80°C"; „IP67"; hmotnost 52 g; start: nenalezeno |
| [Revizeshop](https://www.revizeshop.cz/Testo-174T) (také [Reviznipristroje](https://www.reviznipristroje.cz/teplota-a-vlhkost/4115-testo-174-t-mini-zaznamnik-teploty-s-usb-c-a-softwarem-pro-pc.html) 2 432 Kč, „Skladem do 3 pracovních dnů") | **Testo 174T – verze s USB-C** („Miniaturní záznamník teploty s USB-C a softwarem pro PC") | **2 251 Kč** (1 860 Kč bez DPH) | „Rozlišení: 0,1 °C" (Reviznipristroje) | „Přesnost: ±0,5 °C (-30 až +70 °C)" | „Interval měření: 1 min až 24 h" (**pod 1 min nelze**) | „Paměť: 16 000 naměřených hodnot" | „Rozměry: 60 × 38 × 18,5 mm" | „Software ComSoft Basic – k dispozici ke stažení zdarma"; „Profesionální software s funkcí exportu do Excelu"; CSV: nenalezeno; Windows/Mac: nenalezeno; v balení „kabelu pro přenos dat USB 2.0" | „2× lithiová knoflíková baterie (CR 2032)", „Životnost baterie: 500 dní (při intervalu 15 min. a teplotě +25 °C)"; „zálohování dat … při její výměně" | „Skladem"; **2 ks v košíku: „CELKEM s DPH 4 501 Kč"** | rozsah „-30 až +70 °C"; skutečné stažení SW jsem neověřil (testo.com vrací HTTP 429 „Vercel Security Checkpoint") |
| [Promertech](https://promertech.cz/testo-174t-datalogger-teploty) / [Gastro-bazar](https://www.gastro-bazar.eu/testo-174-t-datalogger-teploty/) | **Testo 174T – klasická verze** | Promertech **1 887,6 Kč**; Gastro-bazar **1 209 Kč** | „Rozlišení 0,1 °C" (Promertech) | „Přesnost ±0,5 °C (-30 … +70 °C)" (Promertech) | nenalezeno na těchto stránkách (viz Revizeshop: 1 min–24 h) | „Paměť 16.000 Naměřených hodnot" | „Rozměry 60 x 38 x 18,5 mm" | „software Basic zdarma ke stažení"; **„K naprogramování a vyčtení dataloggeru dat potřebujete rozhraní USB, které není součástí dodávky"** (Gastro-bazar) | „2 lithiové baterie (CR2032)", „provoz z baterií cca 500 dní" | Promertech „Skladem" + „Pokud objednáte větší množství, než máme skladem, odešleme objednávku do 14 dní"; **2 ks: 3 775,2 Kč**. Gastro-bazar „Skladem : Ihned k Odeslání (2 ks)"; **2 ks: „1 998 Kč" bez DPH, „Cena vč. DPH: 2 417,58 Kč"** | Bez dokupu USB rozhraní (cena rozhraní: nenalezeno na těchto stránkách; Promertech nabízí „Testo 174T sada … 3 875 Kč", stránku jsem neotevřel) logger nevyčtete. Proto je výhodnější USB-C verze z řádku výše |

## 2. Částečně vyhovující

| Odkaz | Model | Cena za kus | Rozlišení | Přesnost | Interval | Paměť | Rozměr | Software / export | Baterie | Skladem | Poznámky |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Garni-meteo.cz](https://www.garni-meteo.cz/usb-datalogger-pro-mereni-teploty-a-relativni-vlhkosti-gar-175.html) | **GARNI GAR 175** | **2 130 Kč** (1 760 Kč bez DPH) | „0,1°C" | **„-10°C až +40°C ±1°C"**; „-40°C až -10°C a +40°C až +70°C ±1,5°C" – **nesplňuje ±0,5 °C** | „od 2 sekund do 30 sekund po jedné sekundě, dále 1, 5, 15, 30 minut …" (**jediný, který zvládne 10–30 s**) | „paměť na 32 000 dat (16 000 pro teplotu a 16 000 pro relativní vlhkost)" | „Celkové rozměry: 101 x 25 x 23 mm" (netfoto.cz; na Garni-meteo.cz rozměr nenalezen) | „software TempRH Datalogger V2.6"; „data ve formě tabulky ve formátu *.csv"; „Ke stažení: Program pro Windows"; „pracuje pod operačním systémem Windows 7, 8, 10 a 11" (Mac: nenalezeno); „možnost odloženého zahájení měření" | „baterie 3,6 V, lithiová (1/2 AA)"; výměnnost: nenalezeno (Epřístroje prodává náhradní lithiové 1/2 AA) | „můžete mít zítra"; **2 ks v košíku: „4 260 Kč", doprava zdarma** | rozsah „-40°C až +70°C"; měří i vlhkost; jediný s ověřeným CSV a odkazem na stažení SW přímo na stránce |

## 3. Vyřazené / nenalezené

| Co | Důvod (citace) |
|---|---|
| Lascar EL-USB-1 ([Epřístroje](https://www.epristroje.cz/el-usb-1-usb-datalogger-teploty-35-az--80-c-pamet-na-16-000-hodnot/)) | „Rozlišení: 0.5°C" → vyřazeno (horší než 0,1 °C) |
| Voltcraft DL-121TH | Hledání na Voltworld: žádná shoda; Conrad.cz za captchou → **nenalezeno** v otevřeném CZ obchodě |
| Elitech RC-5 | Žádný český e-shop jsem nenašel → **nenalezeno** |
| iButton DS1922 | TME detail (`tme.eu/cz/details/…`) vrací HTTP 403 „Okamžik…" (Cloudflare) → **nelze ověřit**; český prodejce nenalezen |
| Testo 174T Sada (s rozhraním) | Jen ve výpisu Promertech (3 875 Kč), stránku jsem neotevřel |
| UNI-T A57 BT, Voltcraft DL-240K, TFA LOG200 TC | Bluetooth, resp. vnější sonda na kabelu → mimo zadání |
| GME CEM DT-174B | Dříve ve výpisu GME „Skladem v e-shopu 1 ks" (907,50 Kč) → pro 2 stejné kusy nestačí; parametry neověřeny |
| Conrad.cz, Alza, Heureka, Mall (allegro), RS CZ, TME detail, Testo.com | Cloudflare/Akamai/429 → **nelze ověřit** (captchy jsem neobcházel) |

## 4. Doručení do ČR a B2C

- Voltworld: v pokladně „Země doručení: Česká republika", „PPL na výdejní místo 99 Kč" (ověřeno dříve na téže pokladně u K202); obchodní podmínky řeší spotřebitele.
- Promertech: „Doručení do: Česko", „Zásilkovna – výdejní místo 99 Kč", „PPL Standard 110 Kč"; obchodní podmínky § 1751 OZ, „Toto právo náleží výhradně spotřebiteli".
- Gastro-bazar: v košíku „Ve které zemi nakupujete? Česká republika (CZK)".
- Garni-meteo: „můžete mít zítra - u vás nebo na 3500+ odběrných místech", „Máte dopravu zdarma!"; B2B je samostatný „B2B e-shop".
- SmartElektro, Revizeshop: v košíku „Dopravu máte zdarma!", resp. „PPL - Professional Parcel Logistic"; výslovné „ČR" jsem u nich v textu nenašel → **nenalezeno**.

## 5. Výběr: 3 nejlepší

**Hlavní otázka: splňuje alespoň jeden 0,1 °C a ±0,5 °C?** Ano, všichni tři níže.

1. **Voltcraft DL-210TH (Voltworld, 1 649 Kč/ks, 3 298 Kč za 2 ks)** – splňuje 0,1 °C, ±0,5 °C, rozsah -30…+60 °C, paměť 20 010, skladem, 2 ks v košíku. Chybí: interval pod 1 min (minimum 1 min – požadavek „nebo 1 min" splněn, 10–30 s ne), CSV a samostatné stažení SW nenalezeno, výměna baterie nenalezena, přesnost bez uvedeného rozsahu.
2. **UNI-T UT330C (SmartElektro, 1 631 Kč/ks, 3 262 Kč za 2 ks)** – splňuje 0,1 °C, paměť 60 000, výrobce uvádí export CSV a software zdarma, z trojice nejmenší průřez. Chybí: interval záznamu nenalezen, přesnost ±0,5 °C jen v 0–40 °C (mimo to ±1 °C), výměna baterie nenalezena, start měření nenalezen.
3. **Testo 174T s USB-C (Revizeshop, 2 251 Kč/ks, 4 501 Kč za 2 ks)** – ±0,5 °C v celém rozsahu -30…+70 °C, 0,1 °C, 16 000 hodnot, výměnná baterie (zálohování při výměně), kabel USB v balení, export do Excelu. Chybí: interval pod 1 min, CSV nenalezeno, skutečné stažení SW neověřeno, nejdražší.

Pokud potřebujete interval 10–30 s: z ověřených jen **GARNI GAR 175** (2 130 Kč/ks), ale přesnost je ±1 °C, tedy nesplňuje ±0,5 °C; pro rozdíl desetin °C mezi dvěma kusy stejného modelu je to nejbližší.

## 6. Průchod hrdlem ~4 cm (výpočet, ne ze stránky)

Pokud je hrdlo kruhové o průměru 40 mm, musí úhlopříčka příčného řezu loggeru být menší: DL-210TH 19×37 mm → 41,6 mm; Testo 174T 38×18,5 mm → 42,3 mm; UT330C 30×24 mm → 38,4 mm; GAR 175 25×23 mm → 34 mm. Tedy **UT330C a GAR 175 projdou, DL-210TH a Testo 174T nejspíš ne**, pokud je hrdlo opravdu jen 40 mm. Změřte své hrdlo před nákupem.

## 7. Poznámky

- Zboží.cz (srovnávač) jsem použil jen k nalezení obchodů; všechny údaje výše jsou z otevřených stránek obchodů nebo výrobce.
- Skladové zásoby: u Voltworld, SmartElektro, Revizeshop a Garni-meteo je jen „Skladem" bez počtu; 2 ks se do košíku vešly bez hlášení. Počet kusů uvádí pouze Gastro-bazar („2 ks").
