from full_fred.fred import Fred
from full_fred.categories import Categories
import json
from full_fred.series import Series
import json
import os
from os import path
import pandas as pd
import numpy as np
import time
from time import sleep

categories = Categories()
series = Series()
categories.set_api_key_file('full_fred_key.txt')
series.set_api_key_file('full_fred_key.txt')
category_dict = {}
categories_dict = {}
category_dict["categories"]=categories_dict
l_ids_rate_limited = []


import unicodedata
import string

valid_filename_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')
    filename = filename.replace("%","_pct_")

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]


def output_file():
    global category_dict
    with open("fred_categories.json", "w") as outfile:
        json.dump(category_dict, outfile, indent=4, sort_keys=True)

def is_series_file_there(filename):        
    folder_location = os.getcwd()
    folder_location = os.path.abspath(os.path.join(folder_location, os.pardir ,"datasets","fed","monthly_unemployment_by_county"))
    file_name = os.path.join(folder_location,clean_filename(filename) + ".csv")
    if not os.path.exists(file_name):
        return False
    else:
        return True

def save_series_file(filename,my_data_frame):
    
    folder_location = os.getcwd()
    folder_location = os.path.abspath(os.path.join(folder_location, os.pardir ,"datasets","fed","monthly_unemployment_by_county"))
    
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)
    
    file_name = os.path.join(folder_location,clean_filename(filename) + ".xlsx")
    print(file_name)
    
    with pd.ExcelWriter(file_name,engine='xlsxwriter') as writer:
        my_data_frame.to_excel(writer,sheet_name="Sheet1",freeze_panes=(1,0))
        writer.save()
    
    file_name = os.path.join(folder_location,clean_filename(filename) + ".csv")
    
    print(file_name)
    
    with open(file_name, "w") as outfile:
        my_data_frame.to_csv(outfile)
    

def re_try_error_states(my_l_state_keys_with_errors,my_l_state_names_with_errors):    

    did_sleep = False
    print("*"*80)
    print("THE NUMBER OF PROBLEMS ARE:")
    print("*"*80)    
    print(len(my_l_state_names_with_errors))
    print("*"*80)    
    print("*"*80)
    print("The problem children are:")
    print("*"*80)    
    print(my_l_state_names_with_errors)
    print("*"*80)    
    
    
    l_state_keys_with_errors = []
    l_state_names_with_errors = []
    my_counter = 0
    for my_id in my_l_state_keys_with_errors :        
        
        #if not my_state["name"] in ["Alaska","Connecticut"]:
        #    continue

        my_state_id     = my_id
        my_state_name   = my_l_state_names_with_errors[my_counter]
        my_counter      = my_counter+1
        my_iterator     = 0
        
        print("*"*80)
        print("Doing re-try for:", my_state_name)
        print("*"*80)
        
        #print(my_state)
        time.sleep(2)
        try:

            categories = Categories()
            series = Series()
            categories.set_api_key_file('full_fred_key.txt')
            series.set_api_key_file('full_fred_key.txt')

            state_details = categories.get_child_categories(my_id)["categories"][0]
            if state_details["name"] == "Counties":
                time.sleep(1)

                categories = Categories()
                series = Series()
                categories.set_api_key_file('full_fred_key.txt')
                series.set_api_key_file('full_fred_key.txt')

                print(state_details)
                for county in categories.get_child_categories(state_details["id"])["categories"]:
                    my_iterator = my_iterator + 1

                    print(county)
                    print(county["id"])

                    if my_iterator % 2 == 0 and not did_sleep:
                        sleep(1.4)
                        did_sleep=True
                    if my_iterator % 5 == 0 and not did_sleep:
                        sleep(2)
                        did_sleep=True    
                    if my_iterator % 9 == 0 and not did_sleep:
                        sleep(1.5)
                        did_sleep=True
                    if my_iterator % 13 == 0 and not did_sleep:
                        sleep(2.5)
                        did_sleep=True                                
                    
                    print("*"*80)
                    print("THE NUMBER OF PROBLEMS ARE:")
                    print(len(my_l_state_names_with_errors))
                    print("*"*80)    
                    print("*"*80)
                    print("THE NUMBER OF PROBLEMS THIS ITERATION:")
                    print(len(l_state_names_with_errors))
                    print("*"*80)    

                    county_details = categories.get_series_in_a_category(county["id"])
                    #print(county_details)
                    if len(county_details.keys())>0:
                        for mkey in county_details["seriess"]:
                            if ("unemployment" in mkey["title"].lower()) and ("monthly" in mkey["frequency"].lower()) :
                                #print(mkey)
                                file_name = mkey["title"].lower() + "_" + mkey["id"]
                                if is_series_file_there(file_name):
                                    continue
                                series = Series()
                                series.set_api_key_file('full_fred_key.txt')
                                my_data_frame = series.get_series_df(mkey["id"])
                                my_series_object = series.get_a_series(mkey["id"])["seriess"][0]
                                save_series_file(file_name,my_data_frame)
                                print("*"*80)
                                my_iterator = my_iterator + 1

                                if my_iterator % 2 == 0 and not did_sleep:
                                    sleep(1.4)
                                    did_sleep=True
                                if my_iterator % 5 == 0 and not did_sleep:
                                    sleep(2)
                                    did_sleep=True    
                                if my_iterator % 9 == 0 and not did_sleep:
                                    sleep(1.5)
                                    did_sleep=True
                                if my_iterator % 13 == 0 and not did_sleep:
                                    sleep(2.5)
                                    did_sleep=True                                

                                series = None
                                did_sleep=False
                                
                                
        except Exception as e:
            print("*"*80)
            print("Something went wrong:")
            print(e)
            print("*"*80)
            l_state_keys_with_errors.append(my_state_id)
            l_state_names_with_errors.append(my_state_name)
            
            print("*"*80)
            print("THE NUMBER OF PROBLEMS ARE:")
            print(len(my_l_state_names_with_errors))
            print("*"*80)    
            print("*"*80)
            print("THE NUMBER OF PROBLEMS THIS ITERATION:")
            print(len(l_state_names_with_errors))
            print("*"*80)  
            time.sleep(8)
            series = None
            categories = None
            did_sleep = False
            
            
            
    return l_state_keys_with_errors,l_state_names_with_errors
    
        
def get_county_unemployment_series(id):
    if id==1:
        return
    print(id)
    global categories
    global l_ids_rate_limited
    my_cat = categories.get_a_category(id)
    l_state_keys_with_errors = []
    l_state_names_with_errors = []
    my_iterator = 0
    if my_cat is not None and "categories" in my_cat.keys():
        print(my_cat)
        if my_cat["categories"][0]["name"] == "States":
            #print(categories.get_child_categories(id))
            for my_state in categories.get_child_categories(id)["categories"]:
                #if not my_state["name"] in ["Alaska","Connecticut"]:
                #    continue
                my_iterator = my_iterator + 1
                my_state_id = my_state["id"]
                my_state_name = my_state["name"]
                
                print(my_state)
                time.sleep(2)
                try:
                    
                    categories = Categories()
                    series = Series()
                    categories.set_api_key_file('full_fred_key.txt')
                    series.set_api_key_file('full_fred_key.txt')
                    
                    state_details = categories.get_child_categories(my_state["id"])["categories"][0]
                    if state_details["name"] == "Counties":
                        time.sleep(1)
                       
                        categories = Categories()
                        series = Series()
                        categories.set_api_key_file('full_fred_key.txt')
                        series.set_api_key_file('full_fred_key.txt')
                        
                        print(state_details)
                        for county in categories.get_child_categories(state_details["id"])["categories"]:
                            my_iterator = my_iterator + 1
                            
                            print(county)
                            print(county["id"])
                            county_details = categories.get_series_in_a_category(county["id"])
                            my_iterator = my_iterator + 1

                            if my_iterator % 2 == 0 and not did_sleep:
                                sleep(1.4)
                                did_sleep=True
                            if my_iterator % 5 == 0 and not did_sleep:
                                sleep(2)
                                did_sleep=True    
                            if my_iterator % 9 == 0 and not did_sleep:
                                sleep(1.5)
                                did_sleep=True
                            if my_iterator % 13 == 0 and not did_sleep:
                                sleep(2.5)
                                did_sleep=True                                
                            series = None
                            did_sleep=False                        
                            #print(county_details)
                            if len(county_details.keys())>0:
                                for mkey in county_details["seriess"]:
                                    if ("unemployment" in mkey["title"].lower()) and ("monthly" in mkey["frequency"].lower()) :
                                        #print(mkey)
                                        file_name = mkey["title"].lower() + "_" + mkey["id"]
                                        if is_series_file_there(file_name):
                                            continue
                                        series = Series()
                                        series.set_api_key_file('full_fred_key.txt')
                                        my_data_frame = series.get_series_df(mkey["id"])
                                        my_series_object = series.get_a_series(mkey["id"])["seriess"][0]
                                        save_series_file(file_name,my_data_frame)
                                        print("*"*80)
                                        my_iterator = my_iterator + 1

                                        if my_iterator % 2 == 0 and not did_sleep:
                                            sleep(1.4)
                                            did_sleep=True
                                        if my_iterator % 5 == 0 and not did_sleep:
                                            sleep(2)
                                            did_sleep=True    
                                        if my_iterator % 9 == 0 and not did_sleep:
                                            sleep(1.5)
                                            did_sleep=True
                                        if my_iterator % 13 == 0 and not did_sleep:
                                            sleep(2.5)
                                            did_sleep=True                                
                                            
                                        series = None
                                        did_sleep=False
                                        
                except Exception as e:
                    print("*"*80)
                    print("Something went wrong:")
                    print(e)
                    print("*"*80)
                    if my_state_name.lower().strip() == "virgin islands":
                        continue
                    l_state_keys_with_errors.append(my_state_id)
                    l_state_names_with_errors.append(my_state_name)
                    
                    print("*"*80)
                    print("THE NUMBER OF PROBLEMS THIS ITERATION:")
                    print(len(l_state_names_with_errors))
                    print("*"*80)  
                    
                    
                    time.sleep(8)
                    series = None
                    categories = None
    
    return l_state_keys_with_errors,l_state_names_with_errors
                    


#27281 is the FRED category for States
#while True:
#    time.sleep(.5)
#    l_state_keys_with_errors=get_county_unemployment_series(27281)
l_state_keys_with_errors,l_state_names_with_errors=get_county_unemployment_series(27281)

while len(l_state_keys_with_errors)>0:
    print("*"*100)
    print("*"*100)
    print("DOING ERRORS")
    print("*"*100)
    print("*"*100)
    l_state_keys_with_errors,l_state_names_with_errors = re_try_error_states(l_state_keys_with_errors,l_state_names_with_errors)


    

#output_file()
#series = Series()
#series.set_api_key_file('full_fred_key.txt')
#my_series_object = series.get_a_series("CALOSA7URN")#["seriess"][0]
#print(my_series_object)
