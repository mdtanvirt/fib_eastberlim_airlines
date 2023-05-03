import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
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

with st.sidebar:
    nav_menu = option_menu("Main Menu", ["Dashboard", "Query Analyzer", 'Raw Data'], 
        icons=['clipboard-data', 'map', 'gear'], menu_icon="cast", default_index=0)

if nav_menu == "Dashboard":
    st.header("Dashboard")

elif nav_menu == "Query Analyzer":
    st.header("Data exploration with map")

    '''
    ###############
     # Use pandas to prepare data for tooltip
    #data["ORIGIN_AIRPORT"] = data["ORIGIN_AIRPORT_POS"].apply(lambda f: f["ORIGIN_AIRPORT_LON", "ORIGIN_AIRPORT_LAT"])
    #data["DESTINATION_AIRPORT"] = data["DESTINATION_AIRPORT_POS"].apply(lambda t: t["DESTINATION_AIRPORT_LON", "DESTINATION_AIRPORT_LAT"])

    # Define a layer to display on a map
    GREEN_RGB = [0, 255, 0, 40]
    RED_RGB = [240, 100, 0, 40]

    layer = pdk.Layer(
        "GreatCircleLayer",
        data,
        pickable=True,
        get_stroke_width=12,
        get_source_position=["ORIGIN_AIRPORT_LON", "ORIGIN_AIRPORT_LAT"],
        get_target_position=["DESTINATION_AIRPORT_LON", "DESTINATION_AIRPORT_LAT"],
        get_source_color=RED_RGB,
        get_target_color=GREEN_RGB,
        auto_highlight=True,

    )

    view_state = pdk.ViewState(bearing=45, pitch=50, zoom=8,)

    TOOLTIP_TEXT = {"html": "{S000} jobs <br /> Home of commuter in red; work location in green"}
    r = pdk.Deck(layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
    r.to_html("layer.html")'''

    ###########################

    chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    ##########################

   

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