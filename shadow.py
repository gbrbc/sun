import sys
import os
import pandas as pd

import geopandas as gpd
import numpy as np

from mysun.pybdshadow import *
#import analysis
#from analysis import cal_sunshine
from mysun.analysis import *



from shapely  import wkt
from shapely.wkt  import loads

# in Jupyter this lets us show the figures, but not interactively
##%matplotlib inline

from shapely.geometry import Point, LineString, Polygon
##https://iamdonovan.github.io/teaching/egm722/practicals/vector.html

## the one I used for SPA on gbrmail is avialble as py module
## https://github.com/s-bear/sun-position

#https://www.fs.usda.gov/nac/buffers/guidelines/5_protection/6.html#:~:text=Use%20the%20formula%20s%20%3D%20h,shadow%20direction%20on%20the%20ground.

'''
Use the formula s = h/tan A to calculate shadow length. See the table below for an example. Sun angle calculators are available on the Web which will provide the sun angle (A) and azimuth angle for a given location based on the date and time.



'''


def LINE():
    return "Line: " +  str(sys._getframe(1).f_lineno) + "  "

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



df = pd.read_csv("path1.csv")
df['geometry'] = df['geometry'].apply(loads)
gdf1 = gpd.GeoDataFrame(df, crs="wgs84")  # Replace "your_crs"


print(LINE(), " First geom ",    gdf1['geometry'])
print("And the columns ")

gdf=gpd.GeoDataFrame(gdf1)

print("23656")
print(LINE(),gdf1," ==== ",type(gdf1))






fred=gdf.to_json(to_wgs84=True)

print(LINE(),fred)



#gs=gdf['the_geom']

def try1():
    #if not isinstance(gs,pd.DataFrame):
    #    print(type(gs))

    print("blah")
    #print(gdf[['the_geom']])

    gdf.plot(markersize=.5)

    #print(gdf["centroid"])




def try2():
    #Given UTC datetime
    date = pd.to_datetime('2022-01-01 3:45:33.959797119')\
        .tz_localize('Asia/Shanghai')\
        .tz_convert('UTC')
    #Calculate building shadow for sun light
    print(LINE(), "try2 to shadows")


    print(LINE(), 'puce')
    print(gdf1)
    print(type(gdf1))

    gdf9 = gdf1.iloc[0,0]
#    gdf9 = gpd.GeoDataFrame(gdf1.iloc[0,0], crs="wgs84")
    print(LINE(), 'sluce')
    print(gdf1.iloc[0,0])
    print(LINE(), 'spruce')
    print(type(gdf1.iloc[0,0]))
    
    print('prestar')
    print(LINE(),gdf9)
    print(LINE(),type(gdf9))
    print('end prestar')
    



###GBR add?    gdf2 = gpd.GeoDataFrame(gdf9)


    gdf_approx = gpd.GeoDataFrame({'id': [1], 'geometry': [gdf9]}, crs="WGS84")


    # Calculate the convex hull and assign it back to a new GeoDataFrame or replace the geometry
    convex_hull_gs = gdf_approx.geometry.convex_hull
    # To put it into a GeoDataFrame, you can create a new one or update an existing one
    gdf_convex_hull = gpd.GeoDataFrame(gdf_approx.drop(columns=['geometry']), geometry=convex_hull_gs, crs=gdf_approx.crs)


  #  print(gdf_convex_hull.iloc[0,1])
    print('premauve')
    print(gdf_approx)
    print(type(gdf_approx))
    print('end premauve')
    print(LINE(),' preassign ', gdf1.head())
    print(LINE(),' preassign ', gdf1.loc[0])
#    print(gdf1,try4(gdf1.iloc[0,0]))
    gdf1.iloc[0,0] = gdf_convex_hull.iloc[0,1]
    bambam=gdf_convex_hull.to_json(to_wgs84=True)
    print(LINE(),'bambam')
    print(LINE(),' postassign ', gdf1.head())
    print(LINE(),' postassign ', gdf1.iloc[0])
#    print(gdf1,try4(gdf1.iloc[0,0]))
    








##    gdf1.iloc[0,0]=np.nan

    print(LINE(),' postassign2 ', gdf1.iloc[0,0])
    print(gdf1)


#    print('coords')
#    print(gdf1.loc[0.0].coords)


    print(LINE(), 'mauve')

    for j in range(0,16):
        print(j,":  ",gdf1.iloc[0,j])
    print(LINE(), 'mauveish')
    print(gdf1)
    print(LINE(), 'mauve 1')
    print(type(gdf1))
#    peter=gdf1.to_json(to_wgs84=True)
#    print(gdf1.to_json(peter))

    print(LINE(), 'mauve out')

###this crashes in bdshad.... below
#    buildingshadow = building.copy()
#    a = buildingshadow['geometry'].apply(lambda r: list(r.exterior.coords))


    print(LINE(),"teal")
    gdf1.head()
    wilma=gdf.to_json(to_wgs84=True)

    print(LINE(),wilma)

    exit()


    mymy = cal_sunshine(gdf1)



    shadows = pybdshadow.bdshadow_sunlight(gdf1,date)    

#possible answer
##https://gis.stackexchange.com/questions/188622/rounding-all-coordinates-in-shapely

def try3(fred):
    ## print numbers for a polygon
    import matplotlib.pyplot as plt
    from shapely.geometry import Polygon
    print(LINE(),"  Try3  ",type(fred))
    g=gpd.GeoSeries([fred])
    print("Try3 ",g[0])



def try4(fred):
    ## print plot for a polygon
    import matplotlib.pyplot as plt
    from shapely.geometry import Polygon
    g=gpd.GeoSeries([fred])
    g.plot()
    plt.show()




try2()


###https://people.csail.mit.edu/ericchan/bib/pdf/p275-atherton.pdf
##doesnt take sun into account
##
##have pysolar in Downloads

## https://data.cityofnewyork.us/City-Government/BUILDING/5zhs-2jue/about_data
## SHAPE_AREA  Measures the enclosed area within a polygon.
## 
