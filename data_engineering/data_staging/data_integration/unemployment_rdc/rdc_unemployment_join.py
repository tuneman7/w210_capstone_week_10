import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from re import sub
import sqlite3
import glob
import os
from tqdm import tqdm
import seaborn as sns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#define paths for the fed and realtor data 
#update these paths for your machine when you run the file, or you will read in all csv files from your current working directory

rdc_path ="/Users/moges/w210_sec_008_capstone/data_engineering/datasets/realtor/"
fed_path = "/Users/moges/w210_sec_008_capstone/data_engineering/datasets/fed/monthly_unemployment_by_county"

rdc = pd.read_csv('{}RDC_Inventory_Core_Metrics_County_History.csv'.format(rdc_path))

#set current directory to fed path
os.chdir('{}'.format(fed_path))

globbed_files = glob.glob("*.csv") #creates a list of all csv files

#create empty df
unemployment_df = None

#read in file name as a column for each .csv file in my working directory 
#if this runs for a while, check to see if you've updated the directory 
for i, f in enumerate (globbed_files):
    if i == 0:
        unemployment_df = pd.read_csv(f)
        unemployment_df['file_name'] = f
    else:
        tmp = pd.read_csv(f)
        tmp['file_name'] = f
        unemployment_df = unemployment_df.append(tmp)

#test regex here https://regex101.com/r/ZYKlVw/1
#use regex to strip the county and state names from the file name and drop column 'county' cause it is literally the word 'county'
unemployment_df_2 = unemployment_df['file_name'].str.extract(r'(?<=\_in_)(.*?)(?=\_county_)([_county_]+)_(.*)_.*?')
unemployment_df_2.columns = ['county_name', 'county', 'state']
unemployment_df_2.drop(columns='county', inplace=True)

#change the format of county name to match the realtor data (<county name> <, > <state name>)
#rename the columns and drop columns we don't need
unemployment_df_2['county_name'] = unemployment_df_2['county_name'].str.replace('_',' ')
unemployment_df['county_name'] = unemployment_df_2['county_name'] + ", " + unemployment_df_2['state']
unemployment_df['county_name'] = unemployment_df['county_name'].str.strip()
unemployment_df.drop(columns=['Unnamed: 0', 'file_name'], inplace=True)
unemployment_df.rename(columns={'date': 'month_date_yyyymm'}, inplace=True)

#change the format of the date to xx/xx/xxxx to xxxxxx and make it a string so there aren't data type issues
unemployment_df['month_date_yyyymm'] = pd.to_datetime(unemployment_df['month_date_yyyymm'])
unemployment_df['month_date_yyyymm'] = unemployment_df['month_date_yyyymm'].dt.strftime('%Y%m')
unemployment_df['month_date_yyyymm'] = unemployment_df['month_date_yyyymm'].astype(str)

#merge the realtor file with the unemployment data
rdc['county_name'] = rdc['county_name'].str.strip()

rdc_2 = pd.merge(rdc, unemployment_df, how='left', on=['month_date_yyyymm','county_name'])

#validate missing counties - once FRED data fully downloaded, only missing counties should be DC and Virign Islands
#missing 'value' column means no unemployement data (either data missing from FRED API download or regex didnt capure edge case)
no_county_names = rdc_2[rdc_2['value'].isnull()]

#we only care about county_names since we're validating data for counties without unemployment data and drop dupes, we only need one
# no_county_names = no_county_names[['county_name']]
no_county_names.drop_duplicates(inplace=True)
no_county_names.shape

#only run this if you want a list of names. code above will return 1 column dataframe
# no_county_names_2 = no_county_names['county_name'].tolist()
# no_county_names_2