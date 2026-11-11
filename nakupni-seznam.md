# Finální nákupní seznam – experiment se 2 termoskami (aktualizováno 2026-11-11)

Cíl: zjistit, jestli se v jedné ze dvou termosek zvedla teplota o ~0,1 °C. Rozhoduje hlavně **rozlišení** loggeru (musí být jemnější než hledaná změna) a **stabilita**, ne rozsah.

> **Oprava předchozí verze:** původní seznam s Comet U0121 (rozlišení 0,1 °C) není nejlepší. Při systematickém průchodu všech 57 dataloggerů teploty na Epřístrojích má rozlišení 0,01 °C jediný (Lascar EL-WiFi-TH+, ale ten měří 82 × 70 × 36 mm a je WiFi). Až širší hledání našlo Testo 176 T2 s rozlišením 0,01 °C a sondami Pt100.

## A) Doporučeno pro co nejpřesnější experiment (ověřeno 2026-11-11)

| # | Co | Obchod / odkaz | Ks | Cena za kus | Celkem | Dostupnost |
|---|---|---|---|---|---|---|
| 1 | Testo 176 T2 – záznamník, 2 vstupy pro Pt100 (0572 1762) | [Kubošek](https://shop.kubousek.cz/testo-merici-pristroje_c516937968780731/zaznamniky-s-usb-pripojenim_c647831392092682/zaznamnik-teploty-testo-176-t2-2-kanalovy-s-konektory-pro-velmi-presne-externi-sondy-pt100-0572-1762_p50843) | 1 | 11 290 Kč bez DPH | v košíku s DPH za vše z Kubouška: **22 833 Kč** | „Termín dodání: 1-2 týdny" |
| 2 | Testo laboratorní sonda Pt100, skleněné pouzdro (0609 7072), kabel 1,5 m | [Kubošek](https://shop.kubousek.cz/testo-merici-pristroje_c516937968780731/sondy_c566750999478301/laboratorni-sonda-se-sklenenou-ochranou-odolna-proti-agres.latkam-pt-100-0609-7072_p83343) | 2 | 3 790 Kč bez DPH | (součást 22 833 Kč) | „Termín dodání: 1-2 týdny" |
| 3 | Kabel USB A – mini USB 1 m (WG 11118) – k loggeru není v balení | [Datart](https://www.datart.cz/kabel-wg-usb-mini-usb-1m-11118-cerny.html) | 1 | 149 Kč | 149 Kč | „IHNED K ODESLÁNÍ" |
| 4 | Termoska Lock&lock LHC3220RBR, nerez 500 ml | [Datart](https://www.datart.cz/termoska-lock-lock-lhc3220rbr-cervena.html) | 2 | 279 Kč | 558 Kč | „Ihned k odeslání" (ověřeno 2026-11-09) |

**Celkem 23 540 Kč** (Kubošek 22 833 Kč + 149 Kč + 558 Kč), doprava není započtena. Košík na Kubošku s loggerem a 2 sondami ověřen (screenshot `screenshots/kubousek_176t2_sada_kosik.png`: „Celkem bez DPH 18 870", „Celkem k úhradě 22 833").

### Parametry (doslovně)
- **Testo 176 T2** (Kubošek / datasheet Testo): „Měřicí rozsah -100 do +400 °C", „Přesnost ±0.2 °C (-100 do +200 °C) ±1 Digit", **„Rozlišení 0.01 °C"**, „Rychlost měření 1 s - 24 h", „Pamět 2,000,000 měření hodnot", „Kanály 2 externí", „mini USB, slot pro SD kartu", „103 x 63 x 33 mm", „Životnost baterie 8 let (interval měření 15 min., +25 °C)", software testo ComSoft Basic. „Výstupní protokol z výroby*" – „nejedná se o kalibrační list".
- **Sonda 0609 7072** (Kubošek): „Přesnost Třída A (-50 do +300 °C)", „Průměr sondy 6 mm", „Délka trubice sondy 200 mm", „Délka kabelu 1,500", „Doba odezvy 45 s", Pt100, rozsah -50 až +400 °C.

### Co NENÍ ověřeno
- **Kompatibilita sondy 0609 7072 s Testem 176 T2:** výslovně ji uvádějí jen třetí strany (RS Components: „For Use With testo 176 T2"; katalogy faust.ch, hermeslab.sk), od Testa mi stránka nešla otevřít (HTTP 429). Kubošek píše jen, že lze připojit „dvě sondy Pt100 … z našeho sortimentu sond". **Před objednávkou si kompatibilitu potvrďte u Kubouška.**
- Numerická tolerance sondy třídy A (±°C) na stránce není; výsledná přesnost celé sestavy tedy není zaručena číslem.
- Mobilní aplikace: nenalezeno (jen mini USB a SD karta, PC software).
- Kabel WG 11118 je popsán jako „pro fotoaparát, MP3 či externí disky" – že přenáší data do Testo softwaru, výslovně není.
- Průchod 6mm skleněné sondy a kabelu pod víčkem termosky a těsnost: neověřeno (u obou termosek stejně). Skleněné pouzdro je křehké.
- Kubošek: v patičce „Obchodní podmínky B2B" i „Obchodní podmínky B2C", výslovné potvrzení prodeje soukromým osobám v košíku jsem nenašel.

## B) Ještě přesnější, ale s podmínkami (neověřeno do konce)
- **Pico PT-104** (4× Pt100/Pt1000, PC logger přes USB): „rozlíšenie 0.001 °C a presnosť 0.015 °C", [Elso.sk](https://www.elso.sk/pico-pp682-pt-104-zaznamnik-na-sondy-pt100/), „€847,47" s DPH (€689 bez DPH), „Na objednávku". Slovenský obchod; doručení do ČR jsem nenašel („Doprava zadarmo … s doručením na Slovensko"). Potřebuje PC připojený po celou dobu měření. Pt100 sondy zvlášť (např. Pico SE012 1/10 DIN, €104,55). Nepřepočítával jsem na Kč.
- **Vyřazeno:** Lascar EL-WiFi-TH+ (0,01 °C, ±0,2 °C, 7 490 Kč) – „Dimensions 82 x 70 x 36mm", WiFi, do termosky nejde.

## C) Levnější varianta s horším rozlišením (původní seznam)
Comet U0121 + 2× Comet SN252E + USB-C kabel (Epřístroje, 8 448 Kč) + 2 termosky (558 Kč) = 9 006 Kč. Rozlišení 0,1 °C, přesnost ±0,2 °C. Pro nárůst o jeden krok (0,1 °C) nestačí, pro výraznější ohřev ano.

## Poznámky k metodice (obecně, ne ze stránek)
Slepý pokus (někdo jiný náhodně zvolí, kterou termosku ohřejete), základní linie z 15 min klidu, průměrování posledních minut před a po, opakování 3–5×, stejné čidla a kabeláž v obou termoskách.
