# **__TS_parse__**

Python scripts dedicated to automated parsing of Agilent TapeStation 2200 quality control (QC) run reports for input into a LIMS system. Scripts have been written for both RNA samples going into NGS library prep as well as final DNA/RNA libraries that are compatible with an NGS sequencing platform such as Illumina. The final CSV file output is compatible with auto-populating a customized LIMS system created through MISO by members of the Ontario Institute for Cancer Research (OICR) and the Earlham Institute: http://tgac.github.io/miso-lims/

**Features of the script parser include**: 
  - Creation of a final standarized CSV file that can auto-populate a LIMS system with modifiable headers, with the ability to collect the     average base-pair insert size (NGS libraries) or RIN score and DV200 (RNA samples)
  - Ability to filter through common TapeStation 2200 assay errors such as expired screentapes, accidental sample missing from wells,           intentionally blank wells, and marker(s) not being detected
  - Retains the unique sample description input by the user into the assay
  - Maintains the original order of samples processed as input by the user, with the option for alphnumerical sorting in the CSV
  - Ability to use the corresponding concatenate files to merge multiple PDF scans into one CSV

Agilent Tapestation 2200 instrument documentation: https://www.agilent.com/cs/library/usermanuals/public/G2964-90000_TapeStation_USR_ENU.pdf
