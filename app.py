import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
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
    nav_menu = option_menu("Main Menu", ["Dashboard", "Map Analyzer", 'Query Analyzer', 'Raw Data'], 
        icons=['clipboard-data', 'map', 'gear'], menu_icon="cast", default_index=0)

if nav_menu == "Dashboard":
    #st.header("Dashboard")

    col_flight, col_average_delay_time, col_max_trip, col_busy_port = st.columns(4)
    no_flight = data.shape[0]
    ave_delay_time = round(data['DEPARTURE_DELAY'].mean(), 2)
    max_frequency=data['AIRLINE'].value_counts().idxmax()
    max_frequency_airpirt=data['DESTINATION_AIRPORT'].value_counts().idxmax()

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
        st.metric(label="Avg. departure delay(min).:hourglass_flowing_sand:", value=ave_delay_time)
    
    with col_max_trip:
        st.metric(label="Top flight operator:male-pilot:", value=max_frequency)

    with col_busy_port:
        st.metric(label="Most busy airport:office:", value=max_frequency_airpirt)

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
            tooltip=['AIRLINE', 'ORIGIN_AIRPORT', 'ELAPSED_TIME', 'FLIGHT_NUMBER', 'DISTANCE', 'DESTINATION_AIRPORT']
        ).interactive()
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    
    col_delay_dpt, col_delay_dist = st.columns(2)

    with col_delay_dpt:
        st.write("Operation performance (Departure Delay)")
        df_delay_dpt = data[(data['DEPARTURE_DELAY'] < 0)]
        
        line_chart_dpt = df_delay_dpt
        line_chart_dpt['SCHEDULED_DEPARTURE'] = pd.to_datetime(line_chart_dpt['SCHEDULED_DEPARTURE'])
        line_chart_dpt['DEPARTURE_HOUR'] = line_chart_dpt['SCHEDULED_DEPARTURE'].dt.hour

        hours_cross_tbl = pd.crosstab(line_chart_dpt['DEPARTURE_HOUR'], line_chart_dpt['ORIGIN_AIRPORT'])
        fig = px.line(hours_cross_tbl)
        
        fig.update_layout(
            #title="Time (Hour) vs Departure Delay (in Min)",
            xaxis_title="Duration (in Hours)",
            yaxis_title="Time delay for departure (in Minutes)",
            legend_title="Airport",
        )
        st.write(fig)

    with col_delay_dist:
        st.write("Opetation performance (Destination Delay)")
        df_delay_dist = data[(data['DESTINATION_DELAY'] < 0)]

        line_chart_dist = df_delay_dist
        line_chart_dist['SCHEDULED_DESTINATION'] = pd.to_datetime(line_chart_dist['SCHEDULED_DESTINATION'])
        line_chart_dist['DESTINATION_HOUR'] = line_chart_dist['SCHEDULED_DESTINATION'].dt.hour

        hours_cross_tbl_dist = pd.crosstab(line_chart_dist['DESTINATION_HOUR'], line_chart_dist['DESTINATION_AIRPORT'])
        fig = px.line(hours_cross_tbl_dist)
        
        fig.update_layout(
            #title="Time (Hour) vs Destination Delay (in Min)",
            xaxis_title="Duration (in Hours)",
            yaxis_title="Time delay for arrival (in Minutes)",
            legend_title="Airport",
        )
        st.write(fig)

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

    col_airline, col_origine_port, col_dist_port = st.columns(3)
    
    with col_airline:
        st.subheader("Flights per airlins")
        max_frequency_airline=data['AIRLINE'].value_counts()
        st.dataframe(max_frequency_airline, use_container_width=True)

    with col_origine_port:
        st.subheader("Flights as per Origine Port")
        max_frequency_origin_port=data['ORIGIN_AIRPORT'].value_counts()
        st.dataframe(max_frequency_origin_port, use_container_width=True)

    with col_dist_port:
        st.subheader("Flights as per Destination Port")
        max_frequency_distination_port=data['DESTINATION_AIRPORT'].value_counts()
        st.dataframe(max_frequency_distination_port, use_container_width=True) 

########### Query Analyzer ##########

elif nav_menu == 'Query Analyzer':
    default_df = pd.DataFrame(data, columns=['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'DEPARTURE_DELAY', 'DESTINATION_DELAY','SCHEDULED_DEPARTURE', 'SCHEDULED_DESTINATION'])
    is_analyzer_select = st.sidebar.radio('Please select option', ('Advance Data Explore', 'Graph Analytics'))
    if is_analyzer_select == 'Advance Data Explore':
        filtered_data_column = pd.DataFrame(data, columns=['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'DEPARTURE_DELAY', 'DESTINATION_DELAY'])
        filtered_df = dataframe_explorer(filtered_data_column, case=False)
        st.dataframe(filtered_df, use_container_width=True)

    elif is_analyzer_select == 'Graph Analytics':
        
        ##########
        df_delay_depture = default_df[(default_df['DEPARTURE_DELAY'] < 0)]
        df_delay_depture['DEPARTURE_DELAY']=df_delay_depture['DEPARTURE_DELAY'].astype('str')
        df_delay_depture['DEPARTURE_DELAY']=df_delay_depture['DEPARTURE_DELAY'].str.replace('-','')
        df_delay_depture['DEPARTURE_DELAY']=df_delay_depture['DEPARTURE_DELAY'].astype('float')

        df_delay_depture['SCHEDULED_DEPARTURE'] = pd.to_datetime(df_delay_depture.SCHEDULED_DEPARTURE, format='%Y-%m-%d %H:%M:%S')
        df_delay_depture['SCHEDULED_DEPARTURE'] = pd.to_datetime(df_delay_depture.SCHEDULED_DEPARTURE, format='%H')
        df_delay_depture['SCHEDULED_DEPARTURE'] = df_delay_depture['SCHEDULED_DEPARTURE'].dt.strftime('%H')

        def plot_dpt():

            df = df_delay_depture

            origin_port_list = df["ORIGIN_AIRPORT"].unique().tolist()

            airPort = st.sidebar.multiselect("Select Airports (You can select more airport)", origin_port_list, default=origin_port_list[0:3])
            
            dfs = {country: df[df["ORIGIN_AIRPORT"] == country] for country in airPort}

            fig = go.Figure()
            for country, df in dfs.items():
                fig = fig.add_trace(go.Scatter(x=df["SCHEDULED_DEPARTURE"], y=df["DEPARTURE_DELAY"], name=country, mode='markers', marker_size=df["DEPARTURE_DELAY"], 
                                               hovertext=df['ORIGIN_AIRPORT']))
                
                fig.update_layout(
                title="Time (Hour) vs Departure Delay (in Min)",
                xaxis_title="Duration (in Hours)",
                yaxis_title="Time delay for departure (in Minutes)",
                legend_title="Airport",
            )

            st.plotly_chart(fig, use_container_width=True)


        plot_dpt()
        ##########
            
    else:
        st.dataframe(data)

########### End of Query Analyzer ##########

elif nav_menu == "Raw Data":

    # Data filtering options
    is_enable_filter = st.sidebar.checkbox('Enable filter')
    if is_enable_filter:
        select_one = st.sidebar.radio("Select any one",('Origin Airport', 'Destination Airport'))
        if select_one == 'Origin Airport':
            options_origin = data['ORIGIN_AIRPORT'].unique().tolist()
            selected_options_origin = st.sidebar.multiselect('Select Origin Airport',options_origin)

            filtered_df_origin = data[data["ORIGIN_AIRPORT"].isin(selected_options_origin)]
            st.dataframe(filtered_df_origin)

        if select_one == 'Destination Airport':
            options_destination = data['DESTINATION_AIRPORT'].unique().tolist()
            selected_options_destination = st.sidebar.multiselect('Select Destination Airport',options_destination)

            filtered_df_destination = data[data["DESTINATION_AIRPORT"].isin(selected_options_destination)]
            st.dataframe(filtered_df_destination)

    else:
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
