###########################
# F333290 - H.Joshi        #
# Date Created: 03/07/2024 #
# Last Updated: 26/07/2024 #
###########################

'''
clean_unneeded_files module 

* This module is to be imported and executed in main.py.
*This is the fourth step of the proteomics data processing pipeline. 

The purpose of this module is to automate the unneeded file cleanup process 
after DIA-Umpire file processing has been completed. 

Unneeded files are removed from raw_dir based file extensions/suffixes already predefined in self.unneeded_files. 
Also, if there are files ending in 'Peak', then these files are also removed from peak_dir 
before removing peak_dir itself.  

Class:
CleanFiles

Methods:
__init__() - For initialising the class CleanFiles
cleaning_process(self, raw_dir) - Cleaning unneeded files from raw_dir

Attribute:
self.unneeded_files (tuple) - Predefined file extensions/suffixes that are to be removed from raw_dir
'''
# Importing the required Python libraries for this module: 
import os
import logging

class CleanFiles:
    '''
    The class CleanFiles and its associated methods and attribute
    are used for cleaning up unneeded files after DIA Umpire processing has been done. 

    Methods:
    __init__() - For initialising the class CleanFiles
    cleaning_process(self, raw_dir) - Cleaning unneeded files from raw_dir

    Attributes:
    self.unneeded_files (tuple) - Contains file extensions/suffixes that are to be removed from raw_dir
    '''
    def __init__(self):
        '''
        Initialising the class CleanFiles.
        
        Attribute:
        self.unneeded_files (tuple) - File extensions/suffixes that are to be removed from raw_dir 

        '''
        self.unneeded_files = (".DIAWindowsFS",
                      ".RTidxFS",
                      ".ScanClusterMapping_Q1",
                      ".ScanClusterMapping_Q2",
                      ".ScanClusterMapping_Q3",
                      ".ScanidxFS",
                      ".ScanPosFS",
                      ".ScanRTFS",
                      "_diasetting.ser",
                      "_params.ser")
    

      
    def cleaning_process(self, raw_dir): 
        '''
        Function for cleaning up unneeded files after DIA-Umpire file processing. 

        Informational logging messages are printed to show that the cleanup process is to commence
        and files based on the specified tuple are to be removed.

        All files and directories within raw_dir are listed in current_files. 
        Using a for loop, each file in current_files is iterated through to check whether
        the file ends in the extensions/suffixes specified for removal in self.unneeded_files. 
        If the extensions/suffixes are the same, then the file is removed from raw_dir. 
        If there are files ending in 'Peak' then they are also removed from peak_dir before removing 
        peak_dir itself. 

        Parameter:
         raw_dir (str) - directory in which .mzML and .raw files are stored  
        '''

        # Logging informational message that the cleaning process will start. 
        logging.info("==========")
        logging.info("Unneeded files will now be cleaned and removed.")
        
        # Logging message that unneeded files are to be removed based on the tuple above 
        logging.info(f"File extensions ending in {", ".join(self.unneeded_files)}")
        
        # Listing all files and directories within raw_dir
        current_files = os.listdir(raw_dir)
        
        for f in current_files:
            file_path = os.path.join(raw_dir, f)
            # If the file ends with any of the filetypes mentioned in the tuple, then it is removed from raw_dir 
            if f.endswith(self.unneeded_files): 
                os.remove(file_path)
            # If files end in 'Peak', then those files are removed from peak_dir 
            elif f.endswith("_Peak"):
                peak_dir = os.path.join(raw_dir, f)
                if os.path.isdir(peak_dir):
                    for _f in os.listdir(peak_dir):
                        os.remove(os.path.join(peak_dir, _f))
                    # Removing the empty peak_dir 
                    os.rmdir(peak_dir)



if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The clean_unneeded_files.py module is working!")