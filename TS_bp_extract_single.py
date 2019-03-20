""" The Agilent Tapestation 2200 Controller and software package:
https://www.agilent.com/cs/library/usermanuals/public/G2964-90000_TapeStation_USR_ENU.pdf
provides essential laboratory QC information for libraries created for NGS. The outputs from a Tapestation 2200
assay include a proprietary data analysis file that is encrypted, as well as the option to export all information
to a machine-readable PDF. This script provides the user with the ability to automatically parse the final run report
to extract all essential QC information into a standardized CSV for input into a LIMS system such as MISO, eliminating
the time required to extract information manually and limiting the possibility for user-generated error
"""

import tabula as tb
import glob
import pandas as pd
import PyPDF4 as pf
import csv
import os
import numpy as np

# Parser will handle any errors from expired screentapes and failure to load samples into well
# IMPORTANT- error will still be caused if the marker in a single well was not detected (no table to read)

path = 'X:\\mwatson\\run_reports_avg_bp\\'

txt = glob.glob(path+'2018-12-21*'+'*.pdf')
print(txt)

for filename in txt:
    with open(filename, 'rb') as f:
        pdf = pf.PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        # avoid parsing pages that do not correspond to a sample electropherogram
        # requires selection of thumbnail electropherograms in analysis software when creating PDF
    pages = '4-%s' % number_of_pages
    print(pages)

    df = tb.convert_into(filename, "qc_output.csv", output_format="csv", encoding='utf-8', pages=pages,
                         area = [636.278, 70.805, 688.341, 526.724], multiple_tables=True)
    df_2 = tb.convert_into(filename, "sample_id_output.csv", output_format="csv", encoding='utf-8',
                               pages=pages, area = [312.003,68.722,364.066,370.685], multiple_tables=True)

fields_1 = ['Sample Description']
fields_2 = ['Average Size [bp]']
sample_id = pd.read_csv('sample_id_output.csv', skipinitialspace=True, usecols=fields_1)
qc_data = pd.read_csv('qc_output.csv', skipinitialspace=True, usecols=fields_2)

qc_data_rename = qc_data.rename(index=str, columns={"Average Size [bp]":
    "size_bp"})
qc_data_to_list = qc_data_rename.size_bp.tolist()
id_df = pd.DataFrame(sample_id)

# Drop empty rows produced from reading run reports with error warnings
id_df_drop = id_df.dropna()
id_dedup_reset = id_df_drop.reset_index(drop=True)
id_df_dedup = id_dedup_reset[id_dedup_reset.index % 2 != 1]
id_df_final = id_df_dedup.reset_index(drop=True)


# remove alternating list elements starting at 1 to isolate numerical bp values
del qc_data_to_list[1::2]
qc_data_frame = pd.DataFrame({'size_bp': qc_data_to_list})


# treat dataframe as numerical to eliminate values corresponding to well failures
# no library detected in well will correspond to bp of 650 or greater
qc_data_frame.size_bp = qc_data_frame.size_bp.astype(int)
qc_data_frame[(qc_data_frame>650)] = np.nan

# replace false values over 650 with 'None'
qc_data_frame[['size_bp']] = qc_data_frame[['size_bp']].fillna(0).astype(int)
qc_data_frame[['size_bp']] = qc_data_frame[['size_bp']].replace([0], '')

data_merged = pd.concat([id_df_final, qc_data_frame], axis=1)

# rename columns to be compatible with MISO LIMS auto-populate
data_merged_rename = data_merged.rename(index=str, columns={"Sample Description": "Description", "size_bp":
    "Size (bp)"})

# Filter any sample wells that contain a description for an empty well
fields_3 = ['BLANK', 'Blank', 'blank', 'None', 'none', 'NA', 'N/A', 'n/a', 'Ladder', 'WATER', 'water', 'Water']
data_master = data_merged_rename[~data_merged_rename['Description'].isin(fields_3)]

# final CSV generated containing sample ID and bsp values
data_to_write = pd.DataFrame(data_master).to_csv("TS_bp_output_single.csv", index=False)
print(data_master.to_string(index=False))

os.remove("qc_output.csv")
os.remove("sample_id_output.csv")
