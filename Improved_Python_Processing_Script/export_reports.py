###########################
# F333290 - H.Joshi        #
# Date Created: 23/07/2024 #
# Last Updated: 14/08/2024 #
###########################

'''
export_reports module

* This module is to be imported and executed in main.py. 
* This is the eighth step of the proteomics data processing pipeline.

The purpose of this module is to automate the export of PeptideShaker reports.
The user will be able to export a range of PeptideShaker reports without having to 
open the PeptideShaker GUI to do so. 

A new directory called 'reports' will need to be set up which will store the exported report(s) and reports.cli_log. 
The outputted '.psdb' file from the PeptideShaker process will be ran through the Report CLI to generate the
report(s) the user has requested. 

The exported report(s) are text files with tab delimiter by default.
As per user requirement, these files are then converted to Excel format and stored in the reports directory. 

Dependancies:
Two classes have been imported from previous modules: FolderStructure and PeptideShaker respectively.

Class:
Reports 

Methods:
 __init__(self, raw_dir, thermo_file_parser, reference_name) - Initialising the class Reports with raw_dir, thermo_file_parser, reference_name 
generate_reports() - Generating specified report(s) by executing the Report CLI
convert_report_type() - Converting exported report file(s) from '.txt' to '.xlsx' format 

Attributes:
self.folder_structure  - Instance of the class FolderStructure 
self.prepare_peptideshaker  - Instance of the class PeptideShaker 
self.java_executable (str) - Filepath for Java executable
self.peptide_shaker (str) - Filepath for PeptideShaker executable
self.reference_name (str) - User inputted name for the data
self.top_dir (str) - Top level directory in which all sub directories are located 
self.export_report_directory (str) - Filepath for the reports directory 
self.searched_directory (str) - Filepath for the searched directory  
self.reports_start_time (float) - Records the start time of this process
self.reports_end_time (float) - Records the end time of this process
'''

# Importing the required Python libraries for this module: 
import os
import sys
import subprocess
import logging
import time
import pandas as pd 

# Importing classes from previous modules
from folder_structure import FolderStructure
from prepare_peptideshaker import PeptideShaker

class Reports:
    '''
    The class Reports and its associated methods and attributes are used to export PeptideShaker reports into the reports directory.

    Methods:
    __init__(self, raw_dir, thermo_file_parser, reference_name) - For initialising the class Reports with raw_dir, thermo_file_parser, reference_name 
    generate_reports() - Generating specified report(s) by executing the Report CLI
    convert_report_type() - Converting the exported report file(s) from '.txt' to '.xlsx' format 

    Attributes:
    self.folder_structure  - Instance of the class FolderStructure 
    self.prepare_peptideshaker  - Instance of the class PeptideShaker 
    self.java_executable (str) - Filepath for Java executable
    self.peptide_shaker (str) - Filepath for PeptideShaker executable
    self.reference_name (str) - User inputted name for the data
    self.top_dir (str) - Top level directory in which all sub directories are located 
    self.export_report_directory (str) - Filepath for the reports directory 
    self.searched_directory (str) - Filepath for the searched directory  
    self.reports_start_time (float) - Records the start time of this process
    self.reports_end_time (float) - Records the end time of this process

    '''
    def __init__(self, raw_dir, thermo_file_parser, reference_name):
        '''
        Initialising the class Reports using raw_dir, thermo_file_parser and reference_name.

        Parameters:
        raw_dir (str) - Raw data directory 
        thermo_file_parser (str) -Thermo File Parser executable filepath
        reference_name (str) - Designated reference name for the data 

        Attributes:
        self.folder_structure  - Instance of the class FolderStructure 
        self.prepare_peptideshaker  - Instance of the class PeptideShaker 
        self.java_executable (str) - Filepath for Java executable
        self.peptide_shaker (str) - Filepath for PeptideShaker executable
        self.reference_name (str) - User inputted name for the data
        self.top_dir (str) - Top level directory in which all sub directories are located 
        self.export_report_directory (str) - Filepath for the reports directory 
        self.searched_directory (str) - Filepath for the searched directory  
        self.reports_start_time (float) - Records the start time of this process
        self.reports_end_time (float) - Records the end time of this process

        Raises:
        SystemExit - If the reports directory does not exist, then the module will terminate and log error message  
        '''
        
        self.folder_structure = FolderStructure()
        self.prepare_peptideshaker = PeptideShaker(raw_dir, thermo_file_parser, reference_name)
       
        self.java_executable = self.folder_structure.java_executable
        self.peptide_shaker = self.folder_structure.peptide_shaker
    
        self.reference_name = reference_name
        self.top_dir = os.getcwd()
        
        # Establishing the filepath to the reports directory within the top_dir 
        self.export_report_directory = os.path.join(self.top_dir, "reports")

        # Establishing the filepath to the searched directory as this is where the '.psdb' file is located 
        self.searched_directory = os.path.join(os.path.dirname(raw_dir), "searched")
        
        self.reports_start_time = None
        self.reports_end_time = None

        logging.info("==========")
        # Creating the reports directory to store the exported PeptideShaker report(s) 
        logging.info("Setting up the reports directory.")

        # Try-Except block for setting up the reports directory
        try:
            if not os.path.isdir(self.export_report_directory):
                os.makedirs(self.export_report_directory, exist_ok = True)
                logging.info(f"The following directory has been set up: {self.export_report_directory}")
            else:
                logging.info(f"The following directory already exists: {self.export_report_directory}")
        except:
            logging.error(f"The reports directory does not exist! Please create the reports directory.")
            sys.exit(1)

        
    def generate_reports(self):
        '''
        Function for generating the requested PeptideShaker reports using Report CLI. 
        The requested reports are currently set to "3" and "9" as per the reports_dict. 

        The '.psdb' file from the searched directory is used by Report CLI to export the the required report(s) from PeptideShaker. 

        The time taken for this process to run is recorded and appropriate 
        informational and/or error messages are logged at specific stages of this process.
        A reports_cli_log is also generated in the reports directory which logs the process and/or errors/exceptions if this process fails.

        The exported report(s) and the reports_cli_log are saved in the reports directory.  
        
        '''
        logging.info("Exporting requested PeptideShaker reports.")
        
        self.reports_start_time = time.time()

        # Dictionary of the reports that can be exported from PeptideShaker using Report CLI 
        reports_dict = {'0': "Certificate of Analysis",
                        '1': "Default Hierarchical Report", 
                        '2': "Default PSM Phosphorylation Report",
                        '3': "Default PSM Report", 
                        '4': "Default PSM Report with non-validated matches",
                        '5': "Default Peptide Phosphorylation Report",
                        '6': "Default Peptide Report",
                        '7': "Default Peptide Report with non-validated matches",
                        '8': "Default Protein Phosphorylation Report", 
                        '9': "Default Protein Report",
                       '10': "Default Protein Report with non-validated matches",
                       '11': "Extended PSM Report", 
                       '12': "-n: Your own custom reports"
        }
        
        # Establishing file path of the '.psdb' file in the searched directory
        psdb = os.path.join(self.searched_directory, f"{self.reference_name}.psdb")


        # Try-Except block for executing ReportCLI 
        # Using executables as set up in folder_structure.py and the '.psdb' file    
        try: 
            report_command = [self.java_executable, 
                              "-cp", self.peptide_shaker, 
                              "eu.isas.peptideshaker.cmd.ReportCLI",
                              "-in", psdb,
                              "-out_reports", self.export_report_directory,
                              "-reports", "3, 9",
            ]
            
            report_process = subprocess.run(report_command, capture_output = True, text = True, check = True)
            
             
            self.reports_end_time = time.time()
            
            logging.info(f"PeptideShaker reports have been successfully exported. The requested reports can be found in the reports directory.")


            # Creating a file called 'reports_cli_log' to log the export report process and any errors/execptions if this process fails
            with open(os.path.join(self.export_report_directory, "reports_cli.log"), "w") as outfile:
                outfile.write("Command line arguments\n")
                outfile.write("----------------------\n")
                outfile.write(" ".join(report_command))
                outfile.write("\n\nRun Log\n-------\n")
                outfile.write(report_process.stdout)
                outfile.write(report_process.stderr)
                

                logging.info("Log of the exported reports can be found in ./reports/reports_cli.log")

        except Exception as e:
            logging.error(f"Error found during the PeptideShaker Report Export process: {e}")


    def convert_report_type(self):
        '''
        Function for converting exported PeptideShaker report(s) from '.txt' to '.xlsx' format. 
        
        The report(s) by default are in '.txt' format and with tab delimiter.  
        The '.txt' file is put into a Pandas Dataframe and converted into an Excel file. 
        The Excel file is also stored in the reports directory. 

        Attributes:
        self.export_report_directory (str) - reports directory filepath
        '''
        # Creating a list of all the reports in '.txt' format in the reports directory
        file_list = [f for f in os.listdir(self.export_report_directory) if f.endswith('.txt')]
        
        for file in file_list:
            reports_file_path = os.path.join(self.export_report_directory, file)
            
            # Try-Except block for converting the file format of the report(s)
            try:
                # Tab Delimiter used  
                delimiter = '\t'

                # Creating a pandas Dataframe of the report(s)
                reports_df = pd.read_csv(reports_file_path, delimiter = delimiter)
                
                # Replacing the '.txt' with 'xlsx' and saving the dataframe as an Excel file
                excel_path = os.path.join(self.export_report_directory, file.replace('.txt', '.xlsx'))
                reports_df.to_excel(excel_path, index = False, engine = "openpyxl")
                logging.info(f"The file: {file} has been successfully converted to 'xlsx' format :{excel_path}")

            except Exception as e:
                logging.error(f"Error! The file: {file} has not been converted to 'xlsx' format:{e}")
            


if __name__=="__main__":
    
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The export_reports.py module is working!")


    


