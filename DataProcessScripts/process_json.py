# Convert processed timeseries data to json format
import os
import pandas as pd

source_directory = 'BenchmarkDatasets/processed_timeseries_csvs/A1Benchmark'
destination_directory = 'BenchmarkDatasets/processed_jsons/A1Benchmark'

datasets_count = 67
for i in range(1, datasets_count+1):
    filename_ext_csv = 'real_'+str(i)+'.csv'
    csv_file_name = os.path.join(source_directory, filename_ext_csv)
    filename_ext_json = 'real_' + str(i) + '.json'
    json_file_name = os.path.join(destination_directory, filename_ext_json)
    # Send only the first 2 columns; timestamp and value to be converted to json
    csvfile = open(csv_file_name, 'r')

    # Add the additional information at start
    with open(json_file_name, 'a') as the_file:
        the_file.write('{"granularity": "minutely","series": [')

    # Convert selected columns from csv to pandas dataframe
    df = pd.read_csv(csvfile, usecols=['timestamp', 'value'])

    # Convert pandas dataframe to json
    out = df.to_json(orient='records')[1:-1].replace('},{', '},\n {')
    with open(json_file_name, 'a') as f:
        f.write(out)

    # Add the additional information at the end
    with open(json_file_name, 'a') as the_file:
        the_file.write(']}')