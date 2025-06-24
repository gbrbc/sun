import sys
import os
import pandas as pd

import geopandas as gpd            
import numpy as np

#######PRN#########
#from pybdshadow import *
#from analysis import *

import matplotlib.pyplot as plt

from shapely  import wkt
from shapely.wkt  import loads
from shapely.geometry  import Polygon,mapping


import json


def Deb(msg=""):
  print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}",flush=True)
  sys.stdout.flush()




def convert_multipolygon(gdf9):
    gdf_approx = gpd.GeoDataFrame({'id': [1], 'geometry': [gdf9]}, crs="WGS84")

    # Calculate the convex hull and assign it back to a new GeoDataFrame or replace the geometry
    convex_hull_gs = gdf_approx.geometry.convex_hull
    # To put it into a GeoDataFrame, you can create a new one or update an existing one
    gdf_convex_hull = gpd.GeoDataFrame(gdf_approx.drop(columns=['geometry']), geometry=convex_hull_gs, crs=gdf_approx.crs)
    
    return gdf_convex_hull.iloc[0,1]





pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)





#######################MULTI TO POLYGON#######################

df = pd.read_csv("path1.csv")

df['geometry'] = df['geometry'].apply(loads)
gdf1 = gpd.GeoDataFrame(df, crs="wgs84")  # Replace "your_crs"


gdf1.to_file("/tmp/file_whole2.json",driver='GeoJSON')


#print(gdf1.geometry.data_type)

gdf1['geometry'] = gdf1['geometry'].apply(convert_multipolygon)




