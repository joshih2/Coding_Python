###########################
# F333290 - H.Joshi        #
# Date Created: 11/07/2024 #
# Last Updated: 14/08/2024 #
###########################

'''
main.py module 

The purpose of this module is to execute all of the modules found in top_dir in sequential order 
followed by a brief summary of the whole process.

The whole process will be logged in the dia_umpire_automation.py file.

User interaction with this module is required in two parts:
- when setting up the absolute filepaths for the required executables and raw directory
- when executing main.py as per instructions in the associated README file


 Dependancies:
 Eight classes have been imported from previous modules:
 - FolderStructure
 - ConvertRawFiles
 - DiaUmpire
 - CleanFiles
 - MoveOutputFiles
 - SearchDatabase
 - PeptideShaker
 - Reports 


Class:
Summary

Methods:
 __init__(self, folder_structure, convert_raw_files, dia_umpire, search_database, prepare_peptideshaker, to_search, export_reports)
Initialising the class Summary with some of the modules required to log the summary and the files that were searched using SearchGUI

write_summary() - For logging a brief summary of the duration of key processes in this workflow 

Attributes: 
self.folder_structure - Instance of the class FolderStructure 
self.convert_raw_files - Instance of the class ConvertRawFiles
self.dia_umpire  - Instance of the class DiaUmpire 
self.search_database  - Instance of the class SearchDatabase
self.prepare_peptideshaker  - Instance of the class PeptideShaker 
self.to_search (list) - Files that have undergone SearchGUI database searching
self.export_reports - Instance of the class Reports  
'''

# Importing the required Python libraries for this module: 
import sys
import os
import logging
import time 

# Establishing the absolute filepath of top_dir
top_dir = os.path.dirname(os.path.abspath(__file__))

# Establishing the parent_dir filepath of top_dir
parent_dir = os.path.abspath(os.path.join(top_dir, os.pardir))

# Appending parent_dir to sys.path so that the modules for this pipeline can be found 
sys.path.append(parent_dir)


# Importing all modules from the Improved_Python_Processing_Script package
from Improved_Python_Processing_Script import folder_structure
from Improved_Python_Processing_Script import convert_raw_files
from Improved_Python_Processing_Script import dia_umpire
from Improved_Python_Processing_Script import clean_unneeded_files
from Improved_Python_Processing_Script import move_to_processed
from Improved_Python_Processing_Script import search_database
from Improved_Python_Processing_Script import prepare_peptideshaker
from Improved_Python_Processing_Script import export_reports

# Setting up the executables and raw_dir filepaths as environment variables 
# User interaction is required as the absolute filepaths for the executables and raw_dir need to be updated 
raw_dir = r"C:\Users\joshi\OneDrive - Loughborough University\Documents\Dissertation Project\Coding\Improved_Python_Processing_Script\raw"
thermo_file_parser = r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\resources\ThermoRawFileParser\ThermoRawFileParser.exe"
java_executable = r"C:\DIA_Umpire_Automation\java11\jre\bin\java.exe"
dia_umpire_se  = r"C:\DIA_Umpire_Automation\DIA_Umpire_SE-2.2.8.jar"
search_gui = r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\SearchGUI-4.2.17.jar"
peptide_shaker = r"C:\DIA_Umpire_Automation\PeptideShaker-2.2.25\PeptideShaker-2.2.25.jar"


class Summary:
     '''
       The class Summary and its associated methods and attributes are used to create the Summary section for the DIA_log_file.

       Method:
       __init__(self, folder_structure, convert_raw_files, dia_umpire, search_database, prepare_peptideshaker, to_search, export_reports)
       For initialising the class Summary with some of the modules required to log the summary and the files that were searched using SearchGUI
       
       write_summary() - For logging the brief summary once all modules have been executed 

       Attributes:
       self.folder_structure - Instance of the class FolderStructure 
       self.convert_raw_files - Instance of the class ConvertRawFiles
       self.dia_umpire  - Instance of the class DiaUmpire 
       self.search_database  - Instance of the class SearchDatabase
       self.prepare_peptideshaker  - Instance of the class PeptideShaker 
       self.to_search (list) - Files that have undergone SearchGUI database searching
       self.export_reports - Instance of the class Reports  
     '''
     def __init__(self, folder_structure, convert_raw_files, dia_umpire, search_database, prepare_peptideshaker, to_search, export_reports):
        '''
        Initialising the class Reports using specific modules and SearchGUI searched files to log the summary section of the DIA_log_file.

        Parameters & Attributes:
        self.folder_structure - Instance of the class FolderStructure 
        self.convert_raw_files - Instance of the class ConvertRawFiles
        self.dia_umpire  - Instance of the class DiaUmpire 
        self.search_database  - Instance of the class SearchDatabase
        self.prepare_peptideshaker  - Instance of the class PeptideShaker 
        self.to_search (list) - Files that have undergone SearchGUI database searching
        self.export_reports - Instance of the class Reports 
        '''
        
        self.folder_structure = folder_structure
        self.convert_raw_files = convert_raw_files
        self.dia_umpire = dia_umpire
        self.search_database = search_database
        self.prepare_peptideshaker = prepare_peptideshaker
        self.to_search = to_search
        self.export_reports = export_reports


     def write_summary(self):
        '''
        Function for logging a brief summary of key processes and their duration.
        This summary section will be logged after all all modules have been executed.  
       
        *These attributes are accessed using parameters/attributes list initiated in the Summary class.  
         Attributes:
         self.convert_raw_files.raw_files (list) - .raw files that have been converted successfully to .mzML
         self.dia_umpire.failed_files (list) - .mzML files that have failed DIA Umpire processing 
         self.convert_raw_files.files_to_convert (list) - .raw files that were to converted to .mzML
         self.folder_structure.script_start_time (float) - start time of the processing pipeline
         self.convert_raw_files.conversion_start_time (float) - start time of the file conversion process from .raw to .mzML
         self.convert_raw_files.conversion_end_time (float)  - end time of the file conversion process from .raw to .mzML 
         self.dia_umpire.umpire_start_time (float) - start time of the DIA Umpire process
         self.dia_umpire.umpire_end_time (float) - end time of the DIA Umpire process
         self.search_database.search_start_time (float) - start time of the SearchGUI database searching process
         self.search_database.search_end_time (float) - end time of the SearchGUI database searching process
         self.to_search (list) - accessing list of files that have been successfully searched by SearchGUI 
         self.prepare_peptideshaker.shaker_start_time (float) -  start time of the PeptideShaker process
         self.prepare_peptideshaker.shaker_end_time (float) -  end time of the PeptideShaker process
         self.export_reports.reports_start_time (float) - start time of export PeptideShaker reports process
         self.export_reports.reports_end_time (float) -  end time of the export PeptideShaker reports process 
        '''
       
       
        logging.info("============================")
        logging.info(" Summary")
        logging.info("============================")
        
        # Logging successfully processed files list 
        logging.info("Successfully processed:")
        if self.convert_raw_files.raw_files:
            logging.info("\n         ".join(self.convert_raw_files.raw_files))
        else:
            logging.info("No files processed successfully.")
        
        # If there are failed files , then these files are listed 
        if self.dia_umpire.failed_files:
             logging.info("Failed to process:")
             logging.info("\n         ".join(self.dia_umpire.failed_files))
             logging.info("==========")

        
    # If .raw files are successfully converted to .mzML, then the duration of the following subprocesses will be logged:
    # File conversion, DIA Umpire processing, SearchGUI database searching, PeptideShaker and exporting PeptideShaker reports 
        if self.convert_raw_files.files_to_convert:
            convert_run_time = self.convert_raw_files.conversion_end_time - self.convert_raw_files.conversion_start_time
            logging.info(f"Thermo RAW File Parser converted {len(self.convert_raw_files.files_to_convert)} files in {time.strftime('%M:%S', time.gmtime(convert_run_time))} mins:seconds")
            
            umpire_run_time = self.dia_umpire.umpire_end_time - self.dia_umpire.umpire_start_time
            logging.info(f"DIA Umpire processed {len(self.convert_raw_files.raw_files)} files in {time.strftime('%M:%S', time.gmtime(umpire_run_time))} mins:seconds")

            search_run_time = self.search_database.search_end_time - self.search_database.search_start_time
            logging.info(f"SearchGUI searched {len(self.to_search)} files in {time.strftime('%M:%S', time.gmtime(search_run_time))} mins:seconds") 
            
            shaker_run_time = self.prepare_peptideshaker.shaker_end_time - self.prepare_peptideshaker.shaker_start_time
            logging.info(f"PeptideShaker report generated in {time.strftime('%M:%S', time.gmtime(shaker_run_time))} mins:seconds")

            report_run_time = self.export_reports.reports_end_time - self.export_reports.reports_start_time
            logging.info(f"Peptideshaker reports exported in {time.strftime('%M:%S', time.gmtime(report_run_time))} mins:seconds")
            
            # Logging the total time taken for the whole process to run
            # Date & Timestamp of the process for user reference 
            script_end_time = time.time()
            total_time = script_end_time - self.folder_structure.script_start_time
            logging.info(f"Total time taken for the whole process = {time.strftime('%H:%M:%S', time.gmtime(total_time))} hours:mins:seconds")
            logging.info(f"Date & Time of when the process finished:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(script_end_time))}")
           
           
           
            

    
def main():
    '''
    All of the eight modules created for the proteomic data processing pipeline will be executed in sequential order. 
    All of the methods, attributes, parameters and variables associated with each class will be utilised.
    For detailed explanation of each modules, please refer to each individual module docstrings and comments. 
    
    Finally, a summary section will be printed which will log the duration of key processes in the workflow. 
    
    The process will be logged in the 'dia_umpire_automation.log'.
    '''
    
    # Setting up required directories, executables, parameters and logging configuration 
    # Setting up user prompt to input reference name 
    folder_structure_module = folder_structure.FolderStructure()
    folder_structure_module.logging_setup()
    folder_structure_module.directory_setup()
    folder_structure_module.executable_setup()
    folder_structure_module.parameter_check()
    folder_structure_module.reference_name_setup()

    reference_name = folder_structure_module.reference_name  

    # Using Thermo File Parser to convert .raw files to .mzML format
    convert_raw_files_module = convert_raw_files.ConvertRawFiles(raw_dir,thermo_file_parser)
    convert_raw_files_module.identify_raw_files()
    convert_raw_files_module.convert_raw_files()
    convert_raw_files_module.check_converted_raw_files()
    convert_raw_files_module.retrieve_raw_file_count()

    # DIA Umpire processing on the .mzML files 
    dia_umpire_module = dia_umpire.DiaUmpire(convert_raw_files_module)
    dia_umpire_module.dia_file_processing()

    # Uneeded files generated during DIA Umpire processing are cleaned and removed from raw directory 
    clean_unneeded_files_module = clean_unneeded_files.CleanFiles()
    clean_unneeded_files_module.cleaning_process(raw_dir)

    # Other required files generated during DIA Umpire processing are moved from raw directory to processed directory 
    move_to_processed_module = move_to_processed.MoveOutputFiles(raw_dir,convert_raw_files_module)
    move_to_processed_module.move_to_processed()
    
    # '.mgf' files are concatenated with selected QT tier which are used for SearchGUI protein database searching 
    search_database_module = search_database.SearchDatabase(raw_dir, thermo_file_parser, reference_name)
    search_database_module.update_raw_names()

    to_search = search_database_module.search_process()  
    
    # Using PeptideShaker to visualise and analyse the SearchGUI database search outputs  
    prepare_peptideshaker_module = prepare_peptideshaker.PeptideShaker(raw_dir,thermo_file_parser, reference_name)
    prepare_peptideshaker_module.peptideshaker_process(to_search)

    # Exporting requested PeptideShaker reports without having to open PeptideShaker GUI to do so 
    export_reports_module = export_reports.Reports( raw_dir, thermo_file_parser, reference_name)
    export_reports_module.generate_reports()
    export_reports_module.convert_report_type()

    # Initialising the Class Summary with instances of classes from some of the modules and the to_search list 
    summary = Summary(
        folder_structure = folder_structure_module,
        convert_raw_files = convert_raw_files_module,
        dia_umpire = dia_umpire_module,
        search_database = search_database_module,
        prepare_peptideshaker = prepare_peptideshaker_module,
        to_search = to_search,export_reports = export_reports_module
    )
    
    # Logging the duration of some key processes in the workflow
    summary.write_summary()

if __name__ == "__main__":
    main()


