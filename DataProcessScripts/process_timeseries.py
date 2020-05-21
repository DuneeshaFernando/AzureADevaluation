# Convert the original datasets in Yahoo yws5 to timeseries data
# Execute this file from project root
import pandas as pd
import os
# Get a csv with actual timestamps
time_df = pd.read_csv('long_time_series.csv')
new_time_df = time_df[['timestamp']].copy()

source_directory = "BenchmarkDatasets/yws5/A1Benchmark/"
destination_directory = 'BenchmarkDatasets/processed_timeseries_csvs/A1Benchmark'
datasets_count = 67
for i in range(1, datasets_count+1):
    filename = 'real_'+str(i)+'.csv'
    full_path = os.path.join(source_directory, filename)
    print(full_path)
    df = pd.read_csv(full_path)
    new_df = df[['value', 'is_anomaly']].copy()
    final_df = pd.merge(new_time_df, new_df, left_index=True, right_index=True)
    final_full_path = os.path.join(destination_directory, filename)
    final_df.to_csv(final_full_path, index=False)
