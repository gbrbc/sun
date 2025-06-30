import os,sys
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.affinity import translate
from shapely.wkt import loads
import pyproj
import math
import geopandas as gpd            
import subprocess



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
    
    crs_wgs84 = pyproj.CRS("EPSG:4326")
    
    # Define a custom local projection CRS
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

result = subprocess.run("spa2py " + str(central_lon) + " " + str(central_lat), capture_output=True, text=True, shell=True, check=True)
aresult=result.stdout


(sun_azimuth1,sun_altitude1) = aresult.split()
sun_azimuth=float(sun_azimuth1)+0.0
sun_altitude=float(sun_altitude1)+0.0
#sun_azimuth = 144.71 # degrees (South-West)
#sun_altitude = 13.48 # degrees



import pandas as pd

#print(type(building_base_coords[0]))
#print(type(building_base_coords))

df = pd.read_csv("/Src/sun/path1.csv",sep=',')

df['geometry'] = df['geometry'].apply(loads)

gdf1 = gpd.GeoDataFrame(df, crs="wgs84")  # Replace "your_crs"

gdf1['geometry'] = gdf1['geometry'].apply(convert_multipolygon)

Deb(gdf1.iloc[0][0])

#for k in range(len(df)):
#    print("Df ",df.iloc[k][0])
#    print("Gdf1 ",gdf1.iloc[k][0])

k=0

for row in df.itertuples(index=False):
    Deb('Bldg ' + str(row[5]))


    apoly=Polygon(gdf1.iloc[k][0])
    list1=list(apoly.exterior.coords[:-1])
    list2=[]
#    Deb("interiors len " + str(len(apoly.interiors)))
    if len(apoly.interiors) > 0:
        list2=list(apoly.interiors[0].coords[:-1])    
        list1=list1+list2



    shadow_polygon = calculate_building_shadow(
        list1,
        row[11],
        sun_azimuth,
        sun_altitude,
        central_lat,
        central_lon
    )

    if shadow_polygon:
        print("Shadow Polygon (Long/Lat):")
        if isinstance(shadow_polygon, Polygon):
            print(list(shadow_polygon.exterior.coords))
        elif isinstance(shadow_polygon, MultiPolygon):
            for i, poly in enumerate(shadow_polygon.geoms):
                print(f"APolygon {i+1}: {list(poly.exterior.coords)}")
        bambam=gpd.GeoDataFrame(geometry=[shadow_polygon], crs="WGS84")
        bambam.to_file("/tmp/bambam.json")
        if shadow_polygon.contains(point_to_check): print("In shadow bldg " + str(row[5]))
#        if k == 0:
#            combo = shadow_polygon
#        else:
#            combo = gpd.GeoDataFrame(pd.concat([combo,shadow_polygon], ignore_index=True))
#https://geopandas.org/en/stable/docs/user_guide/mergingdata.html

    else:
        print("No shadow cast (sun at or below horizon).")

    k=k+1
