# Amada Lazerinių Staklių Klaidų Analizės Įrankis

Šis įrankis sukurtas analizuoti Amada lazerinių staklių klaidų duomenis iš Excel failų. Jis padeda identifikuoti dažniausiai pasitaikančias klaidas, jų trukmę ir kitus statistinius rodiklius, kurie gali padėti gerinti gamybos efektyvumą ir mašinų priežiūrą.

## Pagrindinės Savybės

*   **Duomenų Įkėlimas:** Importuoja klaidų duomenis iš Excel failo.
*   **Filtravimas:** Leidžia filtruoti duomenis pagal mašinos modelį ir laiko intervalą.
*   **Statistinė Analizė:** Apskaičiuoja:
    *   Top 10 dažniausiai pasitaikančių klaidų.
    *   Vidutinę klaidų trukmę (sekundėmis) pagal kiekvieną mašiną.
    *   Visų klaidų skaičių pagal kiekvieną mašiną.
    *   Mašiną su didžiausiu klaidų "skoru".
    *   Medžiagų grupę, kuri generuoja daugiausia klaidų.
*   **Klaidų Skoro Apskaičiavimas:** Automatiškai apskaičiuoja individualu klaidu score pagal, klaidų dažnumą, trukmę, mašinos modelį ir materialo tipo įtaką.
*  **Paprastas Prognozavimas** Metodas bando numatyti kada ivyks sekanti klaida (beta test). Reikalauja sufiltruotu mašinu duomenų.
*   **Lentelinis Vaizdavimas:** Atvaizduoja duomenis lentelėje su:
    *   Mašina, `nesting` duomenys, klaidos aprašymas.
    *   Pradžios ir pabaigos laikas, trukmė (sekundėmis), naudojamos medžiagos pavadinimas
    *    Klaidų Skoro (pagal nustatytą algoritmą)
*   **Automatinis Atnaujinimas:** Įrankis automatiškai atnaujina duomenis kas valandą (galima pakeisti kodo parametruose).

## Reikalavimai

*   **Python 3.6+**
*   **Bibliotekos:**
    *   `pandas`
    *   `PyQt5`
    *   `numpy`
    *   `matplotlib`
    *   `seaborn`
    *   `scikit-learn`

    Jūs galite įdiegti šias bibliotekas naudodami:
    `pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn`

## Kaip Naudoti

1.  **Įdiekite Reikiamas Bibliotekas:** Paleiskite `pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn` komandą savo komandinėje eilutėje/terminale.

2.  **Pakeiskite Duomenų Failo Pavadinimą (jeigu reikia):** Įsitikinkite, kad kodo viduje esantis Excel failo pavadinimas `alarmcodes-amada-vanaf-01-10-2024.xlsx` atitinka jūsų failo pavadinimą arba jį pakeiskite, kad atitiktu (126eilutėje).

3.  **Paleiskite Kodą:** Išsaugokite kodą (pvz: `main.py`) ir paleiskite jį komandinėje eilutėje (terminale): `python main.py`
4.  **Analizė** Panaudokite "filter" grupėje pateiktas priemones, analizuokite reikiamus duomenis pagal mašina ir laikotarpį, tada peržiūrėkite lentele. Apatiniame kampe generuojama "summary", kuri išvardina suvestinius duomenis.

## Integracija

*   **Duomenų Šaltinis:**  Šiuo metu kodo failas skaito `xlsx` failą. Esant reikalui ji galite pasikoreguoti (126eiluteje) kad skaitytu `csv`, `json`, `txt` ir kt. Esant reikalui ataskaita galima pritaikyti `MySQL` arba panašiais sprendimais duomenų bazėms.
*   **Aut. Atnaujinimas:** Automatinis atnaujinimas veikia kiekviena valanda, bet jei tai reikia - galima pritaikyti ir kitais terminais. Tai nustatoma (379eiluteje) :`self.update_timer.start(3600000)`.
*   **Kiti Patobulinimai:** Esant dideliam duomenų kiekiui siūloma panaudoti: papildoma klaidu klasifikavimą pagal tipą ir pan, daugiau informacijos su diagramomis ir panašiai.  Taip pat predikciju modeliai gali buti labai naudingi esant pastoviai informacijai (esamas predikcijos modelis skirtas labiau testavimui).

## Kodo Struktūra

*   `LaserMachineErrorAnalysis` klasė yra pagrindinė kodo struktūra, kontroliuojanti visą vartotojo sąsają ir duomenų analizės logiką.
*  Pati pagrindinė funkcija yra `def main()`, kur paleidžiamas programos langas ir kuri atsakinga už kodo "startą".
*   GUI metodai sukurti  per : `init_filter_panel()` , `init_main_view()` ir kt, ir kontroliuoja grafines programas (naudojant `PyQt5`)
*   `load_data()` užkrauna pagrindinį `excel` faila (nustato datu tipus) ir paruošia `pandas dataframe` objektui.
*  `calculate_error_score(self, data)`  - apskaičiuoja  bendrą klaidos "skora". (kaip didelis yra erroras lyginant kitus parametrus ir kokią įtaką turi pagal tipa ar pan.). Šio rezultatai panaudojami tiek UI atvaizdavime (per  `populate_error_table`), o tiek ataskaitų skyrelyje per `update_summary_stats()`.
*    `apply_filter(self)` kontroliuoja filtrą, kuri pritaiko datas, masinu modelius. ir visą reikiamą informaciją parodo vartotojui.

Šis `README` failas turėtų padėti jums greitai susipažinti su kodo funkcijomis ir jo integravimo galimybėmis.
