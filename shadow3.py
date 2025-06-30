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


global gdf1


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


#############################################
##PACKAGE INSERT TO BE TESTED
#############################################

from shapely.geometry import Point, LineString, Polygon
from datetime import date,datetime,timezone
import suncalc
import math  # For mathematical calculations

heknows = []
counter=0


#######SUPPORT FOR SWAP LAT LONG###########

def swappoint(apoint):
    return([apoint.y,apoint.x])

def swaplist(alist):
    retrn=[]
    for m in alist:
        retrn.append(swappoint(m))
    return retrn

def assertrange(alist):
    retrn=[]
    for m in alist:
        if not (m.x > -74.0 and m.x < -73.0): print("X " + str(m.x))
        assert m.x > -74.0 and m.x < -73.0, "x side"
        if not (m.y > 40.0 and m.y < 41.0): print("Y " + str(m.y))
        assert m.y > 40.0 and m.y < 41.0, "y side"

    return retrn



# Assume you have:
# building_polygon: a shapely Polygon representing the building base
# building_height: a number representing the building's height
# point_to_check: a shapely Point representing the location to check
# sun_altitude: the sun's altitude angle (in radians)
# sun_azimuth: the sun's azimuth angle (in radians)

# Function to calculate shadow point for a given vertex
def calculate_shadow_point(vertex, height, altitude, azimuth):
##    Deb("Az " + str(azimuth))
    x, y = vertex.x, vertex.y
    if math.tan(altitude) == 0:  # Sun is at the horizon
        return None  # Shadow is infinitely long
    shadow_offset_x = -height * math.sin(azimuth) / math.tan(altitude)
    shadow_offset_y = -height * math.cos(azimuth) / math.tan(altitude)
    return Point(x + shadow_offset_x, y + shadow_offset_y)






def trypoint2( pointlat,pointlon,namer):
    global gdf1
    global counter
    date=datetime.now(timezone.utc)
##    pos=get_position(date, pointlon, pointlat)
# {pos['azimuth']: -0.8619668996997687, pos['altitude']: 0.5586446727994595}
##    sun_altitude = pos['altitude']
##    sun_azimuth = pos['azimuth']
    sun_altitude = 10.84;
    sun_azimuth =  154.084271;

##data frame w point we care about    
#    newdf=pd.DataFrame({'longitude': [pointlon], 'latitude': [pointlat]})
##convert df to geo df
#    point_to_check = gpd.GeoDataFrame(newdf,geometry=gpd.points_from_xy(newdf.longitude, newdf.latitude, crs="WGS84"))

    point_to_check = Point(pointlon, pointlat)
    assert point_to_check.y < 41


    for k in range(len(gdf1)):
        print("Building " + str(gdf1['building_id'].iloc[k]))
        
        building_polygon = gdf1['geometry'].iloc[k]
        # Calculate shadow points for each vertex of the building's base
        shadow_vertices = []
        building_height=gdf1['height'].iloc[k]
        np=0                    # # of points
        nv=0                    # of verticies
        for vertex in building_polygon.exterior.coords:
            np=1+np
            print("Jelly " +str(np)+"   "+str(vertex))
            shadow_point = calculate_shadow_point(Point(vertex), building_height, sun_altitude, sun_azimuth)
            if shadow_point:
                nv=1+nv
                Deb("NV now " + str(nv))
                shadow_vertices.append(shadow_point)

                assertrange(shadow_vertices)

#        Deb("Points " + str(np) + " Verts " + str(nv))

        # Create the shadow polygon (handle wall shadows if necessary)
        # This part might require more complex geometry operations depending on the building's shape
        # For a simple rectangular building, the shadow polygon can be formed by connecting the shadow vertices
        if nv==10:
          Deb("BamBam v")
          print(type(shadow_vertices))


        fname="/tmp/bam"+str(nv)+".json"
        fshade="/tmp/shade"+str(nv)+".json"
        fw="/tmp/weas"+str(nv)+".json"

        # Create the shadow polygon
        shadow_polygon = Polygon(shadow_vertices)
        shady=Polygon(swaplist(shadow_vertices))

        if nv==10:
          Deb("BamBam")
          print(shadow_polygon)

          ###          shadow_polygon = shadow_polygon.apply(lambda point: shapely.ops.transform(lambda x, y: (y, x), point))


###BUG
###
###shadow_vertices is a set of points
###and when it becomes a polygon it
### is no longer in long/lat



        amydf=pd.DataFrame([shadow_polygon])
        shadyamydf=pd.DataFrame([shady])
        bambam=gpd.GeoDataFrame(geometry=[shadow_polygon], crs="WGS84")
        shadybambam=gpd.GeoDataFrame(geometry=[shady], crs="WGS84")
        Deb("Shady there?")
        assert point_to_check.y < 41
        is_in_shadow = point_to_check.within(shady)
        print(f"Is the point in the shady  shadow? {is_in_shadow}")

        is_in_shadow = point_to_check.within(shadybambam)
        print(f"Is the point in the shady bambam  shadow? {is_in_shadow}")
        


        bambam.to_file(fname)
        shadybambam.to_file(fshade)
#        with open(fname, "w") as f: # Open file in write mode
#          bambam.dump(shadow_polygon,f,indent=4)

        # Check if the point is inside the shadow polygon
#        Deb("point "+str(type(point_to_check)))
        is_in_shadow = shadow_polygon.contains(point_to_check)

        print(f"Is the point in the shadow? {is_in_shadow}")


        is_in_shadow = point_to_check.within(shadow_polygon)

        print(f"Is the point in the w  shadow? {is_in_shadow}")

#        print(shadow_polygon)

#        gdfpoly=gpd.GeoDataFrame(shadow_polygon,crs="EPSG:4326")
#        gdfpoly.to_file("/tmp/file_whole3.json",driver='GeoJSON')
        heknows.append(shadow_polygon)
#        heknows.to_file("/tmp/he" + str(counter) + ".json")
#        heknows.json_dumps("/tmp/he" + str(counter) + ".json")


##24Jun        trymap(shadow_polygon,counter)
        print("Betty " + str(counter))
        counter=counter+1


#try2()

trypoint2( 40.75624,-73.97159, "randolphfrontdoor")
