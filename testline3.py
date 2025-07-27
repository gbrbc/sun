

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
import geopy.distance


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




'''

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
line1 = LineString([( -73.972060000,40.756452513),(-73.972060000, 40.756407487)])
line2 = LineString([( -73.972049874,40.756451155),(-73.972070126, 40.756408845)])
line3 = LineString([( -73.972040970,40.756447246),(-73.972079030, 40.756412754)])
line4 = LineString([( -73.972034361,40.756441256),(-73.972085639, 40.756418744)])
line5 = LineString([( -73.972030844,40.756433909),(-73.972089156, 40.756426091)])
line6 = LineString([( -73.972030844,40.756426091),(-73.972089156, 40.756433909)])
line7 = LineString([( -73.972034361,40.756418744),(-73.972085639, 40.756441256)])
line8 = LineString([( -73.972040970,40.756412754),(-73.972079030, 40.756447246)])
line9 = LineString([( -73.972049874,40.756408845),(-73.972070126, 40.756451155)])
line10 = LineString([( -73.972060000,40.756407487),(-73.972060000, 40.756452513)])
line11 = LineString([( -73.972070126,40.756408845),(-73.972049874, 40.756451155)])
line12 = LineString([( -73.972079030,40.756412754),(-73.972040970, 40.756447246)])
line13 = LineString([( -73.972085639,40.756418744),(-73.972034361, 40.756441256)])
line14 = LineString([( -73.972089156,40.756426091),(-73.972030844, 40.756433909)])
line15 = LineString([( -73.972089156,40.756433909),(-73.972030844, 40.756426091)])
line16 = LineString([( -73.972085639,40.756441256),(-73.972034361, 40.756418744)])
line17 = LineString([( -73.972079030,40.756447246),(-73.972040970, 40.756412754)])
line18 = LineString([( -73.972070126,40.756451155),(-73.972049874, 40.756408845)])
line19 = LineString([( -73.972060000,40.756452513),(-73.972060000, 40.756407487)])





listlin=[line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17, line18, line19]

gpd.options.display_precision = 9
bearing=0
countbaddies=0
compaz=0

#p1=( -73.972060000,40.756452513)
#p2=(-73.972060000, 40.756407487)
#Deb(howlong(p1,p2))
Deb(howlong(geopy.point.Point( -73.972060000,40.756452513),geopy.point.Point(-73.972060000, 40.756407487)))
Deb(howlongline(line1))
assert 5==howlong(( -73.972060000,40.756452513),(-73.972060000, 40.756407487))


for line in listlin:

    print ( '#' * 45)

##how good is compass line?

##line was created by testline2

    fg=howlongline(line)
    if fg != 5:
        print(fg)
        hi=line.coords[0]
        print(hi[0])
        print(line.coords[0])
        print(line.coords[-1])

    assert 5==howlongline(line)

    qaorig=calculate_azimuth_line(line)

    Deb(f"#manufactured bearing {bearing} vs actual {qaorig:.1f}")

    if False==closeaz(bearing,qaorig):
        raise ValueError("bearing diff qaorig >5")



    dshitline = rotateline(LineString(line), 133)

    qa=calculate_azimuth_line(dshitline)
#    if False==closeaz(133,qa):
#        raise ValueError("bearing diff qa >5")

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

    '''


##https://gis.stackexchange.com/questions/126246/convert-lat-lon-into-meters
#    line.transform(3857)
#    Deb(line.length)


    dshittr = gpd.GeoDataFrame(geometry=[line], crs="EPSG:3857")    
#    Deb(dshittr.iloc[0])
    line=dshittr.iloc[0]
#    Deb(type(line))
#    Deb(line.geometry)
#    Deb(line.iloc[0])
    abcc=LineString(line.iloc[0])
    line=abcc

#    line=line.to_crs(3857)

    abc=geopy.distance.geodesic(line.coords[0],line.coords[-1]).meters
#    abc=geopy.distance.geodesic(dshittr.iloc[0],dshittr.iloc[1]).meters


    Deb(f"DaLength {abc:.3f}")

    '''

print(f"baddies    {countbaddies}")


## this all comes from
##https://geographiclib.sourceforge.io/Python/doc/code.html#geographiclib.geodesicline.GeodesicLine.Position

anewline=Geodesic.WGS84.Line(40.756015, -73.970487, 35,caps=3979)
print(anewline)

## fails on internal error
##anobj=geographiclib.geodesicline.GeodesicLine(anewline,40.756015, -73.970487, 35,caps=3979)
##print(anobj)
