import pandas as pd
import time
import warnings
import numpy as np

# TO DO, need to do missing data fill for year over year and month over month percentage change

# TO DO replace unemployment rate with federal unemployement rate for that year? or that month? whichever is easiest

# ignoring warnings to reduce clutter in terminal. prob not best practice, but eh
warnings.filterwarnings('ignore')

# not using population or GDP or personal income per capita, can't figure out bug, but can come back to it
columns = ['median_listing_price', 'active_listing_count', 'median_days_on_market',
           'unemployment_rate', 'thirty_year_interest_rate_four'
           ]


def read_data():
    """
    Reads in our merged realtor data set
    """

    raw_data = pd.read_csv(
        '../data_engineering/datasets/merged/rdc_data_merged_with_unemployment_and_lagged_interest_rate.csv',
        dtype={'month_date_yyyymm': str, 'county_fip': str, 'quality_flag': str, 'unemployment_rate': float})

    raw_data.rename(columns={'month_date_yyyymm': 'date_raw'}, inplace=True)

    # dropping last row b/c it's contact info for realtor.com
    raw_data.drop(raw_data.tail(1).index, inplace=True)

    # creating date column in format yyymmdd by appending 01 as day
    raw_data['date_raw'] = raw_data['date_raw'].astype(str) + '01'

    raw_data['date'] = pd.to_datetime(raw_data['date_raw'], format="%Y%m%d")

    # replacing 'none' value with NA for na.replace
    raw_data = raw_data.replace('none', np.nan)

    print("Columns: ", raw_data.columns)

    return raw_data


def fill_missing_values(data):
    """
    Fills missing values with mean for FIP county for non-time comparison variables in data

    Parameters:
        data (DataFrame): Realtor dataframe merged with additional sources

    Returns:
        data (DataFrame): Realtor dataframe with missing values filled
    """

    for column in columns:
        print("Filling missinge values for ", column, " column")

        # fill by mean of column for specific county fip
        data[column] = data.groupby("county_fips").transform(
            lambda x: x.fillna(x.mean()))[column]

    return data


def add_pending_ratio(data):
    """
    Adds pending ratio to dataset now that there's no more missing values.
    The ratio of the pending listing count to the active listing count within the
    specified geography during the specified month.

    Parameters:
        data (DataFrame): Realtor dataframe merged with additional sources

    Returns:
        data (DataFrame): Realtor dataframe pending ratio filled
    """

    data['pending_ratio'] = data['pending_listing_count'].astype('int64') / \
        data['active_listing_count'].astype('int64')

    return data


def clean_data(data):
    """
    Contains different steps for cleaning data

    Parameters:
        data (DataFrame): Realtor dataframe merged with additional sources

    Returns:
        data (DataFrame): A cleaned dataset :)
    """
    filled_values_data = fill_missing_values(data)
   #data_with_pending_ratio = add_pending_ratio(filled_values_data)

    return filled_values_data


def import_cleaned_data():
    """
    This function is extra, but wanted to make the joke about going from 
    raw data to cooked (or cleaned) data :P 
    """

    raw_data = read_data()

    cooked_data = clean_data(raw_data)

    additional_columns = ['date', 'county_fips', 'county_name']

    cooked_data[columns +
                additional_columns].to_csv('cleaned_data.csv', index=False)


if __name__ == "__main__":
    start_time = time.time()
    import_cleaned_data()
    print("--- %s seconds ---" % (float(time.time()) - float(start_time)))
