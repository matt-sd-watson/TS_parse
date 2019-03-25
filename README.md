# TS_parse

Python scripts dedicated to automated parsing of Agilent TapeStation 2200 run reports for input into a LIMS system. Scripts 
have been written for both RNA samples going into NGS library prep as well as final DNA/RNA libraries that are compatible with an NGS 
sequencing platform such as Illumina. The final CSV file output is compatible with auto-populating a customized LIMS system created through MISO by members of the Ontario Institute for Cancer Research (OICR): http://tgac.github.io/miso-lims/


Features of the script parser include: 
  - Creation of a final standarized CSV file that can auto-populate a LIMS system with modifiable headers
  - Ability to filter through common TapeStation 2200 assay errors such as expired screentapes, samples missing from wells, and marker(s)       not being detected
  - Retains the unique sample description input by the user into the assay

Agilent Tapestation 2200 documentation: https://www.agilent.com/cs/library/usermanuals/public/G2964-90000_TapeStation_USR_ENU.pdf
