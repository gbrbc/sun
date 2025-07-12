
import sys
import os
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from shapely.affinity import translate
from shapely.wkt import loads
import pyproj
import math
import geopandas as gpd
import subprocess
import numpy as np
import pandas as pd

#import geographiclib

from rotateline2 import *

from to_coords import *


from geographiclib.geodesic import Geodesic


def Deb(msg=""):
    print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()


##Debug 430: [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775), (-73.97153870727, 40.75651820027), (-73.971458333347, 40.756484232235), (-73.971510010991, 40.75641352834), (-73.971514021216, 40.756415223183), (-73.971564459855, 40.756436539799), (-73.971612762728, 40.756370451916), (-73.971558313901, 40.75634744048), (-73.971580059362, 40.756317688647),



a=Geodesic.WGS84.Inverse( 40.756579563884,-73.971558876777,  40.756537332775,-73.971583976616)

print(a)

print("Length ",a['s12'],"   azimuth ",180.0+a['azi1'])




############################################

b= [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775)]
k=1


sunaz=149.617534
elevation=13.197431
height=45

dshit2 = gpd.GeoDataFrame(geometry=[LineString(b)], crs="WGS84")



dshit3=dshit2.to_crs("EPSG:3857")

Deb(type(dshit2))
Deb(type(dshit3))


#dshit3['centroid']=dshit3['geometry'].centroid


dshit = rotateline(dshit3.geometry.iloc[0].coords,180.0+a['azi1'], sunaz)

barney = dshit.to_json(to_wgs84=False)  # =True)  #  crs="EPSG:3627"





with open("/tmp/fromwall" + str(k) + ".json", "w") as w1:
    w1.write(barney)
    w1.close()


if sunaz < 180:
    compaz=sunaz+180
else:
    compaz=sunaz-180

tandeg=np.rad2deg(np.deg2rad(elevation))

slength=  height / tandeg

Deb("line length ")
Deb(dshit.geometry.length)
Deb("line x ")
Deb(dshit.geometry)

Deb("Shadow len ")
Deb( slength)





#https://geographiclib.sourceforge.io/html/python/

'''


class geographiclib.constants.Constants[source]
Constants describing the WGS84 ellipsoid

WGS84_a = 6378137.0
the equatorial radius in meters of the WGS84 ellipsoid in meters

WGS84_f = 0.0033528106647474805
the flattening of the WGS84 ellipsoid, 1/298.257223563

'''


'''

given the sun's azimuth and sun's elevation shining on wall at a different angle what formulas are used to compute the ground shadow for a program


a == sun's azi

b == sun's elev

sun unit vector = sin b cos a cos a sin b sin a

2)

rayw == (x   ,  y ,  z )
           p     p    p 


r0 is point on ground

n is ground normal vector in z

some point on ray passing thru rawy is

r == rayw + a b

some point on ground

(r - rayw) dot n = 0

various maths occur


            (rayw - r0) dot n
lambda == -------------

                         (rayw - r0) dot n )
r(projected) =   rayw - (  ------------     ) sun_unit_vector
                            s hat  dot  n




pick up with this

https://bigladdersoftware.com/epx/docs/8-3/engineering-reference/shading-module.html#:~:text=Basic%20shadowing%20concept%20structure,sin%CF%95CS3


149.320049	13.244926 
149.617534	13.197431 


'''

'''
A wall has a height of h.   The sun shines at a certain azimuth and elevation.  can the ground shadow be calculated by using the top of the wall as if it were a line in space, and what would be the formula to use in a program?




from a shapely linestring I want to create a rectangle by duplicating the linestring 3 meters away and then creating lines to complete the rectangle.  The initial linestring is defined in long/lat and all points need to be in long/lat when the rectangle is defined.  The rectangle will then be changed into a polygon in geopandas.  previous example code resulted in "AttributeError: module 'shapely.geometry' has no attribute 'line_merge'"

'''
