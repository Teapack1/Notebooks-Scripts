import os
import pandas as pd

directory = 'files'

csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
csv_files.sort()

concatenated_data = pd.DataFrame()

for file in csv_files:
    file_path = os.path.join(directory, file)
    data = pd.read_csv(file_path)
    concatenated_data = pd.concat([concatenated_data, data])

output_file = os.path.join(directory, 'concatenated_csv.csv')
concatenated_data.to_csv(output_file, index=False)