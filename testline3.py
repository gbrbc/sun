#!/opt/local/bin/python3 

import warnings
warnings.filterwarnings("error", category=UserWarning)
import sys
import os
import shapely
from shapely.geometry import Polygon, MultiPolygon,  LineString
##removed Point
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
import random

import geographiclib
from geopy.point import Point

#from rotateline import *
from shapely import force_2d

###needed to read points from testline2
from geopy.point import Point
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic


def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugTL3 {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()





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

bylist=[(Point(40.75645251254337, -73.97206, 0.0), Point(40.75640748745654, -73.97206, 0.0)), (Point(40.75645115487044, -73.97204987436471, 0.0), Point(40.75640884512859, -73.97207012562886, 0.0)), (Point(40.75644724560719, -73.9720409700316, 0.0), Point(40.75641275438962, -73.97207902995856, 0.0)), (Point(40.75644125626885, -73.97203436099522, 0.0), Point(40.75641874372543, -73.97208563899612, 0.0)), (Point(40.756433909258455, -73.97203084440274, 0.0), Point(40.75642609073418, -73.97208915559385, 0.0)), (Point(40.75642609073418, -73.97203084440615, 0.0), Point(40.756433909258455, -73.97208915559726, 0.0)), (Point(40.75641874372543, -73.97203436100388, 0.0), Point(40.75644125626885, -73.97208563900477, 0.0)), (Point(40.75641275438962, -73.97204097004143, 0.0), Point(40.75644724560719, -73.9720790299684, 0.0)), (Point(40.75640884512859, -73.97204987437114, 0.0), Point(40.75645115487044, -73.97207012563528, 0.0)), (Point(40.75640748745654, -73.97206, 0.0), Point(40.75645251254337, -73.97206, 0.0)), (Point(40.75640884512859, -73.97207012562886, 0.0), Point(40.75645115487044, -73.97204987436471, 0.0)), (Point(40.75641275438962, -73.97207902995856, 0.0), Point(40.75644724560719, -73.9720409700316, 0.0)), (Point(40.75641874372543, -73.97208563899612, 0.0), Point(40.75644125626885, -73.97203436099522, 0.0)), (Point(40.75642609073418, -73.97208915559385, 0.0), Point(40.756433909258455, -73.97203084440274, 0.0)), (Point(40.756433909258455, -73.97208915559726, 0.0), Point(40.75642609073418, -73.97203084440615, 0.0)), (Point(40.75644125626885, -73.97208563900477, 0.0), Point(40.75641874372543, -73.97203436100388, 0.0)), (Point(40.75644724560719, -73.9720790299684, 0.0), Point(40.75641275438962, -73.97204097004143, 0.0)), (Point(40.75645115487044, -73.97207012563528, 0.0), Point(40.75640884512859, -73.97204987437114, 0.0)), (Point(40.75645251254337, -73.97206, 0.0), Point(40.75640748745654, -73.97206, 0.0))]



listlin=[line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14, line15, line16, line17, line18, line19]


def calculate_azimuth(ax, ay, bx, by):
    """Computes the bearing in degrees from the point A(ax,ay) to the point B(bx,by)."""
    a=Geodesic.WGS84.Inverse(ay,  ax,  by,  bx, outmask=1929)
    prelim=a['azi1']
    if prelim==360 or prelim==180:
        return 0
    if prelim < 0:
        prelim=360+prelim
    if prelim >= 180:
        prelim=prelim-180
    if prelim==360 or prelim==180:
        return 0

    return prelim

    TWO_PI = math.pi * 2
    theta = math.atan2(bx - ax, ay - by)
    if theta < 0.0:
        theta += TWO_PI
    return math.degrees(theta)




def calculate_azimuth_line2(aline):
    if not isinstance(aline,LineString):
        raise  TypeError("supply LineString instead")
    first_point = Point(aline.coords[0])
   
    last_point = Point(aline.coords[-1]) # Or line.coords[1] for a simple two-point line

    # Calculate azimuth
#    return calculate_azimuth(first_point.longitude, first_point.latitude, last_point.longitude, last_point.latitude)
    return calculate_azimuth(first_point.longitude, first_point.latitude, last_point.longitude, last_point.latitude)






gpd.options.display_precision = 9



## input is (Point(40.75645251254337, -73.97206, 0.0), Point(40.75640748745654, -73.97206, 0.0))
## what degree to rotate to
##  get length from input #1

def rotateline(mytuple,bearing):

    (p1,p2)=mytuple

## get centroid
    cline = LineString([p1, p2])
    centroid0 = cline.centroid
    centroid = force_2d(centroid0)
    Deb(f"cline  {cline}")


###cline is a fake just to get the centroid to build real line

    abclen=geopy.distance.geodesic(p1, p2).meters

    centroid=Point(centroid.x,centroid.y)

    point1 = geodesic(meters=abclen/2).destination(point=centroid, bearing=bearing)

    opposite_bearing = (bearing + 180) #% 360

    point2 = geodesic(meters=abclen/2).destination(point=centroid, bearing=opposite_bearing)

    line=LineString([point1, point2])

    dshit4 = gpd.GeoDataFrame(geometry=[LineString([(point1.longitude,point1.latitude),(point2.longitude,point2.latitude)])], crs="WGS84")    

    qaorig=calculate_azimuth_line2(line)

    fname = f"/tmp/ts{bearing:.0f}Q{qaorig:.0f}.json"
    barney = dshit4.to_file(fname,driver="GeoJSON")  # =True)  #  crs="EPSG:3627"
    valid = LineString([point1, point2])
    assert valid.is_valid

    return (LineString([point1, point2]))


def rotateline_line(myline,bearing):
    coords = list(myline.coords) # Convert to a list for easier indexing
    p1b = Point(coords[0])
    p2b = Point(coords[-1])

    return rotateline((p1b,p2b),bearing)

'''
#this is a test main routine


ls=1
bearing=25
for i, (p1, p2) in enumerate(bylist):
    newline=myrotate( (p1, p2), bearing)
    bearing = bearing + 25


'''
