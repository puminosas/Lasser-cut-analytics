import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


class LaserMachineErrorAnalysis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amada Laser Machine Error Analysis")
        self.setGeometry(100, 100, 1500, 900)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.init_filter_panel()
        self.init_main_view()
        self.load_data()
        self.setup_auto_update()

    def init_filter_panel(self):
         # Filter Panel Group Setup
        filter_panel = QGroupBox("Filter")
        filter_layout = QHBoxLayout()

         # Machine Dropdown Setup
        machine_label = QLabel("Machine Model:")
        self.machine_combo = QComboBox()
        filter_layout.addWidget(machine_label)
        filter_layout.addWidget(self.machine_combo)

        # Date Selectors Setup
        date_label = QLabel("Date Range:")
        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(self.end_date)

         # Apply filter button
        self.apply_filter_button = QPushButton("Apply Filter")
        self.apply_filter_button.clicked.connect(self.apply_filter)
        filter_layout.addWidget(self.apply_filter_button)

        filter_panel.setLayout(filter_layout)
        self.main_layout.addWidget(filter_panel)

    def init_main_view(self):
        # Split UI area into main display with errors, and analysis part

        main_view_layout = QHBoxLayout()
        self.main_layout.addLayout(main_view_layout)

        self.error_table = QTableWidget()
        self.error_table.setColumnCount(8)
        self.error_table.setHorizontalHeaderLabels([
            "Machine", "Nesting", "Omschrijving", "Start Time", "End Time", "Duration (s)", "Material", "Error Score"
        ])
        
        main_view_layout.addWidget(self.error_table, 3)


        # Summary Panel
        self.analysis_panel = QVBoxLayout()
        main_view_layout.addLayout(self.analysis_panel, 1)
        
        analysis_title = QLabel("Analysis")
        analysis_title.setFont(QFont('Arial', 12, QFont.Bold))
        self.analysis_panel.addWidget(analysis_title)
       
        self.summary_text = QTextBrowser()
        self.analysis_panel.addWidget(self.summary_text)

    def load_data(self):
          # Load excel and prepare the data
        try:
            # Load data from Excel
            self.data = pd.read_excel('/home/pumis/Desktop/Masinu_Klaidu_Analize/alarmcodes-amada-vanaf-1-10-2024.xlsx')

            #Convert time string column to datetime
            self.data['Start tijd'] = pd.to_datetime(self.data['Start tijd'], errors='coerce')
            self.data['Eind tijd'] = pd.to_datetime(self.data['Eind tijd'], errors='coerce')

            #calculate and set error duration to seconds column
            self.data['Duur_sec'] = (self.data['Eind tijd'] - self.data['Start tijd']).dt.total_seconds()

            self.populate_machine_filter()
            self.update_date_range()
            self.apply_filter()  # Apply default filter after loading data
            
        except Exception as e:
           QMessageBox.critical(self, "Error", f"Could not load data: {str(e)}")
           return

    def populate_machine_filter(self):
         #get machines for the filter combobox
        machines = ['All'] + list(self.data['Machine'].unique())
        self.machine_combo.clear()
        self.machine_combo.addItems(machines)
        
    def update_date_range(self):
        #get range of start and end time and use in the filter
        min_date = self.data['Start tijd'].min().date()
        max_date = self.data['Eind tijd'].max().date()
        self.start_date.setDateRange(min_date, max_date)
        self.end_date.setDateRange(min_date, max_date)
        self.start_date.setDate(min_date)
        self.end_date.setDate(max_date)


    def apply_filter(self):
          #get all filter parameters to pass for main error table update
        machine = self.machine_combo.currentText()
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
         
         #Create data copy so we don't change initial
        filtered_data = self.data.copy()  

         # filter out based on filter combobox
        if machine != 'All':
             filtered_data = filtered_data[filtered_data['Machine'] == machine]

        # filter out based on dates
        filtered_data = filtered_data[
            (filtered_data['Start tijd'].dt.date >= start_date) &
            (filtered_data['Eind tijd'].dt.date <= end_date)
        ]
        
          # calculate error score which is then added to error table and used in summary data calculations
        filtered_data = self.calculate_error_score(filtered_data)

         #Populate UI with generated data
        self.populate_error_table(filtered_data)
        self.update_summary_stats(filtered_data)


    def calculate_error_score(self, data):
          # error score for every row - combining error freq, duration, material type and machine model
         # for simplicity at first error is more costly if more frequent, longer duration, specific materials
         
           #create a grouping for material so its more general
         data['Material_Group'] = data.apply(lambda row: row['Nesting.Artikel.Artikelgroep'] if pd.notna(row['Nesting.Artikel.Artikelgroep']) else 'Unknown', axis=1)
        
         # Error Frequency Component - higher = worse error
         error_counts = data['Omschrijving'].value_counts()
         data['error_freq'] = data['Omschrijving'].apply(lambda x: error_counts.get(x, 0) + 1)  

        #same but scoped per machine error occurences
         machine_error_counts = data.groupby('Machine')['Omschrijving'].value_counts()
         data['machine_error_freq'] = data.apply(lambda row: machine_error_counts.get((row['Machine'], row['Omschrijving']),0) +1 , axis=1 )
           
        #Duration normalisation and calculation to be used with total score 
         data['Duration_normalized'] = data['Duur_sec'] / (data['Duur_sec'].max()+ 1)

        #Material grouping based on pre defined value map
         material_costs = {
            '1010-Staalplaat St. DC-01 (St.12-03), 0 t/m 3 mm KGW       1.0330': 1,
            '1020-Staalplaat S 235 JR, 2 t/m 10 mm               1.0038':1,
            '1062-Magnelis S250GD + ZM 310 MAC': 1.3,
            '1080-Staalplaat Sendzimir verzinkt                  1.0226': 1.1,
            '1090-Staalplaat elektrolytisch verzinkt (Zincor)': 1.2,
            '1205-RVS-plaat  RVS 304 2B zonder folie                    1.4301': 1.5,
            '1220-RVS-plaat  RVS 316 L 2B zonder folie                  1.4404':1.6,
            '1300-RVS-plaat  RVS 304 KK 320, met folie               1.4301': 1.5,
            '1415-Alu-plaat  AlMg1 (B57S)  : middel met folie 3.3315': 1.8,
            '1420-Alu-plaat  AlMg3 (54S)   : halfhard  zonder folie 3.3535':1.7,
            '9998-Diversen plaat (nog omzetten)':1.1
            }
        
         data['material_cost'] = data['Nesting.Artikel.Artikelgroep'].apply(lambda x: material_costs.get(x, 1.0) if pd.notna(x) else 1.0 )

         #Final Error Score
         data['Error Score'] = data['machine_error_freq'] * (data['Duration_normalized'] * data['material_cost'])
         return data
  
    def populate_error_table(self, data):
         #Generate error table 
        self.error_table.setRowCount(0)  # Clear all previous rows from table
        if data.empty:  #don't do anything when filtered table is empty
            return
    
        # use data to populate rows one by one
        row_count = len(data)
        self.error_table.setRowCount(row_count) # resize table for incoming data size

         # generate single array (row) from dataframe 
        for row_idx, row_data in data.iterrows():
            row = [
                 row_data["Machine"],
                 row_data["Nesting"],
                 row_data["Omschrijving"],
                row_data['Start tijd'].strftime('%Y-%m-%d %H:%M:%S'),
                row_data['Eind tijd'].strftime('%Y-%m-%d %H:%M:%S'),
                f"{row_data['Duur_sec']:.0f}",
                 row_data['Material_Group'],
                 f"{row_data['Error Score']:.2f}"
                 ]

            #fill table row cell by cell
            for col_idx, cell_data in enumerate(row):
                  self.error_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            
            #Autoresize each colum based on cell value to be always readable 
        self.error_table.resizeColumnsToContents()



    def update_summary_stats(self, data):
         #function generating summary table of most frequent errors etc
         summary_text = "<h3>Error Analysis Summary:</h3>"

          # dont' calculate anything when filtered data is empty
         if data.empty:
              summary_text += "No data available for the selected filter"
         else:
             # top errors - data is first counted, then its limited to 10 top most frequently
             top_errors = data['Omschrijving'].value_counts().head(10).to_frame().reset_index()
             top_errors.columns = ['Error Type', 'Count']
             summary_text += "<br><h4>Top 10 Most Frequent Errors:</h4>"
             summary_text += top_errors.to_html(index=False)

            # average error duration, grouped by machine and output as html
             avg_duration_per_machine = data.groupby('Machine')['Duur_sec'].mean().to_frame().reset_index()
             avg_duration_per_machine.columns = ['Machine', 'Average Error Duration (sec)']
             summary_text += "<br><h4>Average Error Duration per Machine:</h4>"
             summary_text += avg_duration_per_machine.to_html(index=False)

             #calculate all error counts per machine, display as HTML
             error_counts_per_machine = data['Machine'].value_counts().to_frame().reset_index()
             error_counts_per_machine.columns = ["Machine", "Error Count"]
             summary_text += "<br><h4>Error Count Per Machine:</h4>"
             summary_text += error_counts_per_machine.to_html(index=False)


              #output name of a single most problematic material and machine with top errors
             machine_with_highest_score = data.groupby('Machine')['Error Score'].sum().sort_values(ascending=False).index[0]
             top_material_group_machine = data.groupby(['Material_Group'])['Error Score'].sum().sort_values(ascending=False).index[0]
             
             #append additional info to general summary data
             summary_text += f"<br><p><b>Machine With Highest Error Score:</b> {machine_with_highest_score}</p>"
             summary_text += f"<br><p><b>Material Group Causing Most Errors:</b> {top_material_group_machine}</p>"


           # Prediction attempt - simple error time forecast via liner regrassion with usage of the current filter options
             summary_text += "<br><h4>Experimental - Predicting Error Time For  Machine (Linear Regression):</h4>"
             summary_text += "<p> Simple prediction of error using the duration for last entries in the table </p>"
             summary_text += self.get_simple_prediction(data)
             

        # Set formatted text data to UI browser view component  
         self.summary_text.setHtml(summary_text)
        


    def get_simple_prediction(self,data):
         # Function will make a simplified prediction of when the next error would be

            machine_selected = self.machine_combo.currentText()
            if machine_selected == "All" :
                  return "<p> Select Machine for Prediction (select machine filter from combobox) </p>"
            machine_data = data[data["Machine"] == machine_selected].copy()#make machine specific dataset copy from input data

           # simple test, that the data can be trained (there is data, and more than 1 point )
            if machine_data.empty or len(machine_data) <2:
                  return "<p> Not enough data for " + str(machine_selected) + " Machine Prediction (need at least 2 error records )</p>"

           # Prepare data for model. sort by timestamp so latest errors are selected first
            machine_data = machine_data.sort_values('Start tijd', ascending=True)
            #pick last errors for simplified regrassion analysis, limit results for testing
            last_errors = machine_data.tail(10)

           # use numpy so can shape single row correctly to linear regression parameters,
            # to have only array instead of columns from pandas table format for train
            x = np.arange(len(last_errors)).reshape(-1, 1)
            y = last_errors['Duur_sec'].values
             
           # Linear Regression part starts - if anything fails just output warning that training data didn't work
            model = LinearRegression()
            try:
                   model.fit(x, y)
                   new_x = np.array([len(last_errors)]).reshape(-1, 1)  # Predict the next error index from dataset size
                   predicted_y = model.predict(new_x)


                   formatted_prediction = f" <p>Predicted time until next error (estimated) : {timedelta(seconds=predicted_y[0]):%H:%M:%S}</p>"  # format result for UI element to be more user friendly
                   return formatted_prediction # return output text with predictions, including some general warning notes
            except Exception as e:
                    return f"<p>Error in prediction - could not train for {machine_selected}: </p>" + str(e)
                    # if function had any unexpected results, this would just catch any exceptions

    def setup_auto_update(self):
         #simple setup of auto update timer for loading the main excel data ( in this example runs hourly)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.auto_update)
        self.update_timer.start(3600000)  # Update every hour
    
    def auto_update(self):
          #Load the main excel and apply current filtering
         self.load_data()
         self.apply_filter()


def main():
      # start the application
     app = QApplication(sys.argv)
     window = LaserMachineErrorAnalysis()
     window.show()
     sys.exit(app.exec_())

if __name__ == '__main__':
    main()
