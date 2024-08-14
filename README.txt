Proteomics Data Processing Pipeline
===================================

For more information about this project, please contact: 
Dr. Amanda Pearce 
Pearce Polymer Lab
Loughborough University 
Email: a.pearce@lboro.ac.uk

This code has been adapted from the following code written by Dr. Jedd Bellamy-Carter - Loughborough University:
https://github.com/jbellamycarter/DIA-Umpire_SearchGUI_automation

This proteomics data processing pipeline was created as part of an MSc Data Science Project by:
Hetal Joshi - Loughborough University

===================================

In this project, there is a folder called Improved_Python_Processing_Script. 
It contains the directories, parameter files, python modules, __init__.py, main.py, requirements.txt, __pycache__ and README file. 

There are 8 modules which have been created and put into a package as seen in __init__.py file:
 - folder_structure.py
 - convert_raw_files.py
 - dia_umpire.py
 - clean_unneeded_files.py
 - move_to_processed.py
 - search_database.py
 - prepare_peptideshaker.py
 - export_reports.py 

These modules are imported into main.py and executed in an sequential order. 

For successful execution of the workflow, users will need to ensure the following: 

*Python 3.7 or higher installed 

1. Update Executables locations
Before executing main.py, ensure that the executable locations in folder_structure.py and main.py are accurate. 

Default absolute filepaths for the executables are: 
self.java_executable = r"C:\DIA_Umpire_Automation\java11\jre\bin\java.exe";
self.dia_umpire_se = r"C:\DIA_Umpire_Automation\DIA_Umpire_SE-2.2.8.jar";
self.search_gui =  r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\SearchGUI-4.2.17.jar";
self.peptide_shaker =  r"C:\DIA_Umpire_Automation\PeptideShaker-2.2.25\PeptideShaker-2.2.25.jar";
self.thermo_file_parser =  r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\resources\ThermoRawFileParser\ThermoRawFileParser.exe"

2. Copy .raw files into the raw directory
If the raw directory does not exist, then folder_structure.py terminates and so the processed and searched directories cannot be created. 

3. Update Parameter files in folder_structure.py
Three parameters files are required: 
self.DIA_Umpire_Parameters : umpire_se.params
self.SearchGUI_Parameters : search_par 
self.FASTA_Database : database.fasta 

4. When prompted to write the reference name for the data, ensure that names are joined by an underscore (_)
e.g. reference_name 

5. Ensure that the absolute filepath for the raw directory is used in main.py.   

6. Run main.py in command prompt using the following Windows commands:
   Copy and paste the current filepath of your current directory e.g. cd "C:\Users\joshi\Documents\Project\Coding" 
   Then press Enter
   Activate the virtual environment by copying and pasting this command into the command prompt: .\venv\Scripts\Activate
   Then press Enter
   Copy and paste the absolute filepath to where the modules are located e.g. cd "C:\Users\joshi\Documents\Project\Coding\Improved_Python_Processing_Script"
   Then press Enter
   Type in 'python main.py' and press enter; the script will be executed. 











