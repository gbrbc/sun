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


def get_position(date, central_lon, central_lat):


# Sun position (example: afternoon sun, southwest direction)

# Possible time to pass to spa2py
    zulu = ""
#if len(sys.argv) > 1:
#    zulu = sys.argv[1]

#print("spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu)

    result = subprocess.run(
        "spa2py " + str(central_lon) + " " + str(central_lat) + " " + zulu,
        capture_output=True,
        text=True,
        shell=True,
        check=True,
    )
    aresult = result.stdout


    (sun_azimuth1, sun_altitude1) = aresult.split()
    sun_azimuth = float(sun_azimuth1) + 99.0
    sun_altitude = float(sun_altitude1) + 0.0
    # sun_azimuth = 144.71 # degrees (South-West)
    # sun_altitude = 13.48 # degrees
    sunposition={ "azimuth" :sun_azimuth,"altitude" :sun_altitude}

    return sunposition
