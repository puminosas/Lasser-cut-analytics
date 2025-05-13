Amada Laser Machine Foutanalyse Tool
Deze tool is ontworpen om foutgegevens van Amada laser snijmachines te analyseren met behulp van Excel-bestanden. Het helpt bij het identificeren van veelvoorkomende fouten, hun duur en andere statistische indicatoren, wat kan bijdragen aan de verbetering van de productie-efficiëntie en het machineonderhoud.

Belangrijkste Eigenschappen
Data Laden: Importeert foutgegevens uit een Excel-bestand.
Filteren: Maakt het filteren van gegevens mogelijk op basis van machinemodel en datumbereik.
Statistische Analyse: Berekent:
Top 10 meest voorkomende fouten.
Gemiddelde foutduur (in seconden) voor elke machine.
Totaal aantal fouten per machine.
De machine met de hoogste totale foutscore.
De materiaalgroep die de meeste fouten veroorzaakt
Foutscore Berekening: Berekent automatisch een individuele foutscore op basis van frequentie, duur, machinemodel en materiaal impact.
Simpele Voorspelling: (Beta Test) Maakt simpele fout voorspelling gebruik makend van liner regrassion method. Voor de beste nauwkeurigheid dient het resultaat geproduceerd worden met één geselecteerde machine uit filter paneel
Tabellaire Weergave: Toont gegevens in een tabel met:
Machine, Nesting gegevens en foutbeschrijving.
Start- en eindtijd, duur (in seconden), type materiaal en Foutscore.
Automatische Updates: De tool kan data uit het Excel-sheet elke uur automatisch vernieuwen. (Deze parameter kan worden gewijzigd in code config parameters.)
Vereisten
Python 3.6+

Bibliotheken:

pandas
PyQt5
numpy
matplotlib
seaborn
scikit-learn
Je kunt deze bibliotheken installeren met behulp van: pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn

Hoe te Gebruiken
Installeer de Vereiste Bibliotheken: Voer de commando pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn in je command line/terminal.
Check / Update bestandsnaam: Zorg ervoor dat de Excel-bestandsnaam in de code overeenkomt met de jouwe (standaard: alarmcodes-amada-vanaf-01-10-2024.xlsx). Zo niet update het, op 126de regel.
Start de code: Sla de code op (bijv., als main.py) en start hem vanuit de command line (terminal): python main.py
Data Analyse Gebruik "Filter" sectie aangegeven in interface en controleer, analyseer data per gekozen machine/ periode, waarna de informatie via een tabel getoond wordt in het venster. Onderste paneel toont een snelle overzicht tabel per filtering.
Integratie
Data Bron: Momenteel leest de code gegevens uit een xlsx bestand. Je kunt het eenvoudig aanpassen als je csv, json of andere file formats, of andere databases (MySQL en enz.) nodig hebt. Voor het wijzigen data lees methode wijzig de method load_data().
Automatische Update: Standaard autoupdate vernieuwd alle informatie (inclusief ui) elke uur . Indien nodig kunnen deze time-parameters makkelijk in code worden aangepast. Parameters voor time aanpassen in lijn: 379: self.update_timer.start(3600000).
Toekomstige Verbeteringen: Als je werkt met grotere data sets kun je een aanvulling maken, betere classificatie van fouten per type/groepen, meer diagrammen en visuele presentatie en verbetering van predictie modellen.
Code Structuur
De LaserMachineErrorAnalysis klasse is de hoofdstructuur van het script en bepaalt de interface elementen.
def main() methode is het startpunt waar GUI interface gebouwd word.
De GUI methodes gedefinieerd via: init_filter_panel() en init_main_view() beheerd UI creatie en structuur via gebruik van PyQt5.
load_data() Laad excel en zet data object in een pandas dataframe structuur, voor verdere informatiebewerkingen. Zodra data geladen, zorgt de methode er voor dat alle belangrijke initial processen voor correcte informatie weergave van type/ filter etc uitgevoerd worden
calculate_error_score(self, data) - bepaalt individuele Error Score.(de method analyseert impact van elk type fout gebruikmakend van frequentie, materiaal, duur etc.). De methodes gebruikt output results per individuele foute record en maakt van dat het total Score, voor beter UI data presentatie.
populate_error_table(self, data) laad geselecteerde fout tabel rijen op de table weergave. Deze data wordt ingevoerd nadat een filter word gemaakt (gebruiker krijgt relevante en gefilterde fout informatie), tabel data wordt automatisch aangepast.
update_summary_stats(self, data) Geeft op HTML based snelle overzicht per fout type , machines. Method gebruikt data per gemaakte filtratie en gebruikt error score informatie. (method data word uitgelezen door QTextBrowser window)
apply_filter(self) beheer filters die gemaakt worden voor selectie van fout tabel output per: machines model / periode selectie. Deze README zou genoeg info moeten bevatten om je te helpen sneller inzicht krijgen op de functies en integratie.
