""" The Agilent Tapestation 2200 Controller and software package:
https://www.agilent.com/cs/library/usermanuals/public/G2964-90000_TapeStation_USR_ENU.pdf
provides essential laboratory QC information for samples prepared for NGS. The outputs from a Tapestation 2200
assay include a proprietary data analysis file that is encrypted, as well as the option to export all information
to a machine-readable PDF. This script provides the user with the ability to automatically parse the final run report
to extract all essential QC information into a standardized CSV for input into a LIMS system such as MISO, eliminating
the time required to extract information manually and limiting the possibility for user-generated error
"""

import tabula as tb
import glob
import pandas as pd
import PyPDF4 as pf
import os

# Parser will handle any errors from expired screentapes and failure to load samples into well
# IMPORTANT- error will still be caused if the marker in a single well was not detected (no table to read)


def rna_sample(filepath, page_start=4):

    """@Function Arguments:
    @filepath: the directory containing the pdf to parse
    @page_start: the page to begin parsing. For the majority of run reports, this value will correspond to page 4
    returns: a csv file containing the sample ID, RIN, and DV200 value of each RNA sample analyzed"""

    txt = glob.glob(filepath + '*.pdf')
    print(txt)

    for filename in txt:
        with open(filename, 'rb') as f:
            pdf = pf.PdfFileReader(f)
            number_of_pages = pdf.getNumPages()
        # avoid parsing pages that do not correspond to a sample electropherogram
        # requires selection of thumbnail electropherograms in analysis software when creating PDF
        pages = '%s-%s' % (page_start, number_of_pages)
        print(pages)

        df = tb.convert_into(filename, "qc_output.csv", output_format="csv", encoding='utf-8', pages=pages,
                         area = [636.278, 70.805, 688.341, 526.724], multiple_tables=True)
        df_2 = tb.convert_into(filename, "sample_id_output.csv", output_format="csv", encoding='utf-8',
                               pages=pages, area = [312.003,68.722,364.066,370.685], multiple_tables=True)

    fields_1 = ['Sample Description', 'RINe', 'Observations']
    fields_2 = ['% of Total']
    sample_id = pd.read_csv('sample_id_output.csv', skipinitialspace=True, usecols=fields_1)
    qc_data = pd.read_csv('qc_output.csv', skipinitialspace=True, usecols=fields_2)

    # ignore floats while parsing string list to identify marker failures
    id_list = [x for x in sample_id.Observations.tolist() if str(x) != 'nan']

    error_warnings = "Marker(s)"
    for list in id_list:
        if list.startswith(error_warnings):
            raise Exception('Error- one or more sample markers were not detected in the run. Please repeat the assay.')
    else:
        pass

    qc_df = pd.DataFrame(qc_data)
    id_df = pd.DataFrame(sample_id).drop(['Observations'], axis=1)

    # Drop empty rows produced from reading run reports with error warnings
    id_df_drop = id_df.dropna()
    id_dedup_reset = id_df_drop.reset_index(drop=True)
    id_df_dedup = id_dedup_reset[id_dedup_reset.index % 2 != 1]

    qc_df_dedup = qc_df[qc_df.index % 2 != 1]
    qc_dedup_reset = qc_df_dedup.reset_index(drop=True)
    id_df_final = id_df_dedup.reset_index(drop=True)

    data_merged = pd.concat([id_df_final, qc_dedup_reset], axis=1)

    # rename columns to be compatible with MISO LIMS auto-populate
    data_merged_rename = data_merged.rename(index=str, columns={"Sample Description": "Description", "RINe": 
        "RIN", "% of Total": "DV200"})

    # replace each null size value with empty string
    data_merged_rename[['DV200']] = data_merged_rename[['DV200']].fillna('')
    # re-order columns
    data_rename_sorted = data_merged_rename[['Description', 'RIN', 'DV200']]

    fields_3 = ['BLANK', 'Blank', 'blank', 'None', 'none', 'NA', 'N/A', 'n/a', 'Ladder', 'WATER', 'water']
    # Filter any sample wells that contain a description for an empty well
    data_master = data_rename_sorted[~data_rename_sorted['Description'].isin(fields_3)]
    pd.DataFrame(data_master).to_csv("TS_sample_qc_output.csv", index=False)
    print(data_master.to_string(index=False))

    os.remove('sample_id_output.csv')
    os.remove('qc_output.csv')
