
###########################
# F333290 - H.Joshi        #
# Date Created: 07/07/2024 #
# Last Updated: 29/07/2024 #
###########################


'''
search_database module

* This module is to be imported and executed in main.py. 
* This is the sixth step of the proteomics data processing pipeline. 

The purpose of this module is to automate SearchGUI protein database searching process.
Files with the following extensions ('_PeakCluster', '.cms' or '.mzML') are appended to the
not_searched_files list as these files are not used for database searching.
Those files which end in '.mgf' and has the updated raw_name, has the file extension removed. 
This creates a base_file_name of the filenames in thew to_search list 
which is then concatenated with a predefined quality tier to create a new '.mgf' file (tier_file). 
This tier_file is used to search through -xtandem search engine in SearchGUI CLI.
A log file of the searches for each concatenated file is created
and a '.html' file generated by SearchGUI that is not required is then removed. 

Dependancies:
Three classes have been imported from previous modules: FolderStructure, MoveOutputFiles and ConvertRawFiles respectively. 

Class:
SearchDatabase

Methods:
__init__(self, raw_dir, thermo_file_parser, reference_name) - For initialising the class SearchDatabase with raw_dir, thermo_file_parser, reference_name 
update_raw_names() - List of the current raw_names files in the processed directory 
search_process() - Executing the database searching proccess using the SearchGUI CLI  

Attributes:
self.folder_structure  - Instance of the class FolderStructure 
self.convert_raw_files  - Instance of the class ConvertRawFiles 
self.move_to_processed  - Instance of the class MoveOutputFiles 
self.raw_names (list) - Raw filenames without their file extensions 
self.java_executable (str) - Filepath for the Java executable
self.search_gui (str) - Filepath for the SearchGUI executable 
self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
self.SearchGUI_Parameters (str) - Filepath for the search_par file
self.reference_name (str) - User inputted reference name for the data 
self.processed_directory (str) - Filepath for the processed directory  
self.searched_directory (str) - Filepath for the searched directory  
self.search_start_time (float) - Records the start time of the database searching process
self.search_end_time (float) - Records the end time of the database searching processs

'''
# Importing the required Python libraries for this module: 
import os
import subprocess
import logging
import time
import fnmatch


# Importing classes from previous modules:
from folder_structure import FolderStructure
from convert_raw_files import ConvertRawFiles
from move_to_processed import MoveOutputFiles

class SearchDatabase:
    '''
    The class SearchDatabase and its associated methods and attributes are used for the SearchGUI protein database searching process. 

    Methods:
    __init__(self, raw_dir, thermo_file_parser, reference_name) - For initialising the class SearchDatabase with raw_dir, thermo_file_parser, reference_name 
    update_raw_names() - Shows the current raw_names files in the processed directory 
    search_process() - For running the database search engine via SearchGUI CLI

    Attributes:
    self.folder_structure  - Instance of the class FolderStructure 
    self.convert_raw_files  - Instance of the class ConvertRawFiles 
    self.move_to_processed  - Instance of the class MoveOutputFiles 
    self.raw_names (list) - Raw filenames without their file extensions 
    self.java_executable (str) - Filepath for the Java executable
    self.search_gui (str) - Filepath for the SearchGUI executable 
    self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
    self.SearchGUI_Parameters (str) - Filepath for the search_par file
    self.reference_name (str) - User inputted reference name for the data 
    self.processed_directory (str) - Filepath for the processed directory  
    self.searched_directory (str) - Filepath for the searched directory  
    self.search_start_time (float) - Records the start time of the database searching process
    self.search_end_time (float) - Records the end time of the database searching processs
    '''
    def __init__(self, raw_dir, thermo_file_parser, reference_name):
        '''
        Initialising the class SearchDatabase using raw_dir, thermo_file_parser and reference_name.

        Parameters:
        raw_dir (str) - Raw data directory 
        thermo_file_parser (str) -Thermo File Parser executable filepath
        reference_name (str) - Designated reference name for the data 

        Attributes:
        self.folder_structure  - Instance of the class FolderStructure 
        self.convert_raw_files  - Instance of the class ConvertRawFiles 
        self.move_to_processed  - Instance of the class MoveOutputFiles 
        self.raw_names (list) - Raw filenames without their file extensions 
        self.java_executable (str) - Filepath for the Java executable
        self.search_gui (str) - Filepath for the SearchGUI executable 
        self.FASTA_Database (str)  - Filepath for the database.fasta parameter file
        self.SearchGUI_Parameters (str) - Filepath for the search_par file
        self.reference_name (str) - User inputted reference name for the data 
        self.processed_directory (str) - Filepath for the processed directory  
        self.searched_directory (str) - Filepath for the searched directory  
        self.search_start_time (float) - Records the start time of the database searching process
        self.search_end_time (float) - Records the end time of the database searching processs
        '''
        self.folder_structure = FolderStructure()
        self.convert_raw_files = ConvertRawFiles(raw_dir, thermo_file_parser)
        self.move_to_processed = MoveOutputFiles(raw_dir, self.convert_raw_files)

        self.raw_names = self.move_to_processed.raw_names
        self.java_executable = self.folder_structure.java_executable
        self.search_gui = self.folder_structure.search_gui
        self.FASTA_Database = self.folder_structure.FASTA_Database
        self.SearchGUI_Parameters = self.folder_structure.SearchGUI_Parameters
        self.reference_name = reference_name
        
        self.processed_directory = os.path.join(os.path.dirname(raw_dir), "processed")
        self.searched_directory = os.path.join(os.path.dirname(raw_dir), "searched")

        self.search_start_time = None
        self.search_end_time = None


    def update_raw_names(self):
        '''
        Function for updating self.raw_names list with the filenames currently in the processed directory. 

        A list of all the files present in the processed directory is extracted.
        Those filenames which have the '.mgf' file extension are then extracted without their file extension. 

        Attribute:
        self_raw_names (list) - updated list of filenames without their file extensions in the processed directory 
        '''
        self.raw_names = [
        os.path.splitext(f)[0] for f in os.listdir(self.processed_directory)
        if os.path.isfile(os.path.join(self.processed_directory, f)) and f.endswith('.mgf')
    ]

    
    def search_process(self):
        '''
        Function for running database search engine via SearchGUI CLI. 

        Files in self.raw_names list are segregated into to_search and not_searched_files. 
        If files end in '_PeakCluster, '.cms' or '.mzML', then these files are appended to the not_searched_files list.
        Other .mgf files then have their file extension removed so that the quality tier can be concatenated with the filename. 
        These concatenated .mgf files are then used to search through the SearchGUI database engine.
        A '.html' file that is not required but automatically generated from the searching process is then removed. 

        The time taken for this process to run is recorded and appropriate informational and/or 
        warning/error messages are logged at specific stages of this process.
        A search_cli_log is also generated in the search directory which logs the searching process and/or errors/exceptions if searching fails. 

        Method:
        self.update_raw_names() - updating self.raw_names list with the files present in the processed directory 

        Attributes:
        self.processed_directory (str) - filepath for the processed directory 
        self.searched_directory (str) - filepath for the searched directory
        self.java_executable (str) - filepath for the Java executable 
        self.search_gui (str) - filepath for the SearchGUI executable
        self.FASTA_Database (str) - filepath for the database.fasta parameter file
        self.SearchGUI_Parameters (str) - filepath for the search_par file
        self.reference_name (str) -  using user inputted reference name for the data
        self.search_start_time (float) - recording time when the database searching process started
        self.search_end_time (float) -  recording time when the database searching process ended 
        '''
        logging.info("==========")
        logging.info("Running database search with SearchGUI CLI.")
        
        search_engine = "-xtandem"
        logging.info(f"Using {search_engine} search engine.")
        
        self.update_raw_names()

        self.search_start_time = time.time()

        # Creating a dictionary of Quality Tiers (QT) used to set the qt_to_search 
        qt_dict = {'1': "_Q1.mgf", '2': "_Q2.mgf", '3':"_Q3.mgf",
           '12':"_Q1Q2_combined.mgf", '13':"_Q1Q3_combined.mgf", '23':"_Q2Q3_combined.mgf",
           '123':"_Q1Q2Q3_combined.mgf"}

        # qt_to_search is currently set to '1' QT as per the qt_dict dictionary 
        qt_to_search = ['1']
        
        # Files which will be searched using SearchGUI
        to_search = set()  
       
        # List of files that will not be searched (either because these files were skipped or could not be concatenated with QT)
        not_searched_files = []  


        # For loop for iterating through self.raw_names to check file extensions
        for raw_name in self.raw_names:
             # If the file ends in '_PeakCluster', '.cms' or '.mzML', then these files are appended to the not_searched_files list and .'mgf' is added to the filename
            if raw_name.endswith("_PeakCluster") or raw_name.endswith(".cms") or raw_name.endswith(".mzML"):
                not_searched_files.append(raw_name + ".mgf")
                # Warning message is logged that such files will not be searched before continuing with the process 
                logging.warning(f"{raw_name}.mgf will not be searched.")
                continue
            
            # For loop for iterating through qt_to_search
            for qt in qt_to_search:
                # For loop for iterating through each file present in the processed directory 
                for file in os.listdir(self.processed_directory):
                    # If file ends with '.mgf' and has the updated raw name, then its' file extension is removed 
                    if file.endswith(".mgf") and file.startswith(raw_name):
                        base_file_name = os.path.splitext(file)[0]

                        # For loop for iterating through the QT dictionary 
                        for qt_value in qt_dict.values():
                            # If the base_file_name contains the QT suffix, then it is removed 
                            if base_file_name.endswith(qt_value[:-4]):
                                base_file_name = base_file_name[:-len(qt_value[:-4])]
                                break
                        
                        # Filepath of the tier file
                        tier_file = os.path.join(self.processed_directory, base_file_name + qt_dict[qt])
                        
                        # Checking whether the tier file exists
                        # If it is not empty and not found in the to_search set, then tier file is added to the to_search set 
                        if os.path.exists(tier_file): 
                            if os.path.getsize(tier_file) > 0:
                                if tier_file not in to_search:
                                    to_search.add(tier_file)
                            else:
                                not_searched_files.append(os.path.basename(tier_file))
                                logging.warning(f"{os.path.basename(tier_file)} will not be searched as the tier file is empty.")
                        else: 
                            not_searched_files.append(os.path.basename(tier_file))
                            logging.warning(f"{os.path.basename(tier_file)} will not be searched as the tier file does not exist.")
        
        # Converting to_search set into a list 
        to_search = list(to_search)

        # Logging informational message for the files present in to_search list 
        if to_search:
            logging.info("Files to search:")
            for file in to_search:
                logging.info(f"{os.path.basename(file)}")

        # Try-Except block for executing SearchGUI CLI subprocess command 
        # Using required executables, directories, parameters and reference name to conduct database searching 
        try:
            os.makedirs(self.searched_directory, exist_ok=True)
            
            if not to_search:
                logging.error("No files to search.")
            else:
                search_command = [
                    self.java_executable, 
                    "-cp", self.search_gui, 
                    "eu.isas.searchgui.cmd.SearchCLI",
                    "-spectrum_files", ','.join(to_search),
                    "-fasta_file", self.FASTA_Database,
                    "-output_folder", self.searched_directory,
                    "-id_params", self.SearchGUI_Parameters, 
                    search_engine, "1",
                    "-output_default_name", self.reference_name,
                    "-output_data", "1"
                ]

                search_process = subprocess.run(search_command, capture_output=True, text=True, check=True)
                

                self.search_end_time = time.time()

            
                logging.info(f"Searches completed, results can be found in ./searched/{self.reference_name}.zip")
                
                # Creating a file called 'search_cli_log' to log the database searching process and any errors/execptions if this process fails
                with open(os.path.join(self.searched_directory, "search_cli.log"), "w") as outfile:
                    outfile.write("Command line arguments\n")
                    outfile.write("----------------------\n")
                    outfile.write(" ".join(search_command))
                    outfile.write("\n\nRun Log\n-------\n")
                    outfile.write(search_process.stdout)
                    outfile.write(search_process.stderr)
                
                logging.info("Log of searches can be found in ./searched/search_cli.log")
                
                # Removing a .html file automatically generated by the searching process from the search directory 
                for f in fnmatch.filter(os.listdir(self.searched_directory), "SearchGUI*.html"):
                    os.remove(os.path.join(self.searched_directory, f))
                
                # Retrieving the list of to_search files for the prepare_peptideshaker module 
                return list(to_search)
        
        except Exception as e:
            logging.error(f"Error found during the database searching process: {e}")



if __name__=="__main__":
    '''
    Test code to check that this module is working independently. 
    This test code is to be executed directly in the terminal.
    A message will be printed if the module is working properly. 
    '''
    print("The search_database.py module is working!")




