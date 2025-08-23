import sys
import os
import pandas as pd

import geopandas as gpd            
import numpy as np

from pybdshadow import *
#import analysis
#from analysis import cal_sunshine
from analysis import *

import matplotlib.pyplot as plt

from shapely  import wkt
from shapely.wkt  import loads
from shapely.geometry  import Polygon,mapping


import json


# in Jupyter this lets us show the figures, but not interactively
##%matplotlib inline

from shapely.geometry import Point, LineString, Polygon
##https://iamdonovan.github.io/teaching/egm722/practicals/vector.html

## the one I used for SPA on gbrmail is avialble as py module
## https://github.com/s-bear/sun-position

#https://www.fs.usda.gov/nac/buffers/guidelines/5_protection/6.html#:~:text=Use%20the%20formula%20s%20%3D%20h,shadow%20direction%20on%20the%20ground.

heknows = []
counter=0


'''
Use the formula s = h/tan A to calculate shadow length. See the table below for an example. Sun angle calculators are available on the Web which will provide the sun angle (A) and azimuth angle for a given location based on the date and time.



'''


def Deb(msg=""):
  print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}",flush=True)
  sys.stdout.flush()


global icount
icount=0

debug=0


def LINE():
    return "Line: " +  str(sys._getframe(1).f_lineno) + "  "



###NEEDS A FIX TO not use now when a value was given in command line
### so this can be tested at night


def gettime(anarg):
    print( len(sys.argv))

    if anarg == 'now':
        return datetime.now(timezone.utc)

###only drop down here if now wasn't passed as arg
###in the hope that it would be in argv

    if len(sys.argv) > 1:
        return pd.to_datetime(sys.argv[1],format='mixed').tz_localize('America/New_York').tz_convert('UTC')
    else:
      print('die')
      exit()

#        return pd.to_datetime(anarg,format='%Y-%m-%d').tz_localize('America/New_York').tz_convert('UTC')
#    date=pd.to_datetime(anarg,format='%Y-%m-%d').tz_localize('America/New_York').tz_convert('UTC')

##arg1 is the geometry
def convert_multipolygon(gdf9):
    gdf_approx = gpd.GeoDataFrame({'id': [1], 'geometry': [gdf9]}, crs="WGS84")

    # Calculate the convex hull and assign it back to a new GeoDataFrame or replace the geometry
    convex_hull_gs = gdf_approx.geometry.convex_hull
    # To put it into a GeoDataFrame, you can create a new one or update an existing one
    gdf_convex_hull = gpd.GeoDataFrame(gdf_approx.drop(columns=['geometry']), geometry=convex_hull_gs, crs=gdf_approx.crs)
    
    return gdf_convex_hull.iloc[0,1]













pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


#######################READ THE FILE#######################

df = pd.read_csv("path1.csv")
#df = pd.read_json("pathmn.json")
df['geometry'] = df['geometry'].apply(loads)
gdf1 = gpd.GeoDataFrame(df, crs="wgs84")  # Replace "your_crs"

gdf1.to_file("/tmp/file_whole2.json",driver='GeoJSON')


#barney=gdf1.to_json(to_wgs84=True,orient='table')
#filename="/tmp/file_whole2.json"
#with open(filename, "w") as f: # Open file in write mode
#    f.write(barney+"\n") # Write data to file    



##https://stackoverflow.com/questions/56709561/how-to-smartly-loop-over-all-points-in-a-geodataframe-and-look-at-nearest-neig
##df=pd.DataFrame({'points':points,'values':values})
##gdf=gp.GeoDataFrame(df,geometry=[loads(x) for x in df.points], crs={'init': 'epsg:' + str(25832)})


#######################MULTI TO POLYGON#######################

#print(gdf1.geometry.data_type)

gdf1['geometry'] = gdf1['geometry'].apply(convert_multipolygon)





#print(LINE(), " First geom ",    gdf1['geometry'])
#print("And the columns ")

## late 13jun   gdf=gpd.GeoDataFrame(gdf1)

#print("23656")
#print(LINE(),gdf1," ==== ",type(gdf1))





def tryjson():
    fred=gdf1.to_json(to_wgs84=True)

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
    Deb('bambam')
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



def tryreport():

###this crashes in bdshad.... below
#    buildingshadow = building.copy()
#    a = buildingshadow['geometry'].apply(lambda r: list(r.exterior.coords))


    print(LINE(),"teal")
    gdf1.head()
    wilma=gdf1.to_json(to_wgs84=True)

    print(LINE(),wilma)


    date=pd.to_datetime('now',format='%Y-%m-%d').tz_localize('America/New_York').tz_convert('UTC')
    print('cal sunshine')
    mymy = cal_sunshine(gdf1,day=date)
#    print(mymy)
# 

 #   #Given UTC datetime
#    date = pd.to_datetime('2022-01-01 3:45:33.959797119')\
#        .tz_localize('Asia/Shanghai')\
#        .tz_convert('UTC')
    date=pd.to_datetime('now').tz_localize('America/New_York').tz_convert('UTC')

#Calculate building shadow for sun light


#    print('shadows')
#pybdshadow.
#    shadows = bdshadow_sunlight(gdf1,date)
#    shadows


    ax=plt.subplot(111)
    # plot buildings
    gdf1.plot(ax=ax)

    plt.show()


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



def trypoint( pointlat,pointlon,namer):
    global icount

    # above   pointlon,pointlat,
    print("-" * 30,"trypoint ",namer)

    print(f"lat: {pointlat}, long: {pointlon} name: {namer}")


############SANITY  is the point inside any bldg?

##data frame w point we care about    
    newdf=pd.DataFrame({'longitude': [pointlon], 'latitude': [pointlat]})
##convert df to geo df
    geometryp = gpd.GeoDataFrame(newdf,geometry=gpd.points_from_xy(newdf.longitude, newdf.latitude, crs="WGS84"))


#    for k in range(len(gdf1)):
#      poly = Polygon(gdf1.iloc[k].geometry)
#      a=poly.contains(geometryp)
#      if a.any():
#          print("Point ",geometryp, " in bldg ",gdf1.iloc[k])

    for item in gdf1['geometry']:
        newgds=gpd.GeoSeries(item, crs="WGS84")
        a=newgds.contains(geometryp)
        if a.any():
            print(geometryp," in bldg ", item)

        a=geometryp.within(newgds)
        if a.any():
            print(geometryp," in w bldg ", item)
        



############check if point is inside a shadow from each bldg


    pointheight = 5;
    shadows = bdshadow_pointlight(gdf1,pointlon,pointlat,pointheight)
    if debug > 2:
        print("-" * 30)

        print(LINE(),"  shadows")
        print(shadows)
        print(type(shadows))
        print("-" * 30)

    result = list(shadows['geometry'].iloc[0].exterior.coords)

    if debug > 2:
        print(LINE(),"result")
        print(result)

##data frame w point we care about    
    newdf=pd.DataFrame({'longitude': [pointlon], 'latitude': [pointlat]})
##convert df to geo df
    geometryp = gpd.GeoDataFrame(newdf,geometry=gpd.points_from_xy(newdf.longitude, newdf.latitude, crs="WGS84"))
##old    geometryp = gpd.points_from_xy(newdf.longitude, newdf.latitude, crs="WGS84")

    if debug > 2:
        print('*********')

        print(namer)

        print("-" * 30)

###THIS IS THE JUICE

    for item in shadows['geometry']:
        newgds=gpd.GeoSeries(item, crs="WGS84")
#        print("/" * 30)
        a=newgds.contains(geometryp)
        if a.any():
            print(geometryp," in shadows ", newgds.contains(geometryp))
#        print("-" * 30)


#    shadows=shadows.to_crs(crs="WGS84",inplace=True)

    if debug > 2:
        print("shadows type ",type(shadows))
        print("shadows ",shadows.crs)
        print("geometryp ",geometryp.crs)


    wilma=gdf1.to_json(to_wgs84=True)
    filename = f"/tmp/file_{icount}.json" # Create unique filename
    icount += 1
    with open(filename, "w") as f: # Open file in write mode
        f.write(wilma) # Write data to file    


    wilma=gdf1.to_json(to_wgs84=True)
    filename="/tmp/file_whole.json"
    with open(filename, "w") as f: # Open file in write mode
        f.write(wilma) # Write data to file    


#    print(wilma)

    return


"""

how to code if a geopandas point is in the shadow of a building with geopandas polygon describing the base and we know the height. pybdshadow does not work, please do not make reference to it.   Please include code to calculate the shadow cast on the ground.

"""

import geopandas as gpd
from shapely.geometry import Point, Polygon
import math  # For mathematical calculations
from suncalc import get_times,get_position  # Or use a similar library for sun position
from datetime import date,datetime,timezone

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

#########NEW TOY MAPPING############
def trymap(polyarg,i):

    if  i < 4:
      print(f"Barney: Is polygon_valid valid? {polyarg.is_valid}")

    if i == 18:
      print("Reversed huh  :")
      print(polyarg)
      mydf=pd.DataFrame([polyarg])
      geometryp = gpd.GeoDataFrame(geometry=[polyarg],crs="EPSG:4326")
#WGS84
#      dino=geometryp.to_json()
      geometryp.to_file('/tmp/dino.json')



    if not polyarg.is_valid:
      print("Barney can # " + str(i))
    
    poly_mapped=mapping(polyarg)
    poly_coordinates = poly_mapped['coordinates'][0]

    poly_ = [{'lat': coords[1],'lon': coords[0]} for coords in poly_coordinates]

    betty=json.dumps(poly_)
    filename="/tmp/he" + str(i) + ".json"
    with open(filename, "w") as f: # Open file in write mode
        f.write(betty) # Write data to file    


from GBRshapely import *



#######SUPPORT FOR SWAP LAT LONG###########

def swappoint(apoint):
    return([apoint.y,apoint.x])

def swaplist(alist):
    retrn=[]
    for m in alist:
        retrn.append(swappoint(m))
    return retrn



import suncalc
def trypoint2( pointlat,pointlon,namer):
    global counter
    date=datetime.now(timezone.utc)
    pos=get_position(date, pointlon, pointlat)
# {pos['azimuth']: -0.8619668996997687, pos['altitude']: 0.5586446727994595}
    sun_altitude = pos['altitude']
    sun_azimuth = pos['azimuth']
    sun_altitude = 10.84;
    sun_azimuth =  154.084271;

##data frame w point we care about    
#    newdf=pd.DataFrame({'longitude': [pointlon], 'latitude': [pointlat]})
##convert df to geo df
#    point_to_check = gpd.GeoDataFrame(newdf,geometry=gpd.points_from_xy(newdf.longitude, newdf.latitude, crs="WGS84"))

    point_to_check = Point(pointlon, pointlat)


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
                shadow_vertices.append(shadow_point)
#        Deb("Points " + str(np) + " Verts " + str(nv))

        # Create the shadow polygon (handle wall shadows if necessary)
        # This part might require more complex geometry operations depending on the building's shape
        # For a simple rectangular building, the shadow polygon can be formed by connecting the shadow vertices
        if nv==10:
          Deb("BamBam v")
          print(type(shadow_vertices))

          newv=[]

          for mitem in shadow_vertices:
            newv.append([mitem.y,mitem.x])
#            print(type(mitem))

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









###the file read run first, without and calls to subroutines

#tryreport()


#trypoint2( 40.755515,-73.971029,  "mcds")
#trypoint2( 40.756133,-73.970579,  "real mcds")
#trypoint2( 40.756751,-73.970085, "jpmwealth")
#trypoint2( 40.756015,-73.970487, "essAbagel")
#trypoint2( 40.75629,-73.97025, "essDoor")
#trypoint2( 40.75612,-73.97147, "randolph")
trypoint2( 40.75624,-73.97159, "randolphfrontdoor")
#trypoint2( 40.756684,-73.97130, "51st")






###https://people.csail.mit.edu/ericchan/bib/pdf/p275-atherton.pdf
##doesnt take sun into account
##
##have pysolar in Downloads

## https://data.cityofnewyork.us/City-Government/BUILDING/5zhs-2jue/about_data
## SHAPE_AREA  Measures the enclosed area within a polygon.
## 
print(heknows)

#gdfpoly=gpd.GeoDataFrame(heknows, geometry=0,crs="EPSG:4326")
gdfpoly=gpd.GeoDataFrame(heknows, geometry=0,crs="WGS84")
gdfpoly.to_file("/tmp/file_whole5.json")
#,driver='GeoJSON',crs="WGS84")
exit()
betty=gdfpoly.to_json(to_wgs84=True)
with open("/tmp/file_whol3.shp", "w") as f: # Open file in write mode
  f.write(betty) # Write data to file    

##  KML, GPX, CSV, GTFS,




"""

with a polygon describing the footprint of a building, and having the height of the building, and the altitude and azimuth of the sun, how do I produce a polygon of long/lat describing the shadow? Is there "OPEN SOURCE SOFTWARE" library routine that does this?
"""
