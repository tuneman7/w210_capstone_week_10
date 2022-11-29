import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Forecasting Demo",
    page_icon="🎈",
)


def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


def predict(data, county):

    return 'prediction'


_max_width_()


st.title('Forecasting Demo')

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *Forecasting Demo* app is an easy-to-use interface built in Streamlit to help users understand the modeling process for our real estate forcasting project
-   It uses prophet (FB time series package) for prediction
	    """
    )

st.markdown("Data")


data = pd.read_csv('../model_building/cleaned_data.csv')


option = st.selectbox(
    'Choose a county',
    data.county_name.unique())

st.write('You selected:', option)

st.dataframe(data.loc[data.county_name == option])

col1, col2, col3 = st.columns(3)
col1.metric("Reading complexity", "70 °F", "1.2 °F")
col2.metric("Total Length", "9", "-8% to average")
col3.metric("Place Holder metric", "22", "4%")
