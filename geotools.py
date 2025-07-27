import sys
import os
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
import math
import subprocess
from geographiclib.geodesic import Geodesic


"""



print("spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu)

result = subprocess.run(
    "spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu,
    capture_output=True,
    text=True,
    shell=True,
    check=True,
)
aresult = result.stdout


(sun_azimuth1, sun_altitude1) = aresult.split()
sun_azimuth = float(sun_azimuth1) + 0.0
sun_altitude = float(sun_altitude1) + 0.0
# sun_azimuth = 144.71 # degrees (South-West)
# sun_altitude = 13.48 # degrees
sunposition={ "azimuth" :sun_azimuth,"altitude" :sun_altitude}

"""


"""
new wway to compute az

https://geographiclib.sourceforge.io/Python/doc/examples.html?highlight=azimuth


"""




def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugGT {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()







"""!
@callergraph



@callgraph
"""
def calculate_azimuth(ax, ay, bx, by):
    """Computes the bearing in degrees from the point A(ax,ay) to the point B(bx,by)."""
    a=Geodesic.WGS84.Inverse(ay,  ax,  by,  bx, outmask=1929)
    prelim=a['azi1']
#    if prelim < 0:
#        prelim=360+prelim

    return prelim

    TWO_PI = math.pi * 2
    theta = math.atan2(bx - ax, ay - by)
    if theta < 0.0:
        theta += TWO_PI
    return math.degrees(theta)


##is   abs(a) - abs(b) < c
def closeto(a,b,c):
    Deb(f" {abs(a)}  {abs(b)}  {c}  { abs(abs(a) - abs(b)) < c }")
    if   abs(abs(a) - abs(b)) < c :
        return 1
    else:
        return 0



def calculate_azimuth_line(aline):
    if not isinstance(aline,LineString):
        raise  TypeError("supply LineString instead")
    first_point = Point(aline.coords[0])
    last_point = Point(aline.coords[-1]) # Or line.coords[1] for a simple two-point line

    # Calculate azimuth
#    return calculate_azimuth(first_point.x, first_point.y, last_point.x, last_point.y)
    return calculate_azimuth(first_point.x, first_point.y, last_point.x, last_point.y)
    


def get_az_el(central_lon, central_lat):
    zulu = ""
    if len(sys.argv) > 1:
        zulu = sys.argv[1]

    print("spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu)

    result = subprocess.run(
        "spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu,
        capture_output=True,
        text=True,
        shell=True,
        check=True,
    )
    aresult = result.stdout


    (sun_azimuth1, sun_altitude1) = aresult.split()
    sun_azimuth = float(sun_azimuth1) + 0.0
    sun_altitude = float(sun_altitude1) + 0.0
    # sun_azimuth = 144.71 # degrees (South-West)
    # sun_altitude = 13.48 # degrees
    sunposition={ "azimuth" :sun_azimuth,"altitude" :sun_altitude}

    print(sunposition)
    return sunposition


def elucidate(atype):
    Deb(atype.geom_type)
    Deb(atype.geom_type.unique)
    

# Function to extract wall segments as (long, lat) tuples
def extract_wall_coords(geometry):
#    Deb('extract_wall_coords')
#    Deb(geometry.geom_type)
    walls = []
    if geometry.geom_type == 'LineString':
        coords = list(geometry.coords)
        for i in range(len(coords) - 1):
            walls.append((coords[i], coords[i+1]))
    elif geometry.geom_type == 'MultiLineString':
        for line in geometry.geoms:
            coords = list(line.coords)
            for i in range(len(coords) - 1):
                walls.append((coords[i], coords[i+1]))
    return walls


import math

def calculate_azimuthengine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    azimuth = 90 - math.degrees(math.atan2(dy, dx))
    
    # Ensure the azimuth is between 0 and 360 degrees
    if azimuth < 0:
        azimuth += 360
    return azimuth


def calculate_azimuth_gdf(gdf):
    gdf['azimuth'] = gdf.apply(lambda row: calculate_azimuthengine(row['geometry'].coords[0][0],
                                                             row['geometry'].coords[0][1],
                                                             row['geometry'].coords[1][0],
                                                             row['geometry'].coords[1][1]), axis=1)
    return gdf['azimuth'].iloc[0]
