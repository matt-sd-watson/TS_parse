""" The script file TS_parse_NGS_library_single enables the user to extract the bp insert size and sample description
from a Tapestation 2200 PDF run report containing NGS libraries. This additional file gives the ability to concatenate multiple parsing
runs from this parser in order to develop a final CSV that contains libraries from multiple TS assays
"""

from TS_parse_NGS_library_single import data_master
import csv
import pandas as pd
import os

# Check to see if the concatenating file exists. Pass if exists, or create an empty file to combine multiple parsing
# runs. IMPORTANT- before concatenating a new set of runs, delete the old file.
exists = os.path.isfile('TS_parse_concatenate_library.csv')
if exists:
    pass

else:
    with open('TS_parse_concatenate_library.csv', 'w') as make:
        make
        pass

with open('TS_parse_concatenate_library.csv', 'r') as read:
    # Search the CSV file for contents. If file is empty, write column headers that are compatible for MISO (newline
    # to eliminate empty rows between values)
    read.seek(0)
    first_char = read.read(1)  # establish file contents by seeking first character
    if not first_char:
        with open('TS_parse_concatenate_library.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["Description", "Size (bp)"])
    else:
        pass

# Append the dataframe to the existing CSV to concatenate multiple parsing runs without repeating column headers
with open('TS_parse_concatenate_library.csv', 'a', newline='') as add:
    writer = csv.writer(add)
    pd.DataFrame(data_master).to_csv(add, header=False, index=False)
