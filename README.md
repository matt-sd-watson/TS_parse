# **__TS_parse__**

**Note**: An update to the TapeStation analysis software as of April 23, 2019 includes a new feature to export data to a sample data to a simple csv, replacing TS_parse with new built-in functionalality TS_parse scripts can continue to be used for run reports generated from the TapeStation analysis software prior to April 23, 2019. 

TS_parse is a set of Python scripts that is dedicated to automated parsing of Agilent TapeStation 2200 quality control (QC) run reports for input into a LIMS system. These scripts have been written for both RNA samples going into NGS library prep as well as the final DNA/RNA libraries that are compatible with an NGS sequencing platform such as Illumina. The final CSV file output is compatible with auto-populating a customized open-source LIMS system such as MISO, developed by members of the Ontario Institute for Cancer Research (OICR) and created originally by the Earlham Institute. 

**Features of the script parser include**: 
  - Creation of a final standarized CSV file that can auto-populate a LIMS system with modifiable headers, with the ability to collect the     average base-pair insert size (for NGS libraries) or the RIN score and DV200 value (for RNA samples)
  - Ability to filter through common TapeStation 2200 assay errors such as expired screentapes, accidental sample missing from wells,           intentionally blank wells, and marker(s) not being detected (see instrument documentation for further information)
  - Retains the unique sample description input by the user into the assay
  - Maintains the original order of samples processed as input by the user, with the option for alphnumerical sorting in the CSV
  - Ability to use the corresponding concatenate files to merge multiple PDF parsing scans into one CSV, drastically reducing the time         needed to input many samples or libraries into a LIMS

**Additional Resources**

Agilent Tapestation 2200 instrument documentation: https://www.agilent.com/cs/library/usermanuals/public/G2964-90000_TapeStation_USR_ENU.pdf

MISO LIMS developed by OICR: http://tgac.github.io/miso-lims/
