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
        
    

apnea_events={
    'OSA events': OSA_time,
    'hypo_events':Hypo_time
    }

print(apnea_events)