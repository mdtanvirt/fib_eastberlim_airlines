import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import altair as alt
#from streamlit_card import card
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    header {visibility: hidden}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

data_url= "https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv"
data = pd.read_csv(data_url)
# df for airlines frequency 
df_airlines_frequency_count = data.groupby(['AIRLINE']).agg(
    count = pd.NamedAgg(column='AIRLINE', aggfunc='count')
)

with st.sidebar:
    nav_menu = option_menu("Main Menu", ["Dashboard", "Map Analyzer", 'Raw Data'], 
        icons=['clipboard-data', 'map', 'gear'], menu_icon="cast", default_index=0)

if nav_menu == "Dashboard":
    st.header("Dashboard")

    col_flight, col_average_delay_time, col_max_trip = st.columns(3)
    no_flight = data.shape[0]
    ave_delay_time = round(data['DEPARTURE_DELAY'].mean(), 2)
    max_frequency=data['AIRLINE'].value_counts().idxmax()

    st.markdown(
    """
    <style>
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    overflow-wrap: break-word;
    white-space: break-spaces;
    color: Black;
    }
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div p {
    font-size: 130% !important;
    font-family:sans-serif;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    

    with col_flight:
        st.metric(label="Total no. of flights:airplane_departure:", value=no_flight)

    with col_average_delay_time:
        st.metric(label="Avg. departure delay in min.:hourglass_flowing_sand:", value=ave_delay_time)
    
    with col_max_trip:
        st.metric(label="Top flight Operator:male-pilot:", value=max_frequency)

    col_barChart, col_scat_chart = st.columns(2)

    with col_barChart:
        st.write('Number of flights operate by Airline')
        st.bar_chart(df_airlines_frequency_count)
    
    with col_scat_chart:
        st.write('Elapsed Time vs Distance')
        chart = alt.Chart(data).mark_circle(size=60).encode(
            x='DISTANCE',
            y='ELAPSED_TIME',
            color='AIRLINE',
            tooltip=['AIRLINE', 'ORIGIN_AIRPORT', 'ELAPSED_TIME', 'FLIGHT_NUMBER', 'DISTANCE']
        ).interactive()
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        #st.line_chart(['DEPARTURE_DELAY', 'AIRLINE'])

elif nav_menu == "Map Analyzer":
    st.header("Data exploration with map")

    GREEN_RGB = [0, 255, 0, 0]
    RED_RGB = [250, 100, 0, 40]


    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=38.5260,
            longitude=-115.766,
            zoom=3,
            pitch=2,
        ),
        layers=[
            pdk.Layer(
            "GreatCircleLayer",
            data=data,
            pickable=True,
            get_stroke_width=20,
            get_source_position=["ORIGIN_AIRPORT_LON", "ORIGIN_AIRPORT_LAT"],
            get_target_position=["DESTINATION_AIRPORT_LON", "DESTINATION_AIRPORT_LAT"],
            get_source_color=RED_RGB,
            get_target_color=GREEN_RGB,
            auto_highlight=True,
            ),
        ],
    ))

   

elif nav_menu == "Raw Data":
    st.header("Raw data")
    st.dataframe(data)

    @st.cache_data
    def convert_df(data):
        return data.to_csv().encode('utf-8')
    
    csv = convert_df(data)

    st.download_button(
        label='Download Data',
        data=csv,
        file_name='raw.csv',
        mime='text/csv',
    )