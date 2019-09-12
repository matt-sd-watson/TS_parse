import glob
import pandas as pd
import csv
import os
import numpy as np
import chardet as cht

def concatenate_outputs(filepath): 

    data_files = glob.glob(filepath+ '*.csv')

    master_data = []

    for filename in data_files:
        with open (filename, 'rb') as f:
            # establish file encoding type before csv reading to allow merging
            result = cht.detect(f.read())
            csv_read = pd.read_csv(filename, skipinitialspace=True, usecols=['Sample Description', 'Average Size [bp]'],
                           encoding=result['encoding'])
            master_data.append(csv_read)

    final_frame = pd.concat(master_data, axis=0, ignore_index=True)

    master_data_rename = final_frame.rename(index=str, columns={"Sample Description": "Description", "Average Size [bp]":
        "Size (bp)"})

    # Filter any sample wells that contain a description for an empty well
    fields_to_remove = ['BLANK', 'Blank', 'blank', 'None', 'none', 'NA', 'N/A', 'n/a', 'Ladder', 'WATER',
                    'water', 'Water']
    master_data_filtered = master_data_rename[~master_data_rename['Description'].isin(fields_to_remove)]

    data_to_write = master_data_filtered.to_csv("NGS_library_merged.csv", index=False)
    print(master_data_filtered.to_string(index=False))
