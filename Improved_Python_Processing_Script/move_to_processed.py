###########################
# F333290 - H.Joshi        #
# Date Created: 04/07/2024 #
# Last Updated: 26/07/2024 #
###########################

'''
move_to_processed module 

* This module is to be imported and executed in main.py. 
*This is the fifth step of the proteomics data processing pipeline. 

The purpose of this module is to automate the transfer of the processed files 
from the raw directory to the processed directory after the file cleanup process has taken place. 

Files are iteratively moved to the processed directory from the raw directory
based on a predefined list of file extensions.

Class:
MoveOutputFiles

Methods:
__init__(self, raw_dir, convert_raw_files_instance) - For initialising the class MoveOutputFiles with the instance of ConvertRawFiles class 
move_to_processed() -  For moving a predefined list of files from the raw to the processed directory

Attributes:
self.convert_raw_files - Instance of the class ConvertRawFiles
self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
self.raw_names (list) - raw filenames without their file extensions 
self.raw_dir (str) - Location of the .raw files 
self.processed_directory (str) - Filepath for the processed directory  
self.move_file_extensions (list) - Predefined list of file extensions to move to the processed directory 
'''

# Importing the required Python libraries for this module: 
import os
import logging


class MoveOutputFiles:
    '''
    The class MoveOutputFiles and its associated method and attributes
    are used for moving processed files from the raw to the processed directory. 

    Methods:
    __init__(self, raw_dir, convert_raw_files_instance) - For initialising the class MoveOutputFiles with the instance of ConvertRawFiles class 
    move_to_processed() -  For moving a predefined list of files from the raw to the processed directory

    Attributes:
    self.convert_raw_files - Instance of the class ConvertRawFiles
    self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
    self.raw_names (list) - raw filenames without their file extensions 
    self.raw_dir (str) - Location of the .raw files 
    self.processed_directory (str) - Filepath for the processed directory  
    self.move_file_extensions (list) - Predefined list of file extensions to move to the processed directory 
    '''
    def __init__(self, raw_dir, convert_raw_files_instance):
        '''
        Establishing raw_dir and instance of ConvertRawFiles to move processed files from 
        raw directory to the processed directory. 

        Parameter:
        convert_raw_files_instance - Instance of the class ConvertRawFiles 

        Attributes:
        self.convert_raw_files - Instance of the class ConvertRawFiles
        self.raw_files (list) - .raw files that have been converted successfully to .mzML in convert_raw_files.py
        self.raw_names (list) - raw filenames without their file extensions 
        self.raw_dir (str) - Location of the .raw files 
        self.processed_directory (str) - Filepath for the processed directory  
        self.move_file_extensions (list) - Predefined list of file extensions to move to the processed directory 
        '''
        self.convert_raw_files = convert_raw_files_instance
        self.raw_files = convert_raw_files_instance.raw_files
        
        # List of filenames without their file extensions 
        # Created from a list of whole filenames in self.raw_files list 
        self.raw_names = [os.path.splitext(f)[0] for f in self.raw_files]

        self.raw_dir = raw_dir
        self.processed_directory = os.path.join(os.path.dirname(raw_dir), "processed")
        
        # List of file extensions to move to the processed directory
        self.move_file_extensions = ["_Q1.mgf", "_Q2.mgf", "_Q3.mgf", "_Q1.mzML",
                                      "_Q2.mzML", "_Q3.mzML", "_PeakCluster.csv"]

    
    
    
    def move_to_processed(self):
        ''''
        Function for moving files processed by DIA-Umpire from the raw directory to the processed directory. 

        Each raw_name is iterated through the raw_names list using a for loop.
        Each file is then checked for whether it has a file extension as defined in self.move_file_extensions list.
        If the file extension corresponds to the extensions specified in move_file_extensions list,
        then the file in the raw directory is moved to the processed directory.

        Attributes:
        self.raw_names (list) - raw filenames without their file extensions 
        self.move_file_extensions (list) - predefined list of file extensions to move to the processed directory 
        self.raw_dir (str) -  directory for storing .raw files 
        self.processed_directory - processed directory filepath 
        '''
        logging.info("==========")
        logging.info("The process of moving files to the processed directory will start now.")
        
        # For loop for iterating through raw_names list   
        for raw_name in self.raw_names:
            logging.info(f"Moving files for sample {raw_name} to the processed directory.")  
            for ext in self.move_file_extensions:  
                 # File paths for raw_dir and processed directory are made for each extension in self.move_file_extensions list 
                 current_directory = os.path.join(self.raw_dir, raw_name+ext)
                 new_directory = os.path.join(self.processed_directory, raw_name+ext)
                 # If a file with a predefined file extension exists in raw_dir, then file is moved to processed directory 
                 if os.path.exists(current_directory):
                     os.replace(current_directory, new_directory)
           


if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The move_to_processed.py module is working!")


