import sys
import os
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.affinity import translate
from shapely.wkt import loads
import pyproj
import math
import geopandas as gpd
import subprocess
import numpy as np
import pandas as pd

from geotools import *

def Deb(msg=""):
    """!
@callergraph

@showrefby

@callgraph
    """

    print(f"DebugGP {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()





def get_position(date, central_lon, central_lat, **kwargs):

    Deb('get_pos')



# Possible time to pass to spa2py
    zulu = ""
    
    for key, value in kwargs.items():
        if key == "time":
            zulu=value
#        print("The value of {} is {}".format(key, value))


# Sun position (example: afternoon sun, southwest direction)
#    if len(sys.argv) > 1:
#       zulu = sys.argv[1]

    Deb(f"spa2py {central_lon:.3f}  {central_lat:.3f} {zulu}")

    result = subprocess.run(
        "spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu,
        capture_output=True,
        text=True,
        shell=True,
        check=True,
    )
    aresult = result.stdout

## Get the first line of output 

    realresult_index = aresult.find('\n')

# If a newline is found, slice the string up to that index

    if realresult_index != -1:
        realresult = aresult[:realresult_index]
    else:
    # If no newline is found, the entire aresult is considered the "first line"
        realresult = aresult


    (sun_azimuth1, sun_altitude1) = realresult.split()
    sun_azimuth = float(sun_azimuth1) + 0.0  # 99.0
    sun_altitude = float(sun_altitude1) + 0.0
    # sun_azimuth = 144.71 # degrees (South-West)
    # sun_altitude = 13.48 # degrees
    sunposition={ "azimuth" :sun_azimuth,"altitude" :sun_altitude}
    Deb(f"sunpos az  {sun_azimuth:.2f} nyc_az {sun_azimuth-29:.2f}   alt {sun_altitude:.2f}")

    if len(zulu) > 0:
        print(aresult)
    
    return sunposition 
