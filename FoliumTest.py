import pandas as pd
import numpy as np
#import geopandas as gpd
#from shapely.geometry import Point
import matplotlib
import matplotlib.pyplot as plt 
import folium
import os
from IPython.display import display
import streamlit as st
from streamlit_folium import folium_static

st.title('Folium Python QuickMap')
m = folium.Map (
    location = [40.71981037548853, -74.00258103213994],
    #tiles='Mapbox Bright',
    #zoom_start = 11
)

folium_static(m)

col_names = ['UserID', 'VenueID', 'VenueCategoryID', 'VenueCategoryName', 'Latitude', 'Longtitude','Timezone', 'UTCtime']
# read the csv with pandas. the data comes in tab seperator. 
file_name = (f'C:\\Users\\CarolineNeel\\NOTEBOOKS\\dataset_TSMC2014_NYC.txt')
nyc = pd.read_csv(file_name,names=col_names,sep="\t",  encoding = "ISO-8859-1" )
#create geometry
#geometry = [Point(xy) for xy in zip(nyc['Longtitude'], nyc['Latitude'])]
# Create crs dictionary
#crs = {'init': 'epsg:4326'}
#nyc_gdf = gpd.GeoDataFrame(nyc, crs=crs, geometry=geometry)
# reporject
#nyc_gdf_proj = nyc_gdf.to_crs({'init': 'epsg:32618'})

