import os,sys
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.affinity import translate
from shapely.wkt import loads
import pyproj
import math
import geopandas as gpd            
import subprocess
import numpy as np






mylist2d0=[
[ 40.755515,-73.971029,  "mcds"],
[ 40.756133,-73.970579,  "real mcds"],
[ 40.756751,-73.970085, "jpmwealth"],
[ 40.756015,-73.970487, "essAbagel"],
[ 40.75629,-73.97025, "essDoor"],
[ 40.75612,-73.97147, "randolph"],
[ 40.75624,-73.97159, "randolphfrontdoor"],
[ 40.756684,-73.97130, "51st"], ]

mylist2d=[[ 40.75624,-73.97159, "randolphfrontdoor"]]


places_to_check=np.array(mylist2d)              # look for shadows in these locations

## function for debugging
#
# more details
#
def Deb(msg=""):
  print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}",flush=True)
  sys.stdout.flush()



## Function to extract coordinates from the MultiPolygon
#
def to_coords(multipolygon):
    """
    Extracts coordinates from a MultiPolygon object, including holes.

    Args:
        multipolygon: A Shapely MultiPolygon object.

    Returns:
        A list of coordinate tuples.
    """
    coords_list = []
    for polygon in multipolygon.geoms:
        coords_list.extend(list(polygon.exterior.coords[:-1]))
        for interior in polygon.interiors:
            coords_list.extend(list(interior.coords[:-1]))
    return coords_list


## unused
#
def convert_multipolygon(gdf9):
    gdf_approx = gpd.GeoDataFrame({'id': [1], 'geometry': [gdf9]}, crs="EPSG:3857")

    # Calculate the convex hull and assign it back to a new GeoDataFrame or replace the geometry
    convex_hull_gs = gdf_approx.geometry.convex_hull
    # To put it into a GeoDataFrame, you can create a new one or update an existing one
    gdf_convex_hull = gpd.GeoDataFrame(gdf_approx.drop(columns=['geometry']), geometry=convex_hull_gs, crs=gdf_approx.crs)
    
    return gdf_convex_hull.iloc[0,1]




## calc shadow
# 
def calculate_building_shadow(building_polygon_lat_lon, building_height_meters, sun_azimuth_deg, sun_altitude_deg, central_lat, central_lon):
    """
    Calculates the shadow polygon of a building.

    Args:
        building_polygon_lat_lon (list of tuples): List of (longitude, latitude) tuples
                                                   defining the building base.
        building_height_meters (float): Height of the building in meters.
        sun_azimuth_deg (float): Sun's azimuth angle in degrees (0 = North, 90 = East, etc.).
        sun_altitude_deg (float): Sun's altitude angle in degrees (0 = horizon, 90 = zenith).
        central_lat (float): Latitude of a central point for local projection.
        central_lon (float): Longitude of a central point for local projection.

    Returns:
        shapely.geometry.Polygon or MultiPolygon: The shadow polygon in (longitude, latitude) coordinates.
                                                  Returns None if sun altitude is <= 0.
    """
    if sun_altitude_deg <= 0:
        return None # No shadow cast if sun is at or below horizon

    # 1. Define the CRS objects for input (WGS84) and output (local projected)
    # Using EPSG:4326 for WGS84 (lat/lon)
    # For a local projection, we can define a custom one or find a suitable UTM zone.
    # For a small area, a custom Transverse Mercator centered on your building is good.
    # PROJ string for a local Transverse Mercator:
    # +proj=tmerc +lat_0={central_lat} +lon_0={central_lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs
    # k=1 ensures scale is 1 at the central meridian, useful for localized accurate distances.
    # We set x_0 and y_0 to 0 so our local origin is at (central_lon, central_lat)
    
##GBR
    crs_wgs84 = pyproj.CRS("EPSG:4326")
##    crs_wgs84 = pyproj.CRS("CRS84")
    
    # Define a custom local projection CRS
## was ellps=WGS84
##changing proj from tmerc to cea


    local_proj_string = (
        f"+proj=tmerc +lat_0={central_lat} +lon_0={central_lon} "
        "+k=1.0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
    )
    crs_local = pyproj.CRS(local_proj_string)

    # Create transformers for forward and inverse transformations
    transformer_to_local = pyproj.Transformer.from_crs(crs_wgs84, crs_local, always_xy=True)
    transformer_to_lonlat = pyproj.Transformer.from_crs(crs_local, crs_wgs84, always_xy=True)

    # Convert building base from lat/lon to local meters
    building_base_local_coords = []
    for lon, lat in building_polygon_lat_lon:
        x, y = transformer_to_local.transform(lon, lat)
        building_base_local_coords.append((x, y))
    building_base_polygon_local = Polygon(building_base_local_coords)

    # 2. Calculate shadow length and direction vector components
    sun_altitude_rad = math.radians(sun_altitude_deg)
    sun_azimuth_rad = math.radians(sun_azimuth_deg)

    # Shadow length on flat ground
    shadow_length = building_height_meters / math.tan(sun_altitude_rad)

    # Horizontal displacement components for the shadow
    # Azimuth is clockwise from North. Shadow is cast in the opposite direction.
    # dx is change in Easting, dy is change in Northing
    # Sine for Easting, Cosine for Northing for azimuth from North.
    # Negative because shadow goes AWAY from the sun's direction.
    dx = -shadow_length * math.sin(sun_azimuth_rad)
    dy = -shadow_length * math.cos(sun_azimuth_rad)

    # 3. Project the building's top outline to get the shadow
    # For a simple polygon, we can translate the base polygon directly.
    shadow_polygon_local = translate(building_base_polygon_local, xoff=dx, yoff=dy)

    # 4. Convert shadow polygon back to lat/lon
    shadow_lonlat_coords = []
    if isinstance(shadow_polygon_local, Polygon):
        # Shapely's .exterior.coords gives (x,y) tuples
        for x, y in shadow_polygon_local.exterior.coords:
            lon, lat = transformer_to_lonlat.transform(x, y)
            shadow_lonlat_coords.append((lon, lat))
        return Polygon(shadow_lonlat_coords)
    elif isinstance(shadow_polygon_local, MultiPolygon):
        # Handle multipolygon case
        transformed_geoms = []
        for poly in shadow_polygon_local.geoms:
            poly_lonlat_coords = []
            for x, y in poly.exterior.coords:
                lon, lat = transformer_to_lonlat.transform(x, y)
                poly_lonlat_coords.append((lon, lat))
            transformed_geoms.append(Polygon(poly_lonlat_coords))
        return MultiPolygon(transformed_geoms)
    else:
        return None

# Example Usage:
# A simplified rectangular building in New York City (approximate lat/lon)
building_base_coords = [
    (-73.941090280601,40.6811977436),
    (-73.941076174979,40.681127825828),
    (-73.941064881785,40.681071851261),
    (-73.941059696277,40.681046145217),
    (-73.941110723935,40.681040178418),
    (-73.941107748996,40.681025436372),
    (-73.941130955961,40.681022723289),
    (-73.941133668267,40.681036168459),
    (-73.94116451421,40.681189063698),
    (-73.941153631141,40.681197719283),
    (-73.941132562991,40.681200183121),
    (-73.941121882725,40.681196173068),
    (-73.941117566631,40.681194552635),
    (-73.941090280601,40.6811977436) 
]
building_height = 45.0  # meters

# Central point for local projection (can be average of building coords)
central_lat = 40.75643
central_lon = -73.97206
point_to_check = Point(central_lon,central_lat)

# Sun position (example: afternoon sun, southwest direction)

#Possible time to pass to spa2py
zulu=""
if len(sys.argv) > 1:
    zulu=sys.argv[1]

print("spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu)

result = subprocess.run("spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu, capture_output=True, text=True, shell=True, check=True)
aresult=result.stdout


(sun_azimuth1,sun_altitude1) = aresult.split()
sun_azimuth=float(sun_azimuth1)+0.0
sun_altitude=float(sun_altitude1)+0.0
#sun_azimuth = 144.71 # degrees (South-West)
#sun_altitude = 13.48 # degrees


#####@MAINPAGE
"""
for each bldg
   take their multip
   convert it to tuples w to_coords
         GOES WRONG HERE
         gpd from the coords no match for input


   use this and a point to predict a shadow





"""


import pandas as pd
"""!
@page page1 MainLoop Start here


read in each line of the buildings file path1.csv

set up geometry and create the GeoDataFrame

for row is only going to iterate over 1 bldg

each bldg should have a json file starting w /tmp/bldg
with its dataframe





"""


for fake in range(1,8):
    df = []
    df = pd.read_csv("/Src/sun/path1.csv",sep=',',skiprows=lambda x: x != 0 and x != fake)
    Deb("Fake " + str(fake))

    df['geometry'] = df['geometry'].apply(loads)

    gdf1 = gpd.GeoDataFrame(df, crs="WGS84")  # Replace "your_crs"



    k=0
    m=0
    for row in df.itertuples(index=False):



        Deb('Bldg ' + str(row[5]) + " " + str(row[1])+"  "+str(fake))


        geoval=gdf1.geometry.is_valid
        assert geoval.all()

        bname="/tmp/bldg"+str(m)+".json"
        pebbles=gdf1.to_json(to_wgs84=False   )  #True)  #  crs="WGS84"
        if not pebbles: asd=4/0
        Deb("Writing peb "+bname)
        with open(bname,"w") as w:
            w.write(pebbles)
            w.close()

####shadow_banished goes here

    ##    assert apoly.is_valid

        """!
        @page page2 MainLoop continue

        code to compute shadow needs the multipoly
        broken into tuples of long/lat, hopefully
        done by to_coords

        GeoFrame made of result and some are tested
        by eye

        Some come back as not valid structures and
        are skipped

        Passing ones written to JSON as /tmp/fromtuple...

        CRS changed to WGS84 in case they were not before

        centroid calculated as input to shadow calc

        shadow_polygon is result of calc

        """

        list1=to_coords(row[0])
        #        Deb(list1)

        if k>=0:
          #            Deb(row[0])
            dshit=gpd.GeoDataFrame(geometry=[Polygon(list1)], crs="WGS84")
            geoval=dshit.geometry.is_valid
            #            assert geoval.all()     # other choice .all()
            if not  geoval.all() :
              Deb("Skipping tuple "+ str(k)) #   row(5))
              next


            barney=dshit.to_json(to_wgs84=False)  #=True)  #  crs="WGS84"
            Deb("Writing barney "+"/tmp/fromtuple"+str(k)+".json")
            with open("/tmp/fromtuple"+str(k)+".json","w") as w1:
              w1.write(barney)
              w1.close()
              
            dshit.to_crs("WGS84")

###PROJECTION
##https://gis.stackexchange.com/questions/372564/userwarning-when-trying-to-get-centroid-from-a-polygon-geopandas
            dshit.to_crs('+proj=cea').centroid.to_crs(dshit.crs)

##ORIG            dshit["centroid"]=dshit["geometry"].centroid

            dshit["centroid"]= dshit.to_crs('+proj=cea').centroid.to_crs(dshit.crs)



        shadow_polygon = calculate_building_shadow(
          list1,
          row[11],
          sun_azimuth,
          sun_altitude,
          dshit["centroid"].y,
          dshit["centroid"].x
          #        central_lat,
          #        central_lon
        )

        if not shadow_polygon:
          print("Skipping "+row(5))
          next


        if shadow_polygon:
          if not shadow_polygon.is_valid:
            Deb(k)
            Deb(row[1])
            Deb(row[5])
            Deb(shadow_polygon)

        if shadow_polygon:
          pass
        #      assert shadow_polygon.is_valid


#needed?        if shadow_polygon:



##EPSG:4326
          #        print("Shadow Polygon (Long/Lat):")
          #        if isinstance(shadow_polygon, Polygon):
          #            print(list(shadow_polygon.exterior.coords))
          #        elif isinstance(shadow_polygon, MultiPolygon):
          #            for i, poly in enumerate(shadow_polygon.geoms):
          #                print(f"APolygon {i+1}: {list(poly.exterior.coords)}")
          #        bambam=gpd.GeoDataFrame(geometry=[shadow_polygon], crs="WGS84")
          #        bambam.to_file("/tmp/bambam.json")

        frname="/tmp/shadow"+str(fake)+".json"
        bambam=gpd.GeoDataFrame(geometry=[shadow_polygon], crs="WGS84")
        geoval=bambam.geometry.is_valid
        #                assert geoval.all()     # other choice .all()
        if not geoval.all():
          Deb("Skipping shadow " + str(k))

        dino=bambam.to_json(to_wgs84=False) #True)
        Deb("Writing " + frname)
        with open(frname,"w") as w2:
          w2.write(dino)
          w2.close()

#              bambam.to_file(frname,crs="WGS84")
        m=m+1
        print("Datar\t"+str(row[5])+"\t"+frname)




        """!
        @page page3 check each shadow target
        against each building
        for now each shadow is written as json
        to /tmp/shadow..
        In future it should only be for
        shadows that have a target in them

        NB that Point takes lat/long

        /tmp/bimbo... is file with point




        """

        for (mylong,mylat,myname) in places_to_check:
          ### write shadow file for randolph

#            if myname == "randolphfrontdoor" and row[1]=="Randolph":


###################################

###was randolph if

##################################




            point_to_check = Point(mylat,mylong)  ###GBR check this
            bimbo = gpd.GeoDataFrame(geometry=[point_to_check], crs="WGS84")
            dino=bimbo.to_file("/tmp/bimbo.json",driver="GeoJSON")

            if shadow_polygon.contains(point_to_check): print("In shadow bldg " + str(row[5]) + " " + myname)
            #        if k == 0:
            #            combo = shadow_polygon
            #        else:
            #            combo = gpd.GeoDataFrame(pd.concat([combo,shadow_polygon], ignore_index=True))
            #https://geopandas.org/en/stable/docs/user_guide/mergingdata.html


    k=k+1
    m=m+1

"""
I am trying to find a solution in a well-respected library, not something de novo.   I am trying to convert a multipolygon to a set of polygons to use as input to library routines.  What I keep finding as solutions iterating through geoms/exterior/coords and then through interiors.  When I visualize the multipolygon and the resulting polygons in ArcGIS they are kilometers apart.  Is there an open source solution I am not finding?


"""



"""

def calculate_building_shadow(building_polygon_lat_lon, building_height_meters, sun_azimuth_deg, sun_altitude_deg, central_lat, central_lon):

"""

"""@package docstring
see page 43 (paper 26) of doxygen manual
 then p 296  paper 278

"""



"""@bug
why does long/lat for 135 e 50th show up in arcgis & geojson in BK?

CRS.from_wkt('PROJCS["NAD_1983_StatePlane_New_York_Long_Island_FIPS_3104_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["latitude_of_origin",40.1666666666667],PARAMETER["central_meridian",-74],PARAMETER["standard_parallel_1",40.6666666666667],PARAMETER["standard_parallel_2",41.0333333333333],PARAMETER["false_easting",984250],PARAMETER["false_northing",0],UNIT["Foot_US",0.304800609601219],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","2263"]]')
"""
