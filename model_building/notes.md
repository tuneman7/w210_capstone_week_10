Link to [Realtor data dicitonary](https://www.realtor.com/research/data/). Scroll to bottom to see data dictionary.

median_listing_price - fill with average
active_listing_count - fill with average
new_listing_count - fill with average 
price_increased_count - fill with average
price_reduced_count - fill with average
pending_listing_count - fill with average
median_listing_price_per_square_foot - fill with average
median_square_feet - fill with average 
average_listing_price - fill with average
total_listing_count - fill with average
pending_ratio - need to use two other columns to calculate this column
quality_flag - doesn't need to be modeled so not going to clean or fill missing values 
unemployment_rate - fill with national average if missing, this was missing a couple thousand of data


Models and notes in question
* (Varimax)[https://stackoverflow.com/questions/17628589/perform-varimax-rotation-in-python-using-numpy]
    * https://pyflux.readthedocs.io/en/latest/var.html 
* (pooled ols)[https://timeseriesreasoning.com/contents/pooled-ols-regression-models-for-panel-data-sets/]
* (LSTM multivariate)[https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/]
