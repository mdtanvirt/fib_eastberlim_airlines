import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

data_url= "https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv"
df = pd.read_csv(data_url)

st.dataframe(df)