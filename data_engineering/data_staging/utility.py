import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import glob
import pandas as pd
import pandasql as psql

class Utility:
    '''
    Utility class to handle things that all of the other classes may need.  File / screen access etc.
    '''

    screen_width = 76
    def __init__(self):
        self.bozo ="bozo"
        self.screen_width = 76

    # define our clear function
    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


    def data_frames_from_file_list(self,file_loc_dict):
        pandas_return_dict = dict()
        
        for key in file_loc_dict.keys():
            df = pd.read_csv(file_loc_dict[key])
            df.rename(columns={x: x.replace(' ', '_').lower() for x in df.columns}, inplace=True)
            df.rename(columns={x: x.replace(':', '_').lower() for x in df.columns}, inplace=True)
            df.rename(columns={x: x.replace('__', '_').lower() for x in df.columns}, inplace=True)
            #df = df.apply(lambda x: x.str.lower() if x.dtype=='object' else x)
            pandas_return_dict[key] = df
        
        return pandas_return_dict
            
            
            
            
    def view_file_types(self,
                        directory=None,
                        file_filter=None,
                        print_files=False,
                        print_file_names_only=True,
                        return_pandas_data_frames=False,
                       skip_list=None):
        
        if file_filter is None:
            file_filter = "*.*"
        if directory is None:
            directory = self.get_this_dir()
            
        glob_path = os.path.join(directory,file_filter)
        files_in_directory = glob.glob(glob_path)
        
        file_names_only = []
        
        file_loc_dict = dict()
        
        for file in files_in_directory:
            if skip_list is not None:
                if os.path.basename(file) in skip_list:
                    continue
            file_names_only.append(os.path.basename(file))
            file_loc_dict[os.path.basename(file)] = file
            if print_files == True:
                print(file)
                
        if print_file_names_only == True:
            for file in file_names_only:
                print(file)
        
        pandas_dict = None
        
        
        if return_pandas_data_frames == True:
            pandas_dict = self.data_frames_from_file_list(file_loc_dict)
            
        return files_in_directory, file_names_only, file_loc_dict, pandas_dict
            
    

    def get_data_from_file(self,str_file_name,current_dir=False):
        '''
        Read an entire file and push the data back.
        :param str_file_name:
        :return:
        '''
        if current_dir==True:
            str_file_name = os.path.join(self.get_this_dir(),str_file_name)
        with open(str_file_name, 'r') as file:
            data = file.read()

        return data

    def get_this_dir(self):
        '''
        Return the working directory.
        :return:
        '''
        thisdir = os.getcwd()
        return thisdir

