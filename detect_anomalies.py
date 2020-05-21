# Send json files for anomaly detection and write the results to corresponding output files
# Execute the command source ~/.bash_profile before starting
import os
import requests
import json

"""
Sends an anomaly detection request to the Anomaly Detector API. 
If the request is successful, the JSON response is returned.
"""
# <request>
def send_request(endpoint, url, subscription_key, request_data):
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.post(endpoint+url, data=json.dumps(request_data), headers=headers)
    return json.loads(response.content.decode("utf-8"))
# </request>

"""
Detect if the latest data point in the time series is an anomaly.
"""
# <detectLatest>
def detect_latest(request_data):
    print("Determining if latest data point is an anomaly")
    # send the request, and print the JSON result
    result = send_request(endpoint, latest_point_detection_url, subscription_key, request_data)
    return result
    # print(json.dumps(result, indent=4))
# </detectLatest>

"""
Function to send data point by point to detect_latest.
"""
# <detectStream>
def detect_stream(request_data):
    points = request_data['series']
    granularity = request_data['granularity']
    skip_point = 13
    detection_list=[]
    for i in range(skip_point-1):
        detection_list.append(0)
    for i in range(skip_point, len(points)+1):
        single_sample_data = {}
        single_sample_data['series'] = points[0:i]
        single_sample_data['granularity'] = granularity
        single_point = detect_latest(single_sample_data)
        # print(type(single_point)) #dictionary
        # print(single_point)
        if (single_point['isAnomaly']):
            detection_list.append(1)
        else:
            detection_list.append(0)
    return detection_list
# </detectStream>

latest_point_detection_url = "/anomalydetector/v1.0/timeseries/last/detect"
endpoint = os.environ["ANOMALY_DETECTOR_ENDPOINT"]
subscription_key = os.environ["ANOMALY_DETECTOR_KEY"]

source_directory = 'BenchmarkDatasets/processed_jsons/A1Benchmark'
destination_directory = 'DetectionResults/A1Benchmark'
datasets_count = 67
for i in range(1, datasets_count+1):
    filename_ext_json = 'real_' + str(i) + '.json'
    json_file_name = os.path.join(source_directory, filename_ext_json)
    output_filename = 'real_' + str(i) + '.csv'
    out_full_file_name = os.path.join(destination_directory, output_filename)
    file_handler = open(json_file_name)
    json_data = json.load(file_handler)
    # Send to latest anomaly detector
    detection_list = detect_stream(json_data)
    with open(out_full_file_name, 'w') as f:
        for item in detection_list:
            f.write("%s\n" % item)
