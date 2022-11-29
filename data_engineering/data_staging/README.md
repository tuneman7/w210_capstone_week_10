
## Folder contains FRED api work and Merge Work.

Most importantly for Capstone W210, Fall 2022:   
The python program is:  **get_county_unemployment.py**  

The bash wrapper is: **run_fred_download.sh**   -- this will set up necessary dependencies and relies on virtual environments.

This program iterates the "FRED" State Category, it then gets into the "County" series, and then looks for the Monthly Unemployment series and downloads it.   

At present the files are deposited in:   

w210_sec_008_capstone/data_engineering/datasets/fed/monthly_unemployment_by_county/

It tries to re-process errors.  Currently the "Virgin Islands" is the only dataset which appears unable to download.   

## Merge Program 2022-09-16:

The python program is:  **merge_unemployment_with_rdc_frame.py** 

The bash wrapper is: **merge_rdc_data.sh**   -- this will set up necessary dependencies and relies on virtual environments.

The program should be simple enough to read.

Merged files are deposited in:

w210_sec_008_capstone/data_engineering/datasets/merged/

