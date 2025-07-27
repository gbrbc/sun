

import warnings
warnings.filterwarnings("error", category=UserWarning)
import sys
import os
import shapely
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from shapely.affinity import translate
from shapely.wkt import loads
import pyproj
import math
import geopandas as gpd
import subprocess
import numpy as np
import pandas as pd
from longerline import *


import geographiclib

from rotateline import *


def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugTL3 {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()






line1 = LineString([( -73.9720600,40.7564525),(-73.9720600, 40.7564075)])
line2 = LineString([( -73.9720499,40.7564512),(-73.9720701, 40.7564088)])
line3 = LineString([( -73.9720410,40.7564472),(-73.9720790, 40.7564128)])
line4 = LineString([( -73.9720344,40.7564413),(-73.9720856, 40.7564187)])
line5 = LineString([( -73.9720308,40.7564339),(-73.9720892, 40.7564261)])
line6 = LineString([( -73.9720308,40.7564261),(-73.9720892, 40.7564339)])
line7 = LineString([( -73.9720344,40.7564187),(-73.9720856, 40.7564413)])
line8 = LineString([( -73.9720410,40.7564128),(-73.9720790, 40.7564472)])
line9 = LineString([( -73.9720499,40.7564088),(-73.9720701, 40.7564512)])
line10 = LineString([( -73.9720600,40.7564075),(-73.9720600, 40.7564525)])
line11 = LineString([( -73.9720701,40.7564088),(-73.9720499, 40.7564512)])
line12 = LineString([( -73.9720790,40.7564128),(-73.9720410, 40.7564472)])
line13 = LineString([( -73.9720856,40.7564187),(-73.9720344, 40.7564413)])
line14 = LineString([( -73.9720892,40.7564261),(-73.9720308, 40.7564339)])
line15 = LineString([( -73.9720892,40.7564339),(-73.9720308, 40.7564261)])
line16 = LineString([( -73.9720856,40.7564413),(-73.9720344, 40.7564187)])
line17 = LineString([( -73.9720790,40.7564472),(-73.9720410, 40.7564128)])
line18 = LineString([( -73.9720701,40.7564512),(-73.9720499, 40.7564088)])
line19 = LineString([( -73.9720600,40.7564525),(-73.9720600, 40.7564075)])



'''
#other direction
line1 = LineString([( -73.9720600,40.7564525),(-73.9720600, 40.7564075)])
line2 = LineString([( -73.9720499,40.7564512),(-73.9720701, 40.7564088)])
line3 = LineString([( -73.9720410,40.7564472),(-73.9720790, 40.7564128)])
line4 = LineString([( -73.9720344,40.7564413),(-73.9720856, 40.7564187)])
line5 = LineString([( -73.9720308,40.7564339),(-73.9720892, 40.7564261)])
line6 = LineString([( -73.9720308,40.7564261),(-73.9720892, 40.7564339)])
line7 = LineString([( -73.9720344,40.7564187),(-73.9720856, 40.7564413)])
line8 = LineString([( -73.9720410,40.7564128),(-73.9720790, 40.7564472)])
line9 = LineString([( -73.9720499,40.7564088),(-73.9720701, 40.7564512)])
line10 = LineString([( -73.9720600,40.7564075),(-73.9720600, 40.7564525)])
line11 = LineString([( -73.9720701,40.7564088),(-73.9720499, 40.7564512)])
line12 = LineString([( -73.9720790,40.7564128),(-73.9720410, 40.7564472)])
line13 = LineString([( -73.9720856,40.7564187),(-73.9720344, 40.7564413)])
line14 = LineString([( -73.9720892,40.7564261),(-73.9720308, 40.7564339)])
line15 = LineString([( -73.9720892,40.7564339),(-73.9720308, 40.7564261)])
line16 = LineString([( -73.9720856,40.7564413),(-73.9720344, 40.7564187)])
line17 = LineString([( -73.9720790,40.7564472),(-73.9720410, 40.7564128)])
line18 = LineString([( -73.9720701,40.7564512),(-73.9720499, 40.7564088)])
line19 = LineString([( -73.9720600,40.7564525),(-73.9720600, 40.7564075)])
'''



listlin=[line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17, line18, line19]

bearing=0
countbaddies=0
compaz=0
for line in listlin:

    print ( '#' * 45)

##how good is compass line?

##line was created by testline2

    qaorig=calculate_azimuth_line(line)

    Deb(f"#manufactured bearing {bearing} vs actual {qaorig:.1f}")

    if 0==closeto(bearing,qaorig,5):
        raise ValueError("bearing diff qaorig >5")



    dshitline = rotateline(LineString(line), 133)

    qa=calculate_azimuth_line(dshitline)
    if qa<131 or qa>135:
        print(f"line off angle {qa:.1f} vs {bearing}")
        countbaddies=countbaddies+1

    dshit4 = gpd.GeoDataFrame(geometry=[dshitline], crs="WGS84")    

####make compass line longer
    compass=lengthen_line(line,0.25)

    dshit5 = gpd.GeoDataFrame(geometry=[compass], crs="WGS84")    
    total=gpd.pd.concat([dshit4, dshit5], ignore_index=True)

    barney = total.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

    with open("/tmp/ts" + str(bearing) +".json", "w") as w1:
        w1.write(barney)
        w1.close()
    
    compaz = compaz + 10
    bearing = bearing + 20
print(f"baddies    {countbaddies}")


## this all comes from
##https://geographiclib.sourceforge.io/Python/doc/code.html#geographiclib.geodesicline.GeodesicLine.Position

anewline=Geodesic.WGS84.Line(40.756015, -73.970487, 35,caps=3979)
print(anewline)

## fails on internal error
##anobj=geographiclib.geodesicline.GeodesicLine(anewline,40.756015, -73.970487, 35,caps=3979)
##print(anobj)
