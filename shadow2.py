import sys
import os
import pandas as pd

import geopandas as gpd

#import pybdshadow
from mysun.pybdshadow import *
#import analysis
#from analysis import cal_sunshine
from mysun.analysis import *



from shapely.wkt  import loads
from shapely import unary_union
import io
global gdf

def LINE():
    return "Line: " +  str(sys._getframe(1).f_lineno) + "  "



df = pd.read_csv("path1.csv")
df['geometry'] = df['the_geom'].apply(loads)
gdf = gpd.GeoDataFrame(df, crs="wgs84")  # Replace "your_crs"



def try2():
    #Given UTC datetime
    global gdf
    date = pd.to_datetime('2022-01-01 2:45:33.959797119')\
        .tz_localize('Asia/Shanghai')\
        .tz_convert('UTC')
    #Calculate building shadow for sun light
    print(LINE(), "try2 to shadows")

    print(LINE(), " exterior ", gdf.bounds)
    print(LINE(),gdf.iloc[0,0])

#    gdf1=gdf.iloc[0,0]

#    df = pd.read_csv(io.StringIO(gdf1))
#    gdf2 = gpd.GeoDataFrame(df, crs="wgs84",geometry=df[0])  # Replace "your_crs"

#    print(LINE(), " exterior2 ", gdf1.bounds)
#    print(unary_union(gdf.iloc[0,0]).area)

#    x, y = [gdf_item.geometry.exterior.xy for gdf_item in gdf]
    print("exit")
    exit()

    shadows = bdshadow_sunlight(gdf,date)    
#    mymy = cal_sunshine(gdf)


def try3():
    area=gdf['SHAPE_AREA'].iloc[0]
    length=gdf['SHAPE_AREA'].iloc[0]
    print("area ",gdf['SHAPE_AREA'].iloc[0])

    print("length ",gdf['Length'].iloc[0])
    area=float(area)
    length=float(length)
    width=float(area/length)
    print(LINE(), "width ", type(width))
    print( width, "  ",1586.48/212.29)

    



try2()




