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

from rotateline import *

###needed to read points from testline2
from geopy.point import Point

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


#bylist=[(Point( -73.97206,40.75645251254337, 0.0), Point( -73.97206, 40.75640748745654, 0.0)), (Point(40.75645115487044, -73.97204987436471, 0.0), Point(40.75640884512859, -73.97207012562886, 0.0)), (Point(40.75644724560719, -73.9720409700316, 0.0), Point(40.75641275438962, -73.97207902995856, 0.0)), (Point(40.75644125626885, -73.97203436099522, 0.0), Point(40.75641874372543, -73.97208563899612, 0.0)), (Point(40.756433909258455, -73.97203084440274, 0.0), Point(40.75642609073418, -73.97208915559385, 0.0)), (Point(40.75642609073418, -73.97203084440615, 0.0), Point(40.756433909258455, -73.97208915559726, 0.0)), (Point(40.75641874372543, -73.97203436100388, 0.0), Point(40.75644125626885, -73.97208563900477, 0.0)), (Point(40.75641275438962, -73.97204097004143, 0.0), Point(40.75644724560719, -73.9720790299684, 0.0)), (Point(40.75640884512859, -73.97204987437114, 0.0), Point(40.75645115487044, -73.97207012563528, 0.0)), (Point(40.75640748745654, -73.97206, 0.0), Point(40.75645251254337, -73.97206, 0.0)), (Point(40.75640884512859, -73.97207012562886, 0.0), Point(40.75645115487044, -73.97204987436471, 0.0)), (Point(40.75641275438962, -73.97207902995856, 0.0), Point(40.75644724560719, -73.9720409700316, 0.0)), (Point(40.75641874372543, -73.97208563899612, 0.0), Point(40.75644125626885, -73.97203436099522, 0.0)), (Point(40.75642609073418, -73.97208915559385, 0.0), Point(40.756433909258455, -73.97203084440274, 0.0)), (Point(40.756433909258455, -73.97208915559726, 0.0), Point(40.75642609073418, -73.97203084440615, 0.0)), (Point(40.75644125626885, -73.97208563900477, 0.0), Point(40.75641874372543, -73.97203436100388, 0.0)), (Point(40.75644724560719, -73.9720790299684, 0.0), Point(40.75641275438962, -73.97204097004143, 0.0)), (Point(40.75645115487044, -73.97207012563528, 0.0), Point(40.75640884512859, -73.97204987437114, 0.0)), (Point(40.75645251254337, -73.97206, 0.0), Point(40.75640748745654, -73.97206, 0.0))]

#29Jul  bylist=[(Point( -73.97206,40.75645251254337, 0.0), Point( -73.97206, 40.75640748745654, 0.0)),(Point(-73.97204987436471, 40.75645115487044, 0.0), Point(-73.97207012562886, 40.75640884512859, 0.0)), (Point(-73.9720409700316, 40.75644724560719, 0.0), Point(-73.97207902995856, 40.75641275438962, 0.0)), (Point(-73.97203436099522, 40.75644125626885, 0.0), Point(-73.97208563899612, 40.75641874372543, 0.0)), (Point(-73.97203084440274, 40.756433909258455, 0.0), Point(-73.97208915559385, 40.75642609073418, 0.0)), (Point(-73.97203084440615, 40.75642609073418, 0.0), Point(-73.97208915559726, 40.756433909258455, 0.0)), (Point(-73.97203436100388, 40.75641874372543, 0.0), Point(-73.97208563900477, 40.75644125626885, 0.0)), (Point(-73.97204097004143, 40.75641275438962, 0.0), Point(-73.9720790299684, 40.75644724560719, 0.0)), (Point(-73.97204987437114, 40.75640884512859, 0.0), Point(-73.97207012563528, 40.75645115487044, 0.0)), (Point(-73.97206, 40.75640748745654, 0.0), Point(-73.97206, 40.75645251254337, 0.0)), (Point(-73.97207012562886, 40.75640884512859, 0.0), Point(-73.97204987436471, 40.75645115487044, 0.0)), (Point(-73.97207902995856, 40.75641275438962, 0.0), Point(-73.9720409700316, 40.75644724560719, 0.0)), (Point(-73.97208563899612, 40.75641874372543, 0.0), Point(-73.97203436099522, 40.75644125626885, 0.0)), (Point(-73.97208915559385, 40.75642609073418, 0.0), Point(-73.97203084440274, 40.756433909258455, 0.0)), (Point(-73.97208915559726, 40.756433909258455, 0.0), Point(-73.97203084440615, 40.75642609073418, 0.0)), (Point(-73.97208563900477, 40.75644125626885, 0.0), Point(-73.97203436100388, 40.75641874372543, 0.0)), (Point(-73.9720790299684, 40.75644724560719, 0.0), Point(-73.97204097004143, 40.75641275438962, 0.0)), (Point(-73.97207012563528, 40.75645115487044, 0.0), Point(-73.97204987437114, 40.75640884512859, 0.0)), (Point(-73.97206, 40.75640748745654, 0.0), Point(-73.97206, 40.75645251254337, 0.0))]


#bylist=[( Point(-73.972060000, 40.756407487),Point( -73.972060000,40.756452513)),(Point( -73.972049874,40.756451155), Point(-73.972070126, 40.756408845)),(Point( -73.972040970,40.756447246), Point(-73.972079030, 40.756412754)),(Point( -73.972034361,40.756441256), Point(-73.972085639, 40.756418744)),(Point( -73.972030844,40.756433909), Point(-73.972089156, 40.756426091)),(Point( -73.972030844,40.756426091), Point(-73.972089156, 40.756433909)),(Point( -73.972034361,40.756418744), Point(-73.972085639, 40.756441256)),(Point( -73.972040970,40.756412754), Point(-73.972079030, 40.756447246)),(Point( -73.972049874,40.756408845), Point(-73.972070126, 40.756451155)),(Point( -73.972060000,40.756407487), Point(-73.972060000, 40.756452513)),(Point( -73.972070126,40.756408845), Point(-73.972049874, 40.756451155)),(Point( -73.972079030,40.756412754), Point(-73.972040970, 40.756447246)),(Point( -73.972085639,40.756418744), Point(-73.972034361, 40.756441256)),(Point( -73.972089156,40.756426091), Point(-73.972030844, 40.756433909)),(Point( -73.972089156,40.756433909), Point(-73.972030844, 40.756426091)),(Point( -73.972085639,40.756441256), Point(-73.972034361, 40.756418744)),(Point( -73.972079030,40.756447246), Point(-73.972040970, 40.756412754)),(Point( -73.972070126,40.756451155), Point(-73.972049874, 40.756408845)),(Point( -73.972060000,40.756452513), Point(-73.972060000, 40.756407487))]

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
bearing=0
countbaddies=0
compaz=0

ls=1
for i, (p1, p2) in enumerate(bylist):


    print ( '#' * 45)

#    Deb(f"STEP2  {p1}")
#    print(f"line{ls} = LineString([( {p1.longitude:.9f},{p1.latitude:.9f}),({p2.longitude:.9f}, {p2.latitude:.9f})])")

    '''
    if ls==2:
        print(p1)
        print(p2)
        Deb(howlong(p1,p2))

    '''


    cline = LineString([p1, p2])
    centroid = cline.centroid
    Deb(f"cline  {cline}")

###cline is a fake just to get the centroid to build real line

    abclen=geopy.distance.geodesic(p1, p2).meters
    Deb(f"  len  {abclen:.2f}")


###Do here what rotate was supposed to


    Deb('test 1')
    centroid=Point(centroid.x,centroid.y)
    Deb(f"centroid  {centroid}")
    Deb(f"args   {abclen/2000}   {centroid}  {bearing}")


    
#    point1 = geodesic(kilometers=abclen/2000).destination(point=centroid, bearing=bearing)
    point1 = geodesic(meters=2.5).destination(point=centroid, bearing=bearing)
    Deb(f"point1 post-geodesic STEP2  {point1}")
    Deb(f"point1  {type(point1)}")    

    opposite_bearing = (bearing + 180) #% 360
    point2 = geodesic(kilometers=abclen/2000).destination(point=centroid, bearing=opposite_bearing)
    Deb(f"point2 post-geodesic STEP2a {point2}")
    Deb(f"point2  {type(point2)}")    
##blameme   points have equal value, but linestring has diff seconds for long
##blame the lines are 5meters apart in southern direction
    line=LineString([point1, point2])
    Deb(f"centroid  {centroid}")
    Deb(f"line post-geodesic  {line}  bearing {bearing}  opp  {opposite_bearing}")
    Deb(f"STEP3 line  {type(line)}")

    Deb(f"newline {line}")
    qaorig=calculate_azimuth_line2(line)

    Deb(f"#manufactured bearing {bearing} vs actual {qaorig:.1f}")

    if False==closeaz(bearing,qaorig):
        Deb('bearing off')
#        raise ValueError("bearing diff qaorig >5")


    '''
    randomcompass=random.randint(0,359)

    dshitline = rotateline(LineString(line), randomcompass)

    qa=calculate_azimuth_line(dshitline)

    Deb(dshitline)

    '''
##took out dshitline,
##30jul    dshit4 = gpd.GeoDataFrame(geometry=[line], crs="WGS84")    
    dshit4 = gpd.GeoDataFrame(geometry=[LineString([(point1.longitude,point1.latitude),(point2.longitude,point2.latitude)])], crs="WGS84")    
    fname = f"/tmp/ts{bearing:d}Q{qaorig:.0f}.json"
    barney = dshit4.to_file(fname,driver="GeoJSON")  # =True)  #  crs="EPSG:3627"


    dshit4 = gpd.GeoDataFrame(geometry=[line.centroid], crs="WGS84")    

    fname = f"/tmp/ts{bearing:d}Q{qaorig:.0f}CENT.json"
#    barney = dshit4.to_file(fname,driver="GeoJSON")  # =True)  #  crs="EPSG:3627"





    

#    if False==closeaz(bearing,qa):
#        raise ValueError(str(bearing)+" diff qa " + str(qa) + ">5")




    ls=ls+1
    compaz = compaz + 10
    bearing = bearing + 20

        
exit()

























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

    randomcompass=random.randint(0,359)

    dshitline = rotateline(LineString(line), randomcompass)

    qa=calculate_azimuth_line(dshitline)
#    if False==closeaz(133,qa):
#        raise ValueError("bearing diff qa >5")

    if False==closeaz(randomcompass,qa):
        raise ValueError(str(randomcompass)+" diff qa " + str(qa) + ">5")



    if qa<(randomcompass-2) or qa>(randomcompass+2):
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
