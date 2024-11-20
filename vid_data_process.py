import pandas as pd
import numpy as np
import os

# list all the files in the directory
file_list = os.listdir('data')

pid_list = []
response_time_list = []
takeover_duration_list = []
fix_type_list = []
fix_duration_before_takeover_list = []

for file in file_list:
    if file.endswith('.csv'):
        pid = int(file.split('_')[1][:2])
        print(pid,"started")
        # read the csv file
        df = pd.read_csv('data/' + file)
        if 'Behavior' not in df.columns:
            print(pid, "no data")
            continue
        df = df[['Behavior','Behavior type','Time']]
        
        response_time = df[(df['Behavior'] == "Driver's Takeover") & (df['Behavior type'] == "START")]['Time'].values[0] - df[df['Behavior'] == "Takeover Warning"]['Time'].values[0]
        takeover_duration = df[(df['Behavior'] == "Driver's Takeover") & (df['Behavior type'] == "STOP")]['Time'].values[0] - df[(df['Behavior'] == "Driver's Takeover") & (df['Behavior type'] == "START")]['Time'].values[0]
        
        takeover_index = df[(df['Behavior'] == "Driver's Takeover") & (df['Behavior type'] == "START")].index
        fix_type = df.loc[takeover_index-1]['Behavior'].values[0] # Fixation type right before Takeover Warning
        if fix_type == 'Fixation-Road':
            if df.loc[takeover_index-1]['Behavior type'].values[0] == 'START':
                fix_duration_before_takeover = df.loc[takeover_index]['Time'].values[0] - df.loc[takeover_index-1]['Time'].values[0]
            else:
                fix_duration_before_takeover = df.loc[takeover_index-1]['Time'].values[0] - df.loc[takeover_index-2]['Time'].values[0]
        else:
            fix_duration_before_takeover = "NA"
        
        pid_list.append(pid)
        response_time_list.append(round(response_time,4))
        takeover_duration_list.append(round(takeover_duration,4))
        fix_type_list.append(fix_type)
        fix_duration_before_takeover_list.append(fix_duration_before_takeover)
        print(pid, "done")

new_df = pd.DataFrame({'PID': pid_list, 'Response Time': response_time_list, 'Takeover Duration': takeover_duration_list, 'Fixation Type': fix_type_list, 'Fixation Duration Before Takeover': fix_duration_before_takeover_list})
new_df.to_csv('output.csv', index=False)

# Driver's Takeover start - Takeover Warning
# Driver's Takeover duration
# Fixation type right before Takeover Warning
# Fixation duration right before Takeover Warning
