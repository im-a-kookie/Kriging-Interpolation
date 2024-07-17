import csv
import numpy as np

# the dataset class provides rows and columns as numpy arrays
class dataset:
    # init method or constructor
    def __init__(self, column_titles, columns):
        self.column_titles = column_titles
        self.columns = columns
        
    def get(self, title):
        for i in range(len(self.column_titles)):
            if(self.column_titles[i] == title):
                return self.columns[i]
        return []        

def loadcsv(path):
    # Read each row in the CSV
    # Initialize empty lists to store data from each column
    columns = []
    column_titles = []
    # Open the CSV file for reading
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if reader.line_num == 1:
                num_columns = len(row)
                print(f"Columns: {num_columns}")
                for i in range(num_columns):
                    columns.append([])
                    column_titles.append(row[i])
            else:
                for i in range(num_columns):
                    columns[i].append(float(row[i]))
                    
    return dataset(column_titles, columns)
        

