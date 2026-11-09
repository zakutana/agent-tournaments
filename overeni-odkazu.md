# Ověření odkazů – nákup jako soukromá osoba v ČR

Datum ověření: 2026-11-09. Prohlížeč: Playwright / Chromium (locale cs-CZ), JavaScript vykreslen (čekání 4–5 s po načtení).
Screenshoty: složka `screenshots/` (název podle domény + začátek cesty; `*_po-vlozeni`, `*_kosik`, `*_delivery`, `*_doprava` = kroky ověření košíku a dopravy).
Tučné **nelze ověřit** = stránku se nepodařilo načíst (bot-ochrana / captcha / 403). Captchy jsem neřešil ani neobcházel. Nic jsem neobjednával, nevyplňoval formuláře ani neposílal e-mail/osobní údaje. Do košíku jsem zboží vložil jen na vybraných náhradách (košík je jen v mé relaci; po ověření nikam nepokračoval).

Zkratky: „citace" = doslovný text ze stránky (v uvozovkách). „nenalezeno" = na stránce jsem to nenašel.

---

## 1. Zadané odkazy

| # | Odkaz | Stav | Produkt | Cena | Skladem | Doručení do ČR | Citace |
|---|---|---|---|---|---|---|---|
| 1 | gotogarden.com/products/kalibracni-zavazi-50-g | **mrtvý** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **402**, finální URL beze změny, title „Store unavailable". Text: „This store is currently unavailable." / „Are you the store owner?" (Shopify stránka obchodu) |
| 2 | mt.com/cz/cs/…/single_test_weight_158657.html | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP 200, ale obsah je blokační stránka, title „METTLER TOLEDO - 403 Forbidden": „We are sorry, but your current behavior is detected as abnormal, if you feel you have reached this page in an error, please try again later..." |
| 3 | mt.com/cz/cs/…/single_test_weight_30406376.html | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | Totéž: „METTLER TOLEDO - 403 Forbidden" / „your current behavior is detected as abnormal" |
| 4 | b2b-cz.vwr.com/store/category/zavazi-kalibracni/600733?view=list | **mrtvý** (kategorie neexistuje; přesměrováno) | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP 200, finální URL `https://www.vwr.com/cz/cs/?view=list`, title „Globální poskytovatel řešení pro biofarmacii, zdravotnictví a laboratoře \| VWR, part of Avantor" = úvodní stránka, žádné závaží. Na stránce „Přihlásit se / Registrovat", „Order Entry" (B2B portál). |
| 5 | cz.rs-online.com/web/p/kalibracni-zavazi/1891647 | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, title „Access Denied": „You don't have permission to access "http://cz.rs-online.com/web/p/kalibracni-zavazi/1891647" on this server." |
| 6 | alza.cz/digitalni-kapesni-vaha-od-0-01g-d7138338.htm | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, Cloudflare captcha: „Prosím, potvrďte, že jste z masa a kostí" / „Potvrďte, že jste člověk". (Navíc proxy kontejneru zablokovala `challenges.cloudflare.com`.) |
| 7 | m.alza.cz/verk-17013-digital-pocket-scale-200-g-0-01-g-d7989393.htm | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, tatáž captcha: „Prosím, potvrďte, že jste z masa a kostí" |
| 8 | kaufland.cz/product/412147917/ | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, „Vyžadováno ověření": „Potvrďte, že nejste robot, abyste mohli pokračovat." |
| 9 | kaufland.cz/product/207767161/ | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, „Vyžadováno ověření" (totéž) |
| 10 | action.com/cs-cz/p/3218558/presna-digitalni-vaha/ | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403**, „Provádění bezpečnostního ověření": „Tato stránka používá službu zabezpečení k ochraně proti škodlivým botům." |
| 11 | asset.conrad.com/…/000100428ML01/…k202.pdf | **OK jako manuál** (není to prodejní stránka, nelze koupit) | „2-kanálový digitální teploměr se záznamníkem „306" (K 202)", „Obj. č.: 10 04 28" | – | – | – | HTTP 200, `application/pdf`, 7 stran. Rozlišení a ostatní údaje viz část 3. |
| 12 | asset.conrad.com/…/000100518ML01/…k204…pdf | **OK jako manuál** (není to prodejní stránka) | „Digitální teploměr K204", „Obj. č. 10 05 18" | – | – | – | HTTP 200, `application/pdf`, 5 stran. „Teploměr navíc disponuje funkcí záznamu dat." Údaje viz část 3. Pozn.: v názvu souboru je „2187664 … kalibriran po ISO", v textu manuálu zmínka o kalibraci ISO nenalezena. |
| 13 | cz.rs-online.com/web/p/zaznamniky-dat/0126717 | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403** „Access Denied": „You don't have permission to access … /0126717 on this server." |
| 14 | cz.rs-online.com/web/p/zaznamniky-dat/1259516 | **nelze ověřit** | nenalezeno | nenalezeno | nenalezeno | nenalezeno | HTTP **403** „Access Denied" (totéž) |
| 15 | avantorsciences.com/cz/cs/product/41220121/digital-thermometer-testo-925 | **jen B2B** (cena a dostupnost jen po přihlášení) | „Digital thermometer, testo 925", kat. č. TEST0563.0925 | nenalezeno: „Přihlásit se pro vaši cenu" | nenalezeno: „Přihlásit se pro dostupnost" | nenalezeno | HTTP 200, finální URL `https://www.vwr.com/cz/cs/product/41220121/digital-thermometer-testo-925`. Tlačítko „PŘIDAT DO KOŠÍKU" na stránce je, ale bez ceny. Parametry: „Rozsah: ‒50...+1000 °C", „Přesnost: ±(0,5 °C + 0,3% of mv)", „Rozlišení: 0,1 °C (‒50...+499,9 °C)". Funkce záznamu dat na stránce: **nenalezeno** (není to datalogger). Potvrzení B2C: nenalezeno. |

**Shrnutí:** z 15 odkazů je 1× mrtvý (gotogarden), 1× mrtvý/přesměrovaný (VWR kategorie), 1× jen B2B (testo 925), 2× jen PDF manuály, a 10× **nelze ověřit** (bot-ochrana).
**Žádný ze zadaných odkazů se mi nepodařilo ověřit jako funkční B2C nákup.**

---

## 2. Náhrady v českých e-shopech (ověřeno stejným postupem)

### 2a. Kalibrační závaží 50 g

| Obchod / odkaz | Stav | Produkt | Cena | Skladem | Doručení do ČR | Citace |
|---|---|---|---|---|---|---|
| **Metershop** – https://metershop.cz/produkt/kalibracne-zavazie-m1-50-g/ | OK (HTTP 200, koš ověřen) – pozor: **slovenský** provozovatel | Kalibrační závaží M1-50 g, nerez, výrobce G&G Německo | **264 Kč s DPH** (215 Kč bez DPH) | ano, ale text je slovensky: „Na skladě. Štandardne odosielame na nasledujúci pracovný deň." | ano: stránka Dopravní podmínky, „Doprava Česká republika … Objednávka do 2399 Kč s DPH: DHL Kurýr 215 Kč s DPH, Packeta 120 Kč s DPH" | „50 g kalibrační závaží třídy přesnosti M1 určené ke kontrole a kalibraci vah třídy přesnosti III", „největší dovolená chyba +2,5 mg", „materiál nerezová ocel". Tlačítko „Přidat do košíku" → košík „Kalibrační závaží M1-50 g 264 Kč", „Sleva za produkty -26 Kč" (akce Black Listopad −10 %). B2C: „Měřidla pro profesionály ale i pro domácí kutily." V košíku se mi nabízely jen slovenské dopravy (např. „Doprava cez Packeta: 92 Kč", „Cena celkem 358 Kč (včetně 67 Kč DPH)") – české ceny jsou na stránce Dopravní podmínky. Doprava zdarma od 2 400 Kč. |
| **Digitální váhy** – https://www.digitalnivahy.com/produkt/digitalni-vahy-prislusenstvi-k-vaham-kalibracni-zavazi/ZAVAZI50/kalibracni-zavazi-50g/ | OK (HTTP 200, koš ověřen) | Kalibrační závaží 50g, MyWeigh, kód ZAVAZI50 | **69 Kč** (ceny „včetně DPH") | „Dostupnost: skladem" | ano: „Česká pošta – ČR – balík do ruky … přeprava po celé České republice"; cena poštovného: nenalezeno („řídí aktuálním ceníkem České pošty") | „Kalibrační závaží 50g.", košík „ZAVAZI50 Kalibrační závaží 50g 69 Kč", „Všechny uvedené ceny jsou včetně DPH.", nad 5 000 Kč poštovné zdarma. Třída přesnosti / tolerance: nenalezeno. Při objednávce „standardně zasíláno … na dobírku". |
| SpecialniZahradnictvi.cz – https://www.specialnizahradnictvi.cz/kalibracni-zavazi/kalibracni-zavazi-50g/ | stránka OK (HTTP 200), **košík netestován** | Kalibrační závaží 50g | 65 Kč (54 Kč bez DPH) | „SKLADEM" | nenalezeno | „Celokovové kalibrační závaží … hmotnost: 50g. Kalibrační závaží s maximální odchylkou 0,25mg." (tvrzení prodejce) |
| Growway-garden.cz – https://www.growway-garden.cz/eshop/zavazicko-50-g-3730/ | stránka OK (HTTP 200), **košík netestován** | Závažíčko 50 g | 65,00 Kč | „Skladem" | nenalezeno | „Kalibrační závaží 50 g", „Do košíku", „DOPRAVA ZDARMA NAD 2000 Kč" |

Doporučení: pokud stačí orientační kontrola váhy, nejlevnější je digitalnivahy.com (69 Kč). Pokud chcete uvedenou třídu přesnosti (M1), je to Metershop (264 Kč), ale jde o slovenský obchod.

### 2b. Váha 200 g / 0,01 g

| Obchod / odkaz | Stav | Produkt | Cena | Skladem | Doručení do ČR | Citace |
|---|---|---|---|---|---|---|
| **Datart** – https://www.datart.cz/kuchynska-vaha-domo-do9096w-nerez.html | OK (HTTP 200, koš ověřen) | Kuchyňská váha Domo DO9096W nerez (kód DOMDO9096W) | **449 Kč s DPH** (371 Kč bez DPH v košíku) | „IHNED K ODESLÁNÍ", „u vás již 10. 11. 2026"; „až v 2 prodejnách" | dopravy ano, slovo „ČR/Česko" v dialogu nenalezeno; nabízeno: „Balíkovna … od 59 Kč", „Zásilkovna – doručení na adresu … 89 Kč", „Doprava kurýrem DPD … 99 Kč" | „laboratorní/zlatnická váha • přesnost 0,01 g • … nosnost 200 g • kapesní formát", tlačítko „Vložit do košíku" → košík „Domo DO9096W nerez … 449 Kč / ks včetně DPH 21%". B2C: ceny s DPH 21 %; zvláštní sekce firem „DATART PRO podnikání" je oddělená. |
| Datart – Eldonex EKS-4045-BK – https://www.datart.cz/kuchynska-vaha-eldonex-eks-4045-bk-cerna | stránka OK (HTTP 200), košík netestován | Kuchyňská váha Eldonex EKS-4045-BK černá | 229 Kč s DPH | ve výpisu hledání: „Poslední kus k odeslání" (na samotné stránce stav nepotvrzen) | viz výše | „Maximální zatížení: 0,2 kg • Přesnost vážení: 0,01 g" |
| Datart – SOGO SS-3996 – https://www.datart.cz/kuchynska-vaha-sogo-ss-3996-cerna | stránka OK (HTTP 200), košík netestován | Kuchyňská váha SOGO SS-3996 černá | 349 Kč s DPH | ve výpisu hledání: „Ihned k odeslání" | viz výše | „Maximální zatížení: 0,2 kg • Přesnost vážení: 0,01 g" |

(Alza, Kaufland a Action – původní odkazy 6–10 – jsou blokované, proto jsem je nahradil Datartem.)

### 2c. Teploměr se záznamem dat – kde koupit

Viz část 3 (K202 / K204).

### 2d. Dvě stejné nerezové termosky 0,5 l

| Obchod / odkaz | Stav | Produkt | Cena | Skladem | Doručení do ČR | Citace |
|---|---|---|---|---|---|---|
| **Datart** – https://www.datart.cz/termoska-lock-lock-lhc3220rbr-cervena.html | OK (HTTP 200, koš ověřen s množstvím **2 ks**) | Termoska Lock&lock LHC3220RBR červená (kód LOCLHC3220RBR) | **279 Kč / ks s DPH**, 2 ks = **558 Kč** (231 Kč / ks bez DPH) | „IHNED K ODESLÁNÍ", „u vás již 10. 11. 2026"; konkrétní počet kusů na skladě: nenalezeno, ale košík přijal 2 ks bez chybového hlášení | stejný dialog dopravy: „Balíkovna … od 59 Kč", „Zásilkovna – doručení na adresu … 89 Kč", „Doprava kurýrem DPD … 99 Kč" | „Termoska • Objem termonádoby: 500 ml • Materiál: nerezová ocel • Barva: červená", v košíku s množstvím 2: „Cena celkem s DPH 558 Kč", „Lock&lock LHC3220RBR červená … Ihned k odeslání … 279 Kč / ks". Screenshot `datart_lock_lhc3220rbr_kosik_2ks.png`. |
| Datart – varianta GPK – https://www.datart.cz/termoska-lock-lock-lhc3220gpk.html | stránka OK (HTTP 200), košík netestován | Termoska Lock&lock LHC3220GPK | 279 Kč s DPH | ve výpisu: „Ihned k odeslání" | viz výše | „Termoska • Objem termonádoby: 500 ml • Materiál: nerezová ocel • Barva: růžová, zlatá" |

Poznámka: produktová fotka u „LHC3220RBR červená" je na screenshotu spíše růžová/vínová – o barvě rozhoduje text na stránce, fotku jsem neposuzoval.

---

## 3. Voltcraft K202 / K204 – který model se dnes dá koupit

### 3a. Údaje z manuálů (Conrad PDF)

| | **K202** (manuál Obj. č. 10 04 28) | **K204** (manuál Obj. č. 10 05 18) |
|---|---|---|
| Kanály | 2 („2-kanálový digitální teploměr se záznamníkem") | 4 („Měřící vstup … kanálu T1 … T2 … T3 … T4") |
| Rozsah | „Typ K: – 200 °C až + 1370 °C"; dodané čidlo „– 50 °C až + 200 °C" | „-200 až +1370 °C"; dodané čidlo „-50 °C až +200 °C" |
| **Rozlišení** | „0,1 °C (< 200 °C); 1 °C (> 200 °C )" | tabulka: -200 až +200 °C → 0,1 °C; +200 až +400 °C → 1 °C; +400 až +1370 °C → 1 °C |
| **Přesnost** | **nenalezeno** (manuál uvádí jen, že je „zaručena, bude-li se … okolí teploměru pohybovat … od + 18 °C až do + 28 °C", číselná tolerance chybí) | „-200 až +200 °C ±( 0,2% + 1K)"; „+200 až +400 °C ±( 0,5% + 1K)"; „+400 až +1370 °C ±( 0,2% + 1K)"; čidlo TP-K01: „-50 až +200 °C± 2,2K nebo ±0,75%"; „Přesnost je zaručena po dobu jednoho roku +23 °C ± 5K" |
| Záznam dat | „ukládat do své vnitřní paměti až 16.312 naměřených" hodnot | „Teploměr navíc disponuje funkcí záznamu dat." (tlačítko REC, výchozí interval 5 s) |
| Napájení | 1 baterie 9 V | 9 V |
| Rozhraní | PC přes software „SE305" | sériové rozhraní |

Pozn.: Údaje o přesnosti u K202 uvádí jen e-shop Promertech (viz níže, „Základní přesnost (±) 0,3 %", „Základní přesnost měření (+/-) 1 °C", „Rozlišení teploty 0.1 °C") – to není z manuálu a v manuálu K202 jsem to nenašel.

### 3b. Co lze dnes koupit v ČR jako soukromá osoba

| Model | Obchod / odkaz | Stav | Cena | Skladem | Doručení do ČR | Citace |
|---|---|---|---|---|---|---|
| **Voltcraft K202** (Conrad č. 100428 – shoduje se s manuálem 10 04 28) | **Voltworld.cz** – https://www.voltworld.cz/teplomery/voltcraft-k202-teplomer--typ-senzoru-k--funkce-dataloggeru/ | OK (HTTP 200, košík ověřen) | **3 735 Kč s DPH** (3 087 Kč bez DPH) | „Skladem" | ano: v pokladně „Země doručení: Česká republika / Slovensko", „PPL na výdejní místo 99 Kč", „PPL na adresu 139 Kč", „Zásilkovna na výdejní místo 125 Kč", „Zásilkovna na adresu 145 Kč" | „Kód produktu: 100428", „Datalogger pro 16 000 hodnot", košík „VOLTCRAFT K202 teploměr, typ senzoru K, funkce dataloggeru … 3 735 Kč / ks", „Cena bez DPH: 3 086,78 Kč", „Objednejte ještě za 4 265 Kč a budete mít dopravu zdarma." B2C: obchodní podmínky řeší spotřebitele („Volbou práva … není kupující, který je spotřebitelem, zbaven ochrany…"); zákaz prodeje soukromým osobám nenalezen. |
| Voltcraft K202 | Promertech.cz – https://promertech.cz/voltcraft-k202-digitalni-teplomer-s-dataloggerem | stránka OK (HTTP 200), košík netestován | 3 809,71 Kč s DPH (3 148,52 Kč bez DPH) | „Skladem u dodavatele (expedice do 7 dnů)" | stránka Doprava a platba: „Doručení do: 🇨🇿 Česko", „Zásilkovna – výdejní místo 99 Kč", „PPL Standard 110 Kč" | „Teploměr … 16 000 naměřených hodnot", „Doprava zdarma" |
| Voltcraft K202 | Epřístroje.cz – https://www.epristroje.cz/dvoukanalovy-teplotni-datalogger-voltcraft-k202/ | stránka OK (HTTP 200), košík netestován | 4 990 Kč s DPH (4 124 Kč bez DPH) | „Do 3 dnů", „Můžeme doručit do: 13.11.2026" | nenalezeno | „Do košíku" |
| **Voltcraft K204 – ale kód 100806, ne 100518** | Promertech.cz – https://promertech.cz/voltcraft-k204-digitalni-teplomer | OK (HTTP 200, košík ověřen) | **2 416,38 Kč s DPH** (1 997,01 Kč bez DPH) | „Skladem u dodavatele (expedice do 7 dnů)" | viz Promertech výše (Česko) | „Provedení 4-kanálový", v košíku „Voltcraft K204 - Digitální teploměr 100806". B2C: obchodní podmínky § 1751 OZ, „Toto právo [odstoupení bez udání důvodu] náleží výhradně spotřebiteli." |

**Důležité upozornění ke K204:** Promertech prodává K204 s kódem **100806** (v košíku „100806"). Váš manuál je k **10 05 18**. Manuál k 100806 (Conrad, „Digitální teploměr K 204", „Obj. č.: 10 08 06") jsem stáhl a porovnal: popisuje sériové rozhraní RS-232 a MAX/MIN, ale slova „datalogger", „REC" a „paměť" jsem v něm **nenašel**; manuál 100518 naopak uvádí „funkcí záznamu dat" a tlačítko REC. Zdá se tedy, že 100806 **nemá záznam do paměti**, ale to je můj závěr z porovnání textů, ne potvrzení od prodejce. Také Promertechova stránka K204 na rozdíl od K202 neuvádí paměť 16 000 hodnot.
**K204 s dataloggerem (100518) jsem v žádném otevřeném českém B2C obchodě neověřil → nelze ověřit.** Conrad.cz (`conrad.cz/cs/p/100428.html`, `…/100518.html`) vrací Cloudflare „Okamžik…" (HTTP 403); Heureka a TS Bohemia jsou také blokované.

**Závěr pro K202/K204:** Ověřeně koupit lze **K202 (100428)** – Voltworld 3 735 Kč, skladem, PPL do ČR; v manuálu je rozlišení 0,1 °C (< 200 °C) / 1 °C (> 200 °C), přesnost číselně uvedena není.

---

## 4. Co jsem nemohl ověřit a proč

- Alza (2 odkazy), Kaufland (2), Action (1), Conrad.cz, Heureka, TS Bohemia, Hornbach („Client Challenge"), CZC/Mall (přesměrování na allegro.cz, HTTP 403): Cloudflare/Akamai captcha nebo blokace. Captchu jsem neřešil.
- Mettler Toledo (2) a RS Components (3): blokace („abnormal behavior" / „Access Denied").
- Conrad.cz: nelze potvrdit, zda je dnes K204 100518 v prodeji a za kolik. Cena ve vyhledávači (nepřevzata do tabulky, neověřeno stránkou).
- Datart: počet kusů termosek na skladě stránka neuvádí (jen „Ihned k odeslání"); doručení: dialog nezmiňuje výslovně „ČR".
- Kalibrační závaží: certifikované třídy (F1/E2) jsem v otevřeném B2C českém obchodě neověřil (P-LAB a Mikrovahy.cz jsem otevřel, ale neanalyzoval).

## 5. Použité postupy a vedlejší poznámky

- Stav = skutečný HTTP stav z Chromia. U mt.com je 200, ale obsah je blokační stránka, takže jsem ho neuznal jako ověřený.
- Webové vyhledávání jsem použil jen k nalezení kandidátských domén; každý uvedený údaj v tabulkách pochází z otevřené stránky v prohlížeči (nebo z manuálu PDF).
- Soubory screenshotů: `screenshots/` (např. `datart_domo_do9096w_kosik.png`, `voltworld_k202_doprava.png`, `metershop_m1_50g_kosik.png`).
