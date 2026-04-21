import os
import json
import pandas as pd
from glob import glob


class OSAData:
    def __init__(self, data_path: str):
        self.path_list = glob(os.path.join(data_path, "*"))
        self.patient_data = []

    @staticmethod
    def str2seconds(time_str: str) -> float:
        parts = time_str.split(":")
        h, m = map(int, parts[:2])

        s_part = parts[2]
        if '.' in s_part:
            s, ms = s_part.split('.')
            s = int(s)
            ms = float(f"0.{ms}")
        else:
            s = int(s_part)
            ms = 0.0

        if h < 12:
            h += 24

        return h * 3600 + m * 60 + s + ms

    @staticmethod
    def extract_event_annotations(file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def extract_spo2(spo_path, record_start):
    
        time_col = pd.read_csv(spo_path, usecols=[1]).iloc[:, 0]
        timestamps = time_col.apply(OSAData.str2seconds) - record_start

       
        value_col = pd.read_csv(spo_path, usecols=[2]).iloc[:, 0]
        values = [0 if x == '-' else float(x) for x in value_col]

        return {
            'time': timestamps.tolist(),
            'spo2': values
        }

    @staticmethod
    def load_single_patient(files: list):
        data = {
            "spo2": None,
            "annotation": None
        }

        record_start = None

     
        for file in files:
            if 'annotation' in file:
                ann = OSAData.extract_event_annotations(file)
                data["annotation"] = ann
                record_start = ann["record_start"]

  
        for file in files:
            if 'SpO2' in file:
                data["spo2"] = OSAData.extract_spo2(file, record_start)

        return data

    def load_data(self):
        for path in self.path_list:
            if os.path.isdir(path):
                files = glob(os.path.join(path, "*"))
                patient_data = self.load_single_patient(files)
                self.patient_data.append(patient_data)

        self.patient_data=self.patient_data[0]
        patient={
            'spo2_time': self.patient_data["spo2"]["time"],
            'spo2_values': self.patient_data["spo2"]["spo2"],
            'annotation': self.patient_data["annotation"]['events'],
            'record_start': self.patient_data["annotation"]["record_start"]
        }

        return patient 
    

