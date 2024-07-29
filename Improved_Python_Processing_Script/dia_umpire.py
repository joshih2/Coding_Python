###########################
# F333290 - H.Joshi        #
# Date Created: 26/06/2024 #
# Last Updated: 26/07/2024 #
###########################

'''
dia_umpire Module 

* This module is to be imported and executed in main.py. 
*This is the third step of the proteomics data processing pipeline.

The purpose of this module is to automate the .mzML file processing by DIA-Umpire
and deal with any errors that may arise from this processing step. 

Dependancy:
One class has been imported: FolderStructure from folder_structure.py 

Class:
DiaUmpire

Methods:
__init__(self, convert_raw_files_instance) - For initialising the class DiaUmpire with the instance of ConvertRawFiles class 
dia_file_processing() - Processing .mzML files using DIA Umpire 

Attributes:
self.convert_raw_files  - Instance of the class ConvertRawFiles 
self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
self.number_of_raw_files (int) - Count of .mzML files that have been processed by DIA Umpire
self.failed_files (list) - .mzML files that have failed to be processed by DIA Umpire 
self.dia_processed_files (set) - For checking the .mzML files that have been processed by DIA Umpire 
self.umpire_start_time (float) - Records the start time of the DIA Umpire process
self.umpire_end_time (float) - Records the start time of the DIA Umpire process
self.folder_structure  -  Instance of the class FolderStructure
self.java_executable (str) - Filepath for the Java executable
self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file

Exceptions:
subprocess.CalledProcessError - Occurs when umpire_command fails and so logs warning message 
Exception - Occurs when any exception occurs during processing causing the umpire_command to fail and so logs error message
'''

# Importing the required Python libraries for this module:
import os
import subprocess
import time
import logging

# Importing class from a previous module:
from folder_structure import FolderStructure

class DiaUmpire:
    '''
    The class DiaUmpire and its associated methods and attributes are used for DIA Umpire File Processing.

    Methods:
    __init__(self, convert_raw_files_instance) - For initialising the class with the instance of ConvertRawFiles class 
    dia_file_processing() - Processing .mzML files using DIA Umpire 


    Attributes:
    self.convert_raw_files  - Instance of the class ConvertRawFiles 
    self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
    self.number_of_raw_files (int) - Count of .mzML files that have been processed by DIA Umpire
    self.failed_files (list) - .mzML files that have failed to be processed by DIA Umpire 
    self.dia_processed_files (set) - For checking the .mzML files that have been processed by DIA Umpire 
    self.umpire_start_time (float) - Records the start time of the DIA Umpire process
    self.umpire_end_time (float) - Records the start time of the DIA Umpire process
    self.folder_structure  -  Instance of the class FolderStructure
    self.java_executable (str) - Filepath for the Java executable
    self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
    self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file
    '''
    def __init__(self, convert_raw_files_instance):
        '''
        Establishing instances of FolderStructure and ConvertRawFiles to process .mzML files using DIA Umpire. 
        This allows access to the required executables, parameters and .mzML files used for DIA Umpire file processing. 

        Parameter:
        convert_raw_files_instance - Instance of the class ConvertRawFiles 

        Attributes:
        self.convert_raw_files  - Instance of the class ConvertRawFiles 
        self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
        self.number_of_raw_files (int) - Count of .mzML files that have been processed by DIA Umpire
        self.failed_files (list) - .mzML files that have failed to be processed by DIA Umpire 
        self.dia_processed_files (set) - For checking the .mzML files that have been processed by DIA Umpire 
        self.umpire_start_time (float) - Records the start time of the DIA Umpire process
        self.umpire_end_time (float) - Records the start time of the DIA Umpire process
        self.folder_structure  -  Instance of the class FolderStructure
        self.java_executable (str) - Filepath for the Java executable
        self.dia_umpire_se (str) - Filepath for the DIA Umpire SE executable
        self.DIA_Umpire_Parameters (str) - Filepath for the umpire_se.params file
        '''
        
        self.convert_raw_files = convert_raw_files_instance
        self.raw_files = self.convert_raw_files.raw_files
        self.number_of_raw_files = len(self.raw_files)

        self.failed_files = []
        self.dia_processed_files = set()
        self.umpire_start_time = None
        self.umpire_end_time = None 

        self.folder_structure = FolderStructure()
        self.java_executable = self.folder_structure.java_executable
        self.dia_umpire_se = self.folder_structure.dia_umpire_se
        self.DIA_Umpire_Parameters = self.folder_structure.DIA_Umpire_Parameters

        
    def dia_file_processing(self):
        '''
        Function for DIA Umpire file processing of .mzML files. 

        Unique .mzML files are identified in self.raw_files and processed using DIA Umpire. 
        For each processed .mzML file, a DIA Umpire log file is created in raw_dir. 
        If .mzML files fail processing, these files are appended to the self_failed_files list. 
        self_raw_files list is updated to ensure that only successfully DIA Umpire processed .mzML files are in this list. 

        The time taken for this process to run is recorded and appropriate informational and/or 
        warning/error messages are logged at specific stages of this process.

        Attributes:
        self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
        self.umpire_start_time (float) - records the start time of the DIA Umpire process
        self.java_executable (str) - Java executable filepath 
        self.dia_umpire.se (str) - DIA Umpire SE executable filepath
        self.convert_raw_files - Instance of the class ConvertRawFiles
        self.DIA_Umpire_Parameters (str) - umpire_se.params parameter filepath 
        self.dia_processed_files (set) - checking that the .mzML files that have been processed by DIA Umpire 
        self.failed_files (list) - .mzML files that have failed to be processed by DIA Umpire 
        self.umpire_end_time (float) - records the start time of the DIA Umpire process

        Raises:
        subprocess.CalledProcessError - Occurs when umpire_command fails and so logs warning message 
        Exception - Occurs when any exception occurs causing the umpire_command to fail and so logs error message  
        '''
        logging.info("==========")
        logging.info("DIA Umpire Processing will start now.")

        # Using a set and list to remove any duplicate .mzML files in self.raw_files 
        # Only unique .mzML files will be used for DIA Umpire processing 
        unique_raw_files = list(set(self.raw_files))
        logging.info(f"{len(unique_raw_files)} files will now be processed.")
        
        self.umpire_start_time = time.time()

        # For loop for iterating through each unique .mzML file for DIA Umpire processing 
        for index, raw_file in enumerate(unique_raw_files, start=1):
            logging.info(f"Processing {raw_file} ({index}/{len(unique_raw_files)}) with DIA Umpire...")
            _proc_time = time.time()
            
            # Try-Except block for executing DIA Umpire Process subprocess command 
            # Using required executables, directories, and parameters as set up in folder_structure.py 
            try:
                umpire_command = [
                    self.java_executable, "-jar", "-Xmx8G", self.dia_umpire_se,
                    os.path.join(self.convert_raw_files.raw_dir, raw_file),
                    self.DIA_Umpire_Parameters
                ]
                
                umpire_process = subprocess.run(umpire_command, capture_output=True, text=True, check=True)
                
                # Renaming the DIA Umpire log file for each processed .mzML file
                os.replace("./raw/diaumpire_se.log", f"./raw/{raw_file[:-5]}_diaumpire.log")
                
                # If return code is non zero, then log warning message about the unsuccessful processing 
                if umpire_process.returncode != 0:
                    logging.warning(f"Error! Please check ./raw/{raw_file[:-5]}_diaumpire.log")
                    self.failed_files.append(raw_file)
                else:
                    # Append the successfully processed .mzML file to the dia_processed_files set
                    self.dia_processed_files.add(raw_file)
                    logging.info(f"File processed in {time.strftime('%M:%S', time.gmtime(time.time() - _proc_time))} min:sec")
            
            # Except when subprocess.CalledProcessError occurs, log warning message for the unsuccessful processed files
            # Append files to the self.failed_files list 
            except subprocess.CalledProcessError as e:
                logging.warning(f"Error processing {raw_file}: {e}")
                self.failed_files.append(raw_file)

            # Except when any exception occurs, logs error message and append the file to the self.failed_files list 
            except Exception as e:
                logging.error(f"Exception occurred processing {raw_file}: {e}")
                self.failed_files.append(raw_file)
        
        # Ensuring that self_raw_files only contains list of successfully processed .mzML files 
        self.raw_files = [f for f in self.raw_files if f not in self.failed_files]

        logging.info(f"{len(self.dia_processed_files)} files have been successfully processed with DIA-Umpire.")
        self.umpire_end_time = time.time()



if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The dia_umpire.py module is working!")
