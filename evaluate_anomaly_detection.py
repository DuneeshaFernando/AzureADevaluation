# Evaluate anomalies detected from Azure AD against labels provided by Yahoo
import os
import csv
from sklearn import metrics
import pandas
"""
Function to evaluate detection against actual labels.
"""
def evaluate_results(label_list,detection_list):
    print("Accuracy ", metrics.accuracy_score(label_list, detection_list))
    print("Precision ", metrics.precision_score(label_list, detection_list))
    print("Recall ", metrics.recall_score(label_list, detection_list))
    print("F1 Score ", metrics.f1_score(label_list, detection_list))
    print("Confusion matrix ", metrics.confusion_matrix(label_list, detection_list))
    try:
        print("AUC ", metrics.roc_auc_score(label_list, detection_list))
    except:
        print("AUC ", 0)

source_directory = 'DetectionResults/A1Benchmark'
original_directory = 'BenchmarkDatasets/processed_timeseries_csvs/A1Benchmark'
datasets_count = 2
detection_list=[]
label_list=[]
for i in range(1, datasets_count+1):
    output_filename = 'real_' + str(i) + '.csv'
    out_full_file_name = os.path.join(source_directory, output_filename)
    # Convert the content in csv file and append to list
    with open(out_full_file_name, newline='') as f:
        reader = csv.reader(f)
        sub_detection_list = list(reader)
    #for each element in the sub_detection_list, append to the detection_list
    for i in sub_detection_list:
        detection_list.append(int(i[0]))
    original_full_file_name = os.path.join(original_directory, output_filename)
    colnames = ['is_anomaly']
    anom_df = pandas.read_csv(original_full_file_name, names=colnames)
    sub_label_list = anom_df.is_anomaly.tolist()
    for i in sub_label_list[1:]:
        label_list.append(int(i))

# print(len(detection_list))
# print(label_list)
# print(len(label_list))
evaluate_results(label_list, detection_list)








