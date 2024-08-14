###########################
# F333290 - H.Joshi        #
# Date Created: 14/06/2024 #
# Last Updated: 14/08/2024 #
###########################

'''
folder_structure Module 

* This module is to be imported and executed in main.py. 
* This is the first step in the process of converting raw mass spectra files into an 
  analysable output which can be viewed in PeptideShaker.

The purpose of this module is to automate the set up of the required directories, 
executables, parameters,logging messages and reference name for the data.
If the various elements of the folder structure are not present, then appropriate error 
and/or informational messages will be logged before either continuing or exiting the module. 

User interaction with this module is required at two stages:
 - when setting up the executables
 - when the user executes main.py, they will be prompted to input a suitable reference name 

Class: 
FolderStructure

Methods:
__init__(self, DIA_log_file = "dia_umpire_automation.log") - For initialising the class with the DIA_log_file 
self.directory_setup() - For creating the required directories
self.executable_setup() - For setting up the required executables
self.parameter_check() - For setting up the three parameter files 
self.reference_name_setup() - To allow user to input a reference name for the data
self.logging_setup() - Setting up the logging file and logging configuration to use throughout the whole pipeline

Attributes: 
self.top_dir (str) - Top level directory in which all sub directories are located 
self.log_file (str) - Log file created for logging the whole process 
self.script_start_time (float) - Records the start time of the processing pipeline
self.reference_name (str) - User inputted reference name for the data 
self.raw_dir (str) - Location of the raw data 
self.java_executable (str) - Filepath for the Java executable
self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
self.search_gui (str) - Filepath for the SearchGUI executable 
self.peptide_shaker (str) - Filepath for the Peptideshaker executable
self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file
self.SearchGUI_Parameters (str) - Filepath for the search_par file
self.FASTA_Database (str)  - Filepath for the database.fasta parameter file


Exceptions:
PermissionError - Occurs when the DIA_log_file is in use and so cannot be deleted 
SystemExit - Occurs when either the directories, executables or parameter files have not been set up properly 
'''

# Importing the required Python libraries for this module: 
import os
import sys
import time
import logging
 
class FolderStructure:
    '''
    The class FolderStructure and its associated methods and attributes are used 
    for setting up the directories, executables and parameters required for this proteomic data processing pipeline. 

    Methods:
    __init__(self, DIA_log_file = "dia_umpire_automation.log") - For initialising the class with the DIA_log_file 
    self.directory_setup() - For creating the required directories
    self.executable_setup() - For setting up the required executables
    self.parameter_check() - For setting up the three parameter files 
    self.reference_name_setup() - To allow the user to input a reference name for the data
    self.logging_setup() - Setting up the logging file and logging configuration to use 
    
    Attributes:
    self.top_dir (str) - Top level directory in which all sub directories are located 
    self.log_file (str) - Log file created for logging the whole process 
    self.script_start_time (float) - Records the start time of the processing pipeline
    self.reference_name (str) - User inputted reference name for the data 
    self.raw_dir (str) - Location of the raw data 
    self.java_executable (str) - Filepath for the Java executable
    self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
    self.search_gui (str) - Filepath for the SearchGUI executable 
    self.peptide_shaker (str) - Filepath for the Peptideshaker executable
    self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
    self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file
    self.SearchGUI_Parameters (str) - Filepath for the search_par file
    self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
    '''
    def __init__(self, DIA_log_file = "dia_umpire_automation.log"):
        '''
        For establishing the required directories, executables and parameters.
        
        Argument:
        DIA_log_file (str) - Name of the log file (already preset to 'dia_umpire_automation.log') used for logging the process 

        Attributes:
        self.top_dir (str) - Top level directory in which all sub directories are located 
        self.log_file (str) - Log file created for logging the whole process 
        self.script_start_time (float) - Records the start time of the processing pipeline
        self.reference_name (str) - User inputted reference name for the data 
        self.raw_dir (str) - Location of the raw data 
        self.java_executable (str) - Filepath for the Java executable
        self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
        self.search_gui (str) - Filepath for the SearchGUI executable 
        self.peptide_shaker (str) - Filepath for the Peptideshaker executable
        self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
        self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file
        self.SearchGUI_Parameters (str) - Filepath for the search_par file
        self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
        '''
        
        self.top_dir = os.getcwd()
        self.log_file = DIA_log_file
        self.script_start_time = time.time()
        self.reference_name = None 
        
        self.raw_dir = None
        
        
        # User is required to update the executables filepath to the actual location using the absolute path 
        self.java_executable = r"C:\DIA_Umpire_Automation\java11\jre\bin\java.exe";
        self.dia_umpire_se = r"C:\DIA_Umpire_Automation\DIA_Umpire_SE-2.2.8.jar";
        self.search_gui =  r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\SearchGUI-4.2.17.jar";
        self.peptide_shaker =  r"C:\DIA_Umpire_Automation\PeptideShaker-2.2.25\PeptideShaker-2.2.25.jar";
        self.thermo_file_parser =  r"C:\DIA_Umpire_Automation\SearchGUI-4.2.17\resources\ThermoRawFileParser\ThermoRawFileParser.exe"
        
        # Creating filepaths for each parameter file in top_dir 
        self.DIA_Umpire_Parameters = os.path.join(self.top_dir, "umpire-se.params")
        self.SearchGUI_Parameters = os.path.join(self.top_dir, "search.par")
        self.FASTA_Database = os.path.join(self.top_dir, "database.fasta")


    def logging_setup(self):
        '''
        Function for setting up the logging configuration for all the modules and for DIA_log_file.
        Logging messages are printed to both the DIA_log_file and the console. 

        Creates the DIA_log_file path and checks whether the log file exists. 
        If it exists, then DIA_log_file is removed. 
        If it is being used, then it cannot be deleted. 

        Logs informational messages about top_dir and the start time of the processing pipeline. 

        Raises:
        PermissionError -  When DIA_log_file is being used, it cannot be deleted. 
        '''
        
        log_file = os.path.join(self.top_dir, self.log_file) 
        # If DIA_log_file exists, then it is removed
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            # If it is being used, then DIA_log_file cannot be deleted
            except PermissionError:
                logging.warning(f"{log_file} cannot be deleted. This file is currently being used in another process.")


        # Setting up the logging format for both the DIA_log_file and the console         
        logging.basicConfig(
            level = logging.INFO,
            format = "%(levelname)-8s %(message)s",
            handlers = [ 
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Logging messages to inform user of where the top_dir is and the start time of the pipeline
        logging.info(f"Script started {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.script_start_time))}")
        logging.info(f"Top directory is {self.top_dir}")
        
        
        # Calculating the total time taken to execute all modules and main.py
        # Used in main.py when logging the summary section of DIA_log_file
        self.log_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.script_start_time))


    def directory_setup(self):
        '''
        Function for setting up raw, processed and searched directories within top_dir.

        The raw directory is set up. 
        If it exists, then a logging message is printed informing the user.
        If it does not exist, then error message is printed and exits the module. 
        Note: If raw directory does not exist, then processed and searched directories cannot be created.  

        The processed and search directories are also set up and checked for whether they exist or not (logs message if exist). 
        If these two directories do not exist, then they are created and the user is informed through logging messages. 

        Attributes:
        self.top_dir (str) - top_dir filepath 
        self.raw_dir (str) - raw_dir filepath (contains the raw data)

        Raises:
        SystemExit - If the raw directory does not exist, then the module will terminate and log error message  
        '''
        logging.info("Setting up the working directories.")
        # Setting up raw directory within top_dir
        self.raw_dir = os.path.join(self.top_dir,"raw")
        # Checking and logging that raw directory has been set up 
        if os.path.isdir(self.raw_dir):
            logging.info(f"The raw directory has been set up: {self.raw_dir}")
        else:
            # Logging error message to inform user that raw directory does not exist and so exits the module
            # If raw directory doesn't exist, the processed and searched folders cannot be created
            logging.error("The raw directory does not exist! Please create the raw directory and provide the data.")
            sys.exit(1)

        # Setting up the other two directories: processed and searched 
        two_dirs = ["processed","searched"]
        for dir_name in two_dirs:
            dir_path = os.path.join(self.top_dir, dir_name)
            # Checking whether the two directories have been set up:
            if not os.path.isdir(dir_path):
                # If the directories don't exist, then the directories are created and the user is informed through logging messages
                os.makedirs(dir_path)
                logging.info(f"The following directory has been created:{dir_path}")
            else:
                logging.info(f"The following directory already exists:{dir_path}")

     
    def executable_setup(self):
        '''
        Function for setting up the following required executables:
        
        java_executable
        dia_umpire_se
        search_gui
        peptide_shaker
        thermo_file_parser
        
        If the executables exists, then a informational message is logged. 
        If executables do not exist, then error message is logged. 
        If thermo_file_parser does not exist, than a warning message is logged. 
        Missing executables are appended to the missing_executables list before exiting the module.

        Attributes:
        self.java_executable (str) - Java executable absolute filepath
        self.dia_umpire_se (str) - DIA Umpire SE executable absolute filepath
        self.search_gui (str) - SearchGUI executable filepath
        self.peptide_shaker (str) - Peptideshaker executable absolute filepath
        self.thermo_file_parser (str) - Thermo File Parser executable absolute filepath

        Raises:
        SystemExit - If there are executables listed in the missing_executables list, the module will terminate and log error message   
        '''
        executables = {
            "java_executable": self.java_executable,
            "dia_umpire_se": self.dia_umpire_se,
            "search_gui": self.search_gui,
            "peptide_shaker": self.peptide_shaker,
            "thermo_file_parser": self.thermo_file_parser
        }
        
        # Checking whether the executables exist and logs the appropriate logging messages:  
        missing_executables = []
        for name, path in executables.items():
            if os.path.exists(path):
                logging.info(f"{name} executable has been found at {path}")
            else:
                if name == "thermo_file_parser":
                    logging.warning(f".mzML files will only be processed as {name} has not been found")
                else:
                    logging.error(f"{name} cannot be found. Please provide the absolute filepath.")
                    missing_executables.append(name)
        # If executables are missing, then the names of the executables are appended to the missing_executables list          
        if missing_executables:
            logging.error(f"List of missing executables: {', '.join(missing_executables)}")
            sys.exit(1)

     
    def parameter_check(self):
        '''
        Function for checking whether each parameter filenname exists or not. 

        Parameter files:
        umpire-se.params - parameter file for DIA Umpire which must be provided. 
        search.par - search gui parameters
        database.fasta - target-decoy database  
        
        If parameter filename exists, then informational message logged informing the user that the filename exists. 
        If parameter filename does not exist, then an error message is logged.
        The missing filenames are appended to parameter_files_missing list. 
        If the parameter_file_missing list contains missing filenames, then error message is logged and exits the module. 
        
        Attributes:
        self.top_dir (str) - top_dir filepath  
        self.DIA_Umpire_Parameters (str) - umpire_se.params parameter filepath
        self.SearchGUI_Parameters (str) - search_par parameter filepath
        self.FASTA_Database (str)  - database.fasta parameter filepath

        Raises:
        SystemExit - If parameter names are listed in the parameter_files_missing list, the module will terminate and log error message  
        '''
        # Dictionary of parameters and their associated filenames
        parameter_files = {
            "DIA_Umpire_Parameters": self.DIA_Umpire_Parameters,
            "SearchGUI_Parameters" : self.SearchGUI_Parameters,
            "FASTA_Database": self.FASTA_Database
        }
        
        # Empty list for listing the missing parameter filenames
        parameter_files_missing = [] 
        
        # For loop for checking if each item in the parameter_files dictionary exists or not
        for parameters, param_files in parameter_files.items():
            file_path = os.path.join(self.top_dir,param_files)
            if os.path.exists(file_path):
                # If parameter filename exists, then logs message informing user that the file exists
                logging.info(f"{param_files} parameter file has been found for {parameters}")
            else:
                # If the parameter file doesn't exist, then logs error message and asks the user to place file in top_dir
                logging.error(f"{param_files} for {parameters} has not been found! Please place {param_files} in {self.top_dir}.")
                # Appending the missing filenames to parameter_files_missing list: 
                parameter_files_missing.append(param_files)
        # If parameter_files_missing list contains missing filenames, then logs error message and exits the module
        if parameter_files_missing:
            logging.error(f"Parameter Files Missing in top_dir: {','.join(parameter_files_missing)}")
            sys.exit(1)



    def reference_name_setup(self):
        '''
        Function for asking the user to input a reference name for the data. 

        If no user input is provided then the name of the top_dir will be used as the reference name.

        Attribute:
        self.reference_name (str) - designated reference name for the data 
        '''
        if not self.reference_name: 
            logging.info("Please input a reference name for this data:")
         
            reference_name = input().strip()
            # If no user input provided, then top_dir will be used as the reference name: 
            if not reference_name:
                reference_name = os.path.basename(self.top_dir)
            # Storing the user input under the variable 'reference_name'
            self.reference_name = reference_name
            logging.info(f"'{reference_name}' is the reference name for this data.")


if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The folder_structure.py module is working!")

    

