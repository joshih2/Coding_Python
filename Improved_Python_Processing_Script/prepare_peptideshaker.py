###########################
# F333290 - H.Joshi        #
# Date Created: 08/07/2024 #
# Last Updated: 14/08/2024 #
###########################


'''
prepare_peptideshaker module

* This module is to be imported and executed in main.py. 
* This is the seventh step of the proteomics data processing pipeline.

The purpose of this module is to automate the generation of the PeptideShaker report ('.psdb' file)
using PeptideShakerCLI on the files in the searched_directory.
An outfile called shaker_cli_log is also created and a '.html' file that is created 
during this process but which is not required is then removed. 
  
Dependancies:
Two classes have been imported from previous modules: FolderStructure and SearchDatabase respectively.


Class:
PeptideShaker

Methods:
__init__(self, raw_dir, thermo_file_parser, reference_name) - Initialising the class PeptideShaker with raw_dir, thermo_file_parser, reference_name 
peptideshaker_process(to_search) - Using searched files to generate a 'psdb' file via PeptideShakerCLI 

Attributes:
self.folder_structure - Instance of the class FolderStructure 
self.search_database  - Instance of the class SearchDatabase 
self.java_executable (str) - Filepath for Java executable
self.peptide_shaker (str) - Filepath for PeptideShaker executable
self.SearchGUI_Parameters (str) - Filepath for the search_par file
self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
self.reference_name (str) - User inputted name for the data   
self.searched_directory (str) - Filepath for the searched directory  
self.shaker_start_time (float) - Records the start time of the PeptideShaker process
self.shaker_end_time (float) - Records the start time of the PeptideShaker process
'''

# Importing the required Python libraries for this module: 
import os
import subprocess
import fnmatch
import time
import logging

# Importing classes from previous modules: 
from folder_structure import FolderStructure
from search_database import SearchDatabase

class PeptideShaker:
    '''
    The class PeptideShaker and its associated methods and attributes are used to generate a PeptideShaker file. 

    Methods:
    __init__(self, raw_dir, thermo_file_parser, reference_name) - For initialising the class PeptideShaker with raw_dir, thermo_file_parser, reference_name 
    peptideshaker_process(to_search) - Generating a 'psdb' file by executing PeptideShakerCLI 


    Attributes:
    self.folder_structure - Instance of the class FolderStructure 
    self.search_database  - Instance of the class SearchDatabase 
    self.java_executable (str) - Filepath for the Java executable
    self.peptide_shaker (str) - Filepath for the PeptideShaker executable
    self.SearchGUI_Parameters (str) - Filepath for the search_par file
    self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
    self.reference_name (str) - User inputted name for the data   
    self.searched_directory (str) - Filepath for the searched directory  
    self.shaker_start_time (float) - Records the start time of the PeptideShaker process
    self.shaker_end_time (float) - Records the start time of the PeptideShaker process
    '''
    def __init__(self, raw_dir, thermo_file_parser, reference_name):
        '''
        Initialising the class PeptideShaker using raw_dir, thermo_file_parser and reference_name.

        Parameters:
        raw_dir (str) - Raw data directory 
        thermo_file_parser (str) -Thermo File Parser executable filepath
        reference_name (str) - Designated reference name for the data 

        Attributes:
        self.folder_structure - Instance of the class FolderStructure 
        self.search_database  - Instance of the class SearchDatabase 
        self.java_executable (str) - Filepath for the Java executable
        self.peptide_shaker (str) - Filepath for the PeptideShaker executable
        self.SearchGUI_Parameters (str) - Filepath for the search_par file
        self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
        self.reference_name (str) - User inputted name for the data   
        self.searched_directory (str) - Filepath for the searched directory  
        self.shaker_start_time (float) - Records the start time of the PeptideShaker process
        self.shaker_end_time (float) - Records the start time of the PeptideShaker process
        '''

        self.folder_structure = FolderStructure() 
        self.search_database = SearchDatabase(raw_dir, thermo_file_parser, reference_name)
        
        self.java_executable = self.folder_structure.java_executable
        self.peptide_shaker = self.folder_structure.peptide_shaker
        self.SearchGUI_Parameters = self.folder_structure.SearchGUI_Parameters 
        self.FASTA_Database = self.folder_structure.FASTA_Database 

        self.reference_name = reference_name 

        self.searched_directory = os.path.join(os.path.dirname(raw_dir), "searched")
       
        self.shaker_start_time = None
        self.shaker_end_time = None

    
    def peptideshaker_process(self, to_search):
        '''
        Function for running the PeptideShaker process via PeptideShaker CLI.

        Searched files in the to_search list are used to generate the '.psdb' file.
        A '.html' file that is not required but automatically generated from this process is then removed. 
        
        The time taken for this process to run is recorded and appropriate 
        informational and/or error messages are logged at specific stages of this process.
        A shaker_cli_log is also generated in the search directory which logs the process and/or errors/exceptions if this process fails. 

        Parameter:
        to_search (list) - Files that have been searched using SearchGUI CLI are used as the input for
                           the PeptideShaker CLI to generate the '.psdb' file 

        Attributes:
        self.java_executable (str)  - filepath for Java executable
        self.peptide_shaker (str) - filepath for PeptideShaker executable
        self.reference_name (str) - user inputted name for the data
        self.FASTA_Database (str) - filepath for the database.fasta parameter file
        self.SearchGUI_Parameters (str) - filepath for the search_par file
        self.searched_directory (str) - filepath for searched directory 
        self.shaker_start_time (float) - Records start time of the process 
        self.shaker_end_time (float) - Records end time of the process 
        '''
        
        logging.info("==========")
        logging.info("Preparing the PeptideShaker file.")
         
        self.shaker_start_time = time.time()

        # Try-Except block for executing PeptideShakerCLI 
        # Using directory, executables, parameters and reference name as set up in folder_structure.py   
        try:
            # Checking that the searched directory exists
            os.makedirs(self.searched_directory, exist_ok=True)
      
            shaker_command = [self.java_executable, "-cp", 
                              self.peptide_shaker, "eu.isas.peptideshaker.cmd.PeptideShakerCLI",
                              "-reference", self.reference_name,
                              "-identification_files", os.path.join(self.searched_directory, self.reference_name+".zip"),
                              "-spectrum_files", ', '.join(to_search),
                              "-fasta_file", self.FASTA_Database,
                              "-id_params", self.SearchGUI_Parameters,
                              "-out", os.path.join(self.searched_directory, f"{self.reference_name}.psdb")
            ]

            
            shaker_process = subprocess.run(shaker_command, capture_output = True, text = True, check = True)

            self.shaker_end_time = time.time()
                
            logging.info(f"Import complete, results can be found in ./searched/{self.reference_name}.psdb")
            
            # Creating a file called 'shaker_cli_log' to log the PeptideShaker process and any errors/execptions if this process fails
            with open(os.path.join(self.searched_directory, "shaker_cli.log"), "w") as outfile:
              outfile.write("Command line arguments\n")
              outfile.write("----------------------\n")
              outfile.write(" ".join(shaker_command))
              outfile.write("\n\nRun Log\n-------\n")
              outfile.write(shaker_process.stdout)
              outfile.write(shaker_process.stderr)
              
            logging.info("Log can be found in ./searched/shaker_cli.log")
              
            # Removing a .html file automatically generated by this process from the search directory 
            for f in fnmatch.filter(os.listdir(self.searched_directory), "PeptideShaker*.html"):
                os.remove(os.path.join(self.searched_directory, f))
        
        except Exception as e:
            logging.error(f"Error found during the Peptideshaker process: {e}")




if __name__=="__main__":
    
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The prepare_peptideshaker.py module is working!")

