import warnings
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
from makerec2deg import *

from getpos import *

#warnings.filterwarnings("error", category=UserWarning)






def Deb(msg=""):
    print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()



sunposition=get_position('now', -73.97206, 40.75643)
Deb(sunposition)

#######SUPPORT FOR SWAP LAT LONG###########

def swappoint(apoint):
    return([apoint.y,apoint.x])




def wall2polygon(wall_list):
    global total

    wallnum=0

    havehalf=1                  # have only 1 of 2 tuples

    for wall1,wall2 in wall_list:


        if havehalf:
            b=[(wall1,wall2)]
            inv1=wall2
            inv2=wall1
            havehalf=0
            continue

        assert         havehalf==0

        havehalf=1
        inv3=wall2
        inv4=wall1


        b=[b[0],(wall1,wall2)]

        wallnum=wallnum+1

    #    a=Geodesic.WGS84.Inverse( 40.756579563884,-73.971558876777,  40.756537332775,-73.971583976616)
        Deb(type(wall1))
        Deb(wall1)

        a=Geodesic.WGS84.Inverse(inv1,inv2,inv3,inv4)


        Deb(a)

        print("Initial line Length ",a['s12'],"   azimuth ",180.0+a['azi1'])




        ############################################

    #    b= [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775)]

#        b = [(wall1,wall2),(wall3,wall4)]

        k=1


        sunaz=sunposition['azimuth']  #149.617534
        assert (0.0+sunaz)<=360

        elevation=sunposition['altitude']  #13.197431
        height=45

        dshit2 = gpd.GeoDataFrame(geometry=[LineString(b)], crs="WGS84")



        dshit3=dshit2.to_crs("EPSG:3857")

        Deb(type(dshit2))
        Deb(type(dshit3))


        dshit3['centroid']=dshit3['geometry'].centroid



        assert (0.0+a['azi1'])<=360

##skip rotate
        skiprotate=True
        if skiprotate:
            dshit4=dshit2
            dshit=dshit2
        else:
    ## Previously added 180 to line's az
            dshit = rotateline(LineString(b),0.0+a['azi1'], sunaz)
            #dshit = rotateline(dshit3.geometry.get_coordinates(),180.0+a['azi1'], sunaz)

            dshit4 = gpd.GeoDataFrame(geometry=[dshit], crs="WGS84")

        barney = dshit4.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

        with open("/tmp/fromwall" + str(wallnum) + ".json", "w") as w1:
            w1.write(barney)
            w1.close()


        if sunaz < 180:
            compaz=sunaz+180
        else:
            compaz=sunaz-180

        tandeg=np.rad2deg(np.deg2rad(elevation))

        slength=  height / tandeg

        #Deb("line length ")
        #Deb(dshit4.geometry.length)
        #Deb("line x ")
        #Deb(dshit4.geometry)




        #############################################
        #############################################
        #####now call makerec2 to make shadow box####
        #############################################
        #############################################



        deglengthlat=slength * (1/111111)
        deglengthlon=slength * (1/(111111*math.cos(40)))
        deglength=8*3*math.fabs((deglengthlat+deglengthlon))/2

        Deb(f"Shadow len {slength:.2f} -> {deglength:.7f}   {(deglength*111111):.2f}  m")






        for k in range(0,1):
            newshadow = makerecdeg(dshit, deglength, k)

            Deb(type(newshadow))

            barney = newshadow.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"





            with open("/tmp/fromwall" + str(wallnum) + ".json", "w") as w1:
                w1.write(barney)
                w1.close()


            if wallnum==1:
                total=newshadow
            else:
                gdfunion=gpd.overlay(total,newshadow,how='union',keep_geom_type=False)
                total=gdfunion

    total=total.sjoin(total,how="inner")
    return total


def main():

    global total


    dlist = [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775), (-73.97153870727, 40.75651820027), (-73.971458333347, 40.756484232235), (-73.971510010991, 40.75641352834), (-73.971514021216, 40.756415223183), (-73.971564459855, 40.756436539799), (-73.971612762728, 40.756370451916), (-73.971558313901, 40.75634744048), (-73.971580059362, 40.756317688647), (-73.97160519838, 40.756283293739), (-73.971755861794, 40.756346968589), (-73.971966606825, 40.756436035918), (-73.971917137126, 40.75650372026), (-73.971842763583, 40.756472287977), (-73.971820192309, 40.756503168892), (-73.971808961763, 40.756518534168), (-73.971834435727, 40.756529299637), (-73.971858272213, 40.756539374012), (-73.971847763277, 40.756553752515), (-73.971817644113, 40.75659496128), (-73.971647241465, 40.756559142392), (-73.97161694632, 40.75659895798), (-73.971591643035, 40.756593410934)]

    dshit8=wall2polygon(dlist)   

    Deb(type(dshit8))

    if not (dshit8.is_valid).all():
        Deb("dshit is not valid")


    dshit8=dshit8.union_all()

        
    barney = dshit8.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"
#    barney = dshit8.to_file("/tmp/total99.json",driver='GeoJSON')

    with open("/tmp/total" + str(99) + ".json", "w") as w1:
        w1.write(barney)
        w1.close()


    dshit8=dshit8.to_crs("EPSG:2263")
    dshit8['centroid']=dshit8['geometry'].centroid
    print(type(dshit8['centroid']))
    print(dshit8['centroid'])


main()




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
