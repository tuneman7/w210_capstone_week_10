import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from utility import Utility


my_utility = Utility()




#load the CSVS into objects


#unemployment data directory:
folder_location = os.getcwd()
ue_data_dir = os.path.abspath(os.path.join(folder_location, os.pardir ,"datasets","fed","monthly_unemployment_by_county"))
#unemployment data objects
ue_full_file_paths,ue_file_names,ue_loc_dict, ue_data_frames = my_utility.view_file_types(file_filter="*.csv",
                                            return_pandas_data_frames=True,
                                            directory=ue_data_dir,
                                            print_file_names_only=False)


#RDC data (single file)
core_data_directory = os.path.abspath(os.path.join(folder_location, os.pardir ,"datasets","realtor"))
#RDC data (single file)
rdc_full_file_paths, rdc_file_names, rdc_loc_dict, rdc_data_frames = my_utility.view_file_types(file_filter="RDC_Inventory_Core_Metrics_County_History.csv",
                                             return_pandas_data_frames=True,
                                             directory=core_data_directory,
                                             print_file_names_only=True)



#print(rdc_full_file_paths)


merged_unemployment = None

#for each of the counties change it to county_name, yearmonth, value
my_counter = 0
for key in ue_data_frames.keys():
    df = ue_data_frames[key]
    splitted_fn = key.split('_')
    state = splitted_fn[len(splitted_fn)-2]
    series_and_csv = splitted_fn[len(splitted_fn)-1]
    county_name = key.replace("county","").replace(series_and_csv,"").replace(state,"").replace("unemployment_rate_in_","").replace("_"," ").replace("umployment rate in ","").replace("unemployment rate  ","").replace("unemploynt rate in ","").strip()
    #print(key)
    county_name = county_name + ", " + state
    #print(county_name)
    sql = '''
    select \'''' + county_name + '''\' as county_name,
    replace(substr(date,1,7),'-','') as yearmonth,
    value
    from df
    '''
    
    #    merged_unemployment
#    join rdc_data
#    on rdc_data.month_date_yyyymm = replace(substr(date,1,7),'-','')
    
    #print(sql)
    #break
    my_result = psql.sqldf(sql)
    #pd.set_option('display.max_rows', my_result.shape[0]+1)
    #pd.set_option('display.max_rows', 20)
    #print('my_result','\n',my_result)
    
    #dump it into the data frame
    #ue_data_frames[key] = df
    
    if my_counter == 0:
        merged_unemployment = my_result
    else:
        merged_unemployment = merged_unemployment.append(my_result,ignore_index=True)
        #print(county_name)
    
    my_counter = my_counter+1
    
    #break
    

print("*"*100)
print("FINISHED RUNNING THE MERGE ABOUT TO DO A JOIN")
print("*"*100)

print("*"*100)
print("CHECK WHAT WAS DONE")
print("*"*100)

#check what we have just done:

print(len(ue_data_frames.keys()))
sql = '''
select count(distinct county_name) from merged_unemployment
'''
my_result = psql.sqldf(sql)
pd.set_option('display.max_rows', my_result.shape[0]+1)
pd.set_option('display.max_rows', 20)
print('my_result','\n',my_result)

#now merge the stuff
rdc_data = rdc_data_frames["RDC_Inventory_Core_Metrics_County_History.csv"]

print("*"*100)
print("DOING THE JOIN")
print("*"*100)


sql = '''
select
    rdc_data.*,
    merged_unemployment.value as unemployment_rate
from rdc_data
left join merged_unemployment
on rdc_data.month_date_yyyymm = merged_unemployment.yearmonth
and rdc_data.county_name = merged_unemployment.county_name
'''
merged_frame = psql.sqldf(sql)
pd.set_option('display.max_rows', my_result.shape[0]+1)
pd.set_option('display.max_rows', 20)
#print('my_result','\n',my_result)

print("*"*100)
print("JOIN COMPLETE")
print("*"*100)


#check out the join results.

sql = '''
select
    count(*) from merged_frame 
'''
my_result = psql.sqldf(sql)
pd.set_option('display.max_rows', my_result.shape[0]+1)
pd.set_option('display.max_rows', 20)
print('my_result','\n',my_result)

print("*"*100)
print("TOTAL RDC RECORDS")
print("*"*100)

sql = '''
select
    count(*) from merged_frame where unemployment_rate == 0
'''
my_result = psql.sqldf(sql)
pd.set_option('display.max_rows', my_result.shape[0]+1)
pd.set_option('display.max_rows', 20)
print('my_result','\n',my_result)


print("*"*100)
print("RDC RECORDS MATCHED")
print("*"*100)


sql = '''
select
    distinct * from merged_frame where unemployment_rate is null
'''
my_result = psql.sqldf(sql)
#pd.set_option('display.max_rows', my_result.shape[0]+1)
pd.set_option('display.max_rows', 20)
print('my_result','\n',my_result)

not_joined = my_result

#save off the file

print("*"*100)
print("WRITING THE FILES")
print("*"*100)

folder_location = os.getcwd()
folder_location = os.path.abspath(os.path.join(folder_location, os.pardir ,"datasets","merged"))

if not os.path.exists(folder_location):
    os.makedirs(folder_location)
    
file = os.path.join(folder_location,"rdc_data_merged_with_unemployment.csv")

if os.path.exists(file):
    os.remove(file)

merged_frame.to_csv(file,index=False) 

print("*"*100)
print(file)
print("*"*100)

    
file = os.path.join(folder_location,"rdc_data_not_matched.csv")

if os.path.exists(file):
    os.remove(file)

    
not_joined.to_csv(file,index=False) 

print("*"*100)
print(file)
print("*"*100)