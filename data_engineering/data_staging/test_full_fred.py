from full_fred.fred import Fred
from full_fred.categories import Categories
import json
from full_fred.series import Series
categories = Categories()
categories.set_api_key_file('full_fred_key.txt')
category_dict = {}
categories_dict = {}
category_dict["categories"]=categories_dict
l_ids_rate_limited = []


def output_file():
    global category_dict
    with open("fred_categories.json", "w") as outfile:
        json.dump(category_dict, outfile, indent=4, sort_keys=True)

def get_category_detail(id):
    if id==1:
        return
    print(id)
    global categories
    global l_ids_rate_limited
    my_cat = categories.get_a_category(id)
    if my_cat is not None and "categories" in my_cat.keys():
        print(my_cat["categories"][0])
        print(categories.get_child_categories(id))
        category_dict["categories"][int(my_cat["categories"][0]["id"])] = my_cat["categories"][0]
        series = categories.get_series_in_a_category(id)
        if len(series.keys())>0:
            for mkey in series["seriess"]:
                print(mkey)
                print("*"*80)
                
        #     category_dict["categories"][int(my_cat["categories"][0]["id"])]["series"]=series
    else:
        print(my_cat)
    if my_cat is not None and "error_code" in my_cat.keys():
        if my_cat["error_message"] == "Too Many Requests.  Exceeded Rate Limit":
            l_ids_rate_limited.append(id)
        print(my_cat)

    if id % 30 == 0:
        output_file()


max_cat = 200000
#for i in range(max_cat):
#    get_category_detail(i)

#get_category_detail(27281)
get_category_detail(27540)
#get_category_detail(27286)


#from copy import deepcopy
#l_ids_rate_limited_copy = deepcopy(l_ids_rate_limited)
#l_ids_rate_limited.clear()

#for id in l_ids_rate_limited_copy:
#    get_category_detail(id)


#output_file()
series = Series()
series.set_api_key_file('full_fred_key.txt')
my_series_object = series.get_a_series("CALOSA7URN")#["seriess"][0]
print(my_series_object)