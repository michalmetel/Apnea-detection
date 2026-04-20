from load_dataset import OSAData
import numpy as np



load=OSAData(r"C:\Users\PC\OneDrive\Pulpit\telemedycyna\Apnea-detection\data")
data=load.load_data()
data=data[0]
spo2=data["spo2"]
spo2_time=spo2["time"]
spo2_values=spo2["spo2"]
annotation=data["annotation"]
print(f"First 10 SpO2 values: {spo2_values[:10]}")
print(f"First 10 SpO2 times: {spo2_time[:10]}")
print(f"First 10 annotations: {annotation['events'][:10]}")
print(f"Record start: {annotation['record_start']}")



apnea_events=[]
for event in annotation['events']:
    if event['event_type']=='osa':
        start_time=event['evnet_start']
        duration=event['event_duration']
        end_time=start_time+duration
        print(f"Apnea event from {start_time} to {end_time}")
        apnea_events.append([start_time, end_time])
        break

