from load_dataset import OSAData
import numpy as np



load=OSAData(r"C:\Users\PC\OneDrive\Pulpit\telemedycyna\Apnea-detection\data")
data=load.load_data()



for key, value in data.items():
    if key=='record_start':
        print(f"{key}: {value}")
        break
    print(f"{key}: {len(data[key])} samples")


print(data['annotation'][:5])

# OSA event -> Obstructive Sleep Apnea 
# Hypo event -> Hypopnea
# Both are classified as apneic events, but they have different characteristics.


Hypo_time=[]
OSA_time=[]

for event in data['annotation'][:5]:
    print(event)
    print(f"event: {event['event_type']}\n start:{event['evnet_start']} \n end:{event['evnet_start']+int(event['event_duration'])}")
    if event['event_type']=='osa':
        OSA_time.append([event['evnet_start'], event['evnet_start']+int(event['event_duration'])])
    else:
        Hypo_time.append([event['evnet_start'], event['evnet_start']+int(event['event_duration'])])
        
    
#For every event there are to values -> [[start,stop]] of event
apnea_events={
    'OSA events': OSA_time,
    'hypo_events':Hypo_time
    }

print(apnea_events)

spo2_val=data['spo2_values']
spo2_t=data['spo2_time']
print(f"First 5 samples: {spo2_val[:5]}\n First 5 time records: {spo2_t[:5]}")

start, end = 87171, 87189
event_spo2 = spo2_val[(spo2_t >= start) & (spo2_t <= end)]


for event in data['annotation'][1:3]:
    e_start = event['evnet_start']
    e_end = e_start + int(event['event_duration'])
    e_type = event['event_type']


    mask = (data['spo2_time'] >= e_start) & (data['spo2_time'] <= e_end + 30)
    event_spo2 = data['spo2_values'][mask]

    print(f"[{e_type.upper()}] start={e_start}, end={e_end}")
    print(f"SpO2: {event_spo2}")
    print(f"min={event_spo2.min():.1f}%  drop={event_spo2[0]-event_spo2.min():.1f}pp\n")