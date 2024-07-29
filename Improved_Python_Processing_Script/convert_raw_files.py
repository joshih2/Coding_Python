###########################
# F333290 - H.Joshi        #
# Date Created: 21/06/2024 #
# Last Updated: 25/07/2024 #
###########################

'''
convert_raw_files Module 

* This module is to be imported and executed in main.py. 
* This is the second step of the proteomics data processing pipeline.

  The purpose of this module is to automate the file conversion process of .raw files into .mzML files. 
  This process involves identifying, converting and checking the newly converted .mzML files.

  If raw_dir is not found, then the file conversion process using Thermo File Parser cannot proceed. 

  The time taken for this process to run is recorded and appropriate informational and/or warning 
  messages are logged at specific stages of the file conversion process. 

Class:
ConvertRawFiles

Methods:
__init__(self, raw_dir, thermo_file_parser) - For initialising the class with raw_dir and thermo_file_parser 
identify_raw_files() - Checking whether .raw files and .mzML files exist in raw_dir or not
convert_raw_files() - Converting .raw files to .mzML files using Thermo File Parser 
check_converted_raw_files() - Checking the number of .mzML files successfully converted from .raw files
retrieve_raw_file_count()  - Retrieving the total number of .mzML files now present in raw_dir after file conversion 

Attributes:
self.raw_dir (str) - Location of the .raw files 
self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
self.raw_files (list) - .raw files that have been converted successfully to .mzML
self.files_to_convert (list) - .raw files that are yet to be converted to .mzML
self.thermo_raw_files (list) - .raw files that exist in raw_dir 
self.raw_files_base (list) - .mzML files without their corresponding .mzML file extension
self.raw_file_count (int) -  Total number of .raw files converted to .mzML format 
self.conversion_start_time (float) - Records the start time of the file conversion process
self.conversion_end_time (float) - Records the end time of the file conversion process  

Exceptions:
SystemExit - Occurs when either the raw directory does not exist or when there are no more .mzML files to convert
'''

# Importing the required Python libraries for this module: 
import os
import sys
import time
import logging
import subprocess


class ConvertRawFiles:
    '''
    The class ConvertRawFiles and its associated methods and attributes are used for converting .raw files to .mzML files.

    Methods:
    __init__(self, raw_dir, thermo_file_parser) - For initialising the class with raw_dir and thermo_file_parser 
    identify_raw_files() - Checking whether .raw files and .mzML files exist in raw_dir or not
    convert_raw_files() - Converting .raw files to .mzML files using Thermo File Parser 
    check_converted_raw_files() - Checking the number of .mzML files successfully converted from .raw files
    retrieve_raw_file_count()  - Retrieving the total number of .mzML files now present in raw_dir after file conversion 
    
    Attributes:
    self.raw_dir (str) - Location of the .raw files 
    self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
    self.raw_files (list) - .raw files that have been converted successfully to .mzML
    self.files_to_convert (list) - .raw files that are yet to be converted to .mzML
    self.thermo_raw_files (list) - .raw files that exist in raw_dir 
    self.raw_files_base (list) - .mzML files without their corresponding .mzML file extension
    self.raw_file_count (int) -  Total number of .raw files converted to .mzML format 
    self.conversion_start_time (float) - Records the start time of the file conversion process
    self.conversion_end_time (float) - Records the end time of the file conversion process    
    '''
    def __init__(self, raw_dir, thermo_file_parser):
        '''
    For identifying .raw files to convert to .mzML format using Thermo File Parser.

    Parameters:
    raw_dir (str) -  the raw directory in which the .raw files are stored
    thermo_file_parser (str) - Thermo File Parser executable filepath

    Attributes:
    self.raw_dir (str) - Location of the .raw files 
    self.thermo_file_parser (str) - Filepath for the Thermo File Parser executable
    self.raw_files (list) - .raw files that have been converted successfully to .mzML
    self.files_to_convert (list) - .raw files that are yet to be converted to .mzML
    self.thermo_raw_files (list) - .raw files that exist in raw_dir 
    self.raw_files_base (list) - .mzML files without their corresponding .mzML file extension
    self.raw_file_count (int) -  Total number of .raw files converted to .mzML format 
    self.conversion_start_time (float) - Records the start time of the file conversion process
    self.conversion_end_time (float) - Records the end time of the file conversion process    
        '''
        self.raw_dir = raw_dir
        self.thermo_file_parser = thermo_file_parser
        self.raw_files = []
        self.files_to_convert = []
        self.thermo_raw_files = []
        self.raw_files_base = []
        self.raw_file_count = 0
        self.conversion_start_time = None
        self.conversion_end_time = None 
        

    def identify_raw_files(self):
        '''
        Function for identifying raw files (.raw and .mzML files) in raw_dir. 
        
        If .raw files are found in raw_dir, then these files are added to the self.thermo_raw_files list. 
        If .mzML files are found in raw_dir, then these files are added to the self.raw_files list.
        If raw_dir does not exist, then raw files in raw_dir cannot be identified based on 
        file extension. 

        Attributes:
        self.raw_dir (str) - raw_dir filepath 
        self.raw_files (list) - list containing .mzML files from raw_dir
        self.thermo_raw_files (list) - list containing .raw files from raw_dir 

        Raises:
        SystemExit - If the raw directory does not exist, then the module will terminate and log error message 
        '''
        logging.info("==========") 
        logging.info("Checking whether the raw directory exists. If so,the raw files will be identified based on file extension.")
        # Checking whether raw_dir exists or not 
        if os.path.isdir(self.raw_dir):
            # If raw_dir exists, then all raw files are listed 
            fnames = os.listdir(self.raw_dir)
            for f in fnames:
                # If .mzML extension, file is appended to self.raw_files list 
                if f.endswith(".mzML"):
                    self.raw_files.append(f)
                # Else if .raw extension, the file is appended to self.thermo_raw_files list 
                elif f.endswith(".raw"):
                    self.thermo_raw_files.append(f)
                else:
                    # If the file extension is not .raw or .mzML, it is ignored and continues through the module 
                    continue
        else:
          logging.error("The raw directory cannot be found. Please create the raw directory.")
          sys.exit(1)    


    
    def convert_raw_files(self):
        '''
        Function for converting raw files in raw_dir using Thermo File Parser. 
        
        A list of base filenames from the .mzML files in self.raw_files is created.
        Any .raw file that has not been converted to .mzML format in self.thermo.raw_files is appended 
        to self.files_to_convert list.
        If Thermo File Parser and .raw files for file conversion are both available, then only does
        the file conversion process starts. 
        Successfully converted .raw files are appended to self.raw_files list.  
        File conversion start and finish times are recorded and logging messages about the file conversion 
        process are generated.


        Attributes:
        self.raw_files_base (list) -  .mzML files without their corresponding .mzML file extension
        self.raw_files (list) - .raw files that have been converted successfully to .mzML
        self.thermo_raw_files (list) - .raw files that exist in raw_dir 
        self.files_to_convert (list) - .raw files that are yet to be converted to .mzML
        self.thermo_file_parser (str) - Thermo File Parser executable filepath
        self.conversion_start_time (float) - records the start time of the file conversion process
        self.conversion_end_time (float) - records the end time of the file conversion process  
        '''
        # Creating list of raw file basenames by removing .mzML file extension from each file in self.raw_files 
        self.raw_files_base = [f[:-5] for f in self.raw_files]
        # For loop for iterating through each filename in self.thermo_raw_files 
        for thermo_raw in self.thermo_raw_files:
            # Checking whether raw file basename without the .raw extension is not in self.raw_files_base list
            if thermo_raw not in self.raw_files_base:
                # If not, then raw files are appended to self.files_to_convert list 
                self.files_to_convert.append(thermo_raw) 
            
        
        # File conversion process will only occur if raw files and Thermo File Parser are available 
        if len(self.files_to_convert) > 0 and os.path.exists(self.thermo_file_parser):
            # Logging message to inform user of the number of .raw files requiring file conversion 
            logging.info(f"The process of converting {(len(self.files_to_convert))} Thermo RAW files to .mzML files will start now.")
            
            self.conversion_start_time = time.time()

            for thermo_raw in self.files_to_convert:
                raw_file = thermo_raw[:-4] + ".mzML"
                logging.info(f"Converting {thermo_raw} with Thermo File Parser")
                
                # File conversion process subprocess command 
                return_code = subprocess.call([self.thermo_file_parser,
                                                    "-i", os.path.join(self.raw_dir, thermo_raw),
                                                    "-b", os.path.join(self.raw_dir, raw_file)],
                                                    universal_newlines=True)
                if return_code == 0:
                    logging.info(f"Successfully converted to {raw_file}")
                    self.raw_files.append(raw_file)
                else:
                    logging.error(f"Failed to convert {thermo_raw} to {raw_file}")
                
                self.conversion_end_time = time.time()



    def check_converted_raw_files(self):
        '''
        Function for checking the number of .mzML files successfuly converted from .raw files. 
        
        The total number of converted .mzML files are counted in self.raw_files list. 
        If there no .mzML files are found, then a warning message is logged and exits the module. 

        Attribute:
        self.raw_file_count (int) - count of .raw files converted to .mzML format 
        self.raw_files (list) - .raw files that have been converted successfully to .mzML
        
        Raises:
        SystemExit - If there are no .mzML files, then the module will terminate and log warning message
        '''
        self.raw_file_count = len(self.raw_files) 
        if self.raw_file_count == 0:
            logging.warning("There are no more .mzML files to convert. Exiting the script now.")
            sys.exit(1)
    


    def retrieve_raw_file_count(self):
        '''
        Function for retrieving count of .mzML files present in raw_dir after file conversion.

        Returns:
        An integer value of the total count of successfully converted .mzML files in self.raw_files list 

        Attribute:
        self.raw_files (list) - .raw files that have been converted successfully to .mzML format 
        '''
        return len(self.raw_files)
    


if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The convert_raw_files.py module is working!")