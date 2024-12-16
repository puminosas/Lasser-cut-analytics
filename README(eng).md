# Amada Laser Machine Error Analysis Tool

This tool is designed to analyze error data from Amada laser cutting machines using Excel files. It helps identify common errors, their duration, and other statistical indicators, which may help improve production efficiency and machine maintenance.

## Main Features

*   **Data Loading:** Imports error data from an Excel file.
*   **Filtering:** Allows data filtering by machine model and date range.
*   **Statistical Analysis:** Calculates:
    *   Top 10 most frequent errors.
    *   Average error duration (in seconds) for each machine.
    *   Total error count for each machine.
    *   The machine with the highest total error score.
    *    Material group, causing the most of errors.
*   **Error Score Calculation:** Automatically calculates an individual error score based on frequency, duration, machine model, and material impact.
*   **Simple Prediction:** (Beta Test) Makes a simple error time forecast with liner regrassion. Requires data selection per individual machine from a filter to perform well.
*   **Tabular Display:** Displays data in a table with:
    *   Machine, Nesting data, and error description.
    *   Start and end times, duration (seconds), material type and Error score
*  **Automatic Updates:** This application can reload the main Excel sheet every hour. (the time frame can be altered in the application config).

## Requirements

*   **Python 3.6+**
*   **Libraries:**
    *   `pandas`
    *   `PyQt5`
    *   `numpy`
    *   `matplotlib`
    *   `seaborn`
    *  `scikit-learn`

    You can install these libraries using:
    `pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn`

## How to Use

1.  **Install Required Libraries:** Run the command `pip install pandas PyQt5 numpy matplotlib seaborn scikit-learn` in your command line/terminal.
2.  **Check/Update File name:** Ensure that the Excel filename in the code matches yours (default: `alarmcodes-amada-vanaf-01-10-2024.xlsx`) . If not, then update 126th line with appropriate filename.
3.  **Run the Code:** Save the code (e.g., as `main.py`) and run it from the command line (terminal): `python main.py`
4.  **Data Analysis** Use "filter" group provided for filter, analyze required data per Machine and date ranges, and view results in the main table. At the bottom side a summary is displayed with statistical information for quick overview.

## Integration

*   **Data Source:**  Currently, the code reads data from an `xlsx` file. The data reading code can be adapted for any type `csv`, `json`, or database (such as  `MySQL`, or etc.). For changing data access look up function `load_data()`.
*   **Autoupdate:** Default autoupdate will update all the information and UI elements every hour . If required you can alter time parameters. Change parameters at  line 379: `self.update_timer.start(3600000)`.
*   **Future Improvements:**  If you use bigger files, the code might be further enhanced with better classification of errors by type, diagrams, and improved prediction models.

## Code Structure

*   The `LaserMachineErrorAnalysis` class is the main structure, handling the GUI and data processing.
*    `def main()` - where the GUI of main class are launched to show to user. (basically code entrypoint).
*  GUI methods defined via `init_filter_panel()` and `init_main_view()`, handle creation of UI elements based on the `PyQt5` module.
*  `load_data()` loads excel sheet into `pandas` table object. After excel is parsed it calls for further processes to be completed, as the data type conversions and initial filters (if necessary).
*   `calculate_error_score(self, data)` Calculates general error score for filtering results.
*   `populate_error_table(self, data)` Loads a list of errors per certain filtered data, and loads that info in table view to user interface, for manual inspection, (each individual row with respective information per filter settings).
* `update_summary_stats(self, data)`  Outputs the current general error statistics per machine, error type and duration with usage of error scoring calculations. The method renders summary table to UI browser (`QTextBrowser` with the use of `HTML`).
*  `apply_filter(self)` Method applies main parameters  to data and renders the information based on applied settings in filter window.

This `README` file provides sufficient information to get started with the application, but should provide necessary pointers where to alter specific parts of the application.
