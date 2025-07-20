#import warnings
#warnings.filterwarnings("error", category=UserWarning)
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

from rotateline4 import *

from to_coords import *


from geographiclib.geodesic import Geodesic
from makerec3 import *

from getpos import *
from geotools import * 








sunposition=get_position('now', -73.97206, 40.75643)
Deb(sunposition)

#######SUPPORT FOR SWAP LAT LONG###########

def swappoint(apoint):
    return([apoint.y,apoint.x])




def wall2polygon2(alist):
    """!
@callergraph



@callgraph
    """


    global total

    wallnum=0
    
    for wall1 in alist:
        for wall2 in wall1:
#            Deb(wall2)

            b=wall2

            wallnum=wallnum+1

        ############################################
            k=1


            sunaz=sunposition['azimuth']  #149.617534
            assert (0.0+sunaz)<=360

            elevation=1.0*sunposition['altitude']  #13.197431
            height=45

            dshit2 = gpd.GeoDataFrame(geometry=[LineString(b)], crs="WGS84")


            barney = dshit2.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

            with open("/tmp/prerot" + str(wallnum) + ".json", "w") as w1:
                w1.write(barney)
                w1.close()

            dshit3=dshit2.to_crs("EPSG:3857")

#            Deb(type(dshit2))
#            Deb(type(dshit3))


            dshit3['centroid']=dshit3['geometry'].centroid



    #17        assert (0.0+a['azi1'])<=360

    ##skip rotate
            skiprotate=False
            if skiprotate:
                dshit4=dshit2
                dshit=dshit2
            else:
        ## Previously added 180 to line's az
                wallaz= calculate_azimuth_line(LineString(b))
                Deb("Rotate "+str(wallaz)+"  to  "+str(sunaz))
                dshitline = rotateline4(LineString(b), sunaz)
                #dshit = rotateline(dshit3.geometry.get_coordinates(),wallaz, sunaz)

                dshit4 = gpd.GeoDataFrame(geometry=[dshitline], crs="WGS84")
                dshit2=dshit4
                dshit=dshit4



            barney = dshit4.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

            with open("/tmp/fromwall" + str(wallnum) + ".json", "w") as w1:
                w1.write(barney)
                w1.close()


    #        if sunaz < 180:
    #            compaz=sunaz+180
    #        else:
    #            compaz=sunaz-180

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
    #            newshadow = makerecdeg(dshit4, deglength, k)
                newshadow = makerec3(dshitline, 7*slength, k) # was b

                Deb(type(newshadow))

                barney = newshadow.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"





                with open("/tmp/bigwall" + str(wallnum) + ".json", "w") as w1:
                    w1.write(barney)
                    w1.close()


                if wallnum==1:
                    total=newshadow
                else:
                    gdfunion=gpd.overlay(total,newshadow,how='union',keep_geom_type=False)
                    total=gdfunion

        total=total.sjoin(total,how="inner")
        return total




#############################################


def wall2polygon(wall_list):
    """!
@callergraph



@callgraph
    """


    global total





#############################################




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


def unwraplist(alist):
    for wall1 in alist:
        for wall2 in wall1:
            Deb(wall2)


def main():
    """!
@callergraph



@callgraph
    """

    global total


    dlist=[]

#############################################
#############################################
###read in CSV###############################
#############################################
#############################################

    df = []
    df = pd.read_csv(
        "/Src/sun/path1.csv", sep=",")    

    df['geometry'] = df['geometry'].apply(loads)

    pd.set_option('display.max_colwidth',None)
    pd.set_option('display.max_columns',None)
    
    pd.set_option('display.max_rows',None)
    dshit12 = gpd.GeoDataFrame(df, crs="WGS84")
    dshit12['walls'] = dshit12.geometry.boundary.apply(extract_wall_coords)

    print(dshit12[['NAME', 'walls']].iloc[0])
#    print(dshit12)

    Deb(type(dshit12[['walls']].iloc[0])   )
    prepredlist=dshit12[['walls']]
    Deb(type(prepredlist))
    Deb(type(prepredlist.iloc[0]))
    predlist=pd.Series(prepredlist.iloc[0])
    dlist=predlist.to_list()
    Deb(dlist)


    dshit8=wall2polygon2(dlist)   
#    dshit8=unwraplist(dlist)   


    
    Deb(type(dshit8))

#    if not (dshit8.is_valid).all():
#        Deb("dshit is not valid")


    dshit8=dshit8.union_all()

    Deb(type(dshit8))
    Deb(dshit8.geom_type)
    dshit9=gpd.GeoDataFrame(geometry=[dshit8])

        
    barney = dshit9.to_json(to_wgs84=False)  # =True)  #  crs="EPSG:3627"
#    barney = dshit9.to_file("/tmp/total99.json",driver='GeoJSON')

    with open("/tmp/total" + str(99) + ".json", "w") as w1:
        w1.write(barney)
        w1.close()


    dshit9.set_crs("EPSG:2263",inplace=True)
    dshit8=dshit9
    dshit8['centroid']=dshit8['geometry'].centroid
    Deb(type(dshit8['centroid']))
    Deb(dshit8['centroid'])


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

'''
    dlist=[(-73.971815685417,40.756642525492), (-73.971845414769,40.756601849732), (-73.971882883991,40.756617685264), (-73.971892228211,40.756621634459), (-73.97194539848,40.756548887488), (-73.971898585074,40.756529102783), (-73.971917137126,40.75650372026), (-73.971966606825,40.756436035918), (-73.972187677007,40.756529466501), (-73.972014616104,40.756766249388), (-73.971949620799,40.756738780776), (-73.971793544195,40.756672818476), (-73.971815685417,40.756642525492)]

##135 e 50    dlist = [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775), (-73.97153870727, 40.75651820027), (-73.971458333347, 40.756484232235), (-73.971510010991, 40.75641352834), (-73.971514021216, 40.756415223183), (-73.971564459855, 40.756436539799), (-73.971612762728, 40.756370451916), (-73.971558313901, 40.75634744048), (-73.971580059362, 40.756317688647), (-73.97160519838, 40.756283293739), (-73.971755861794, 40.756346968589), (-73.971966606825, 40.756436035918), (-73.971917137126, 40.75650372026), (-73.971842763583, 40.756472287977), (-73.971820192309, 40.756503168892), (-73.971808961763, 40.756518534168), (-73.971834435727, 40.756529299637), (-73.971858272213, 40.756539374012), (-73.971847763277, 40.756553752515), (-73.971817644113, 40.75659496128), (-73.971647241465, 40.756559142392), (-73.97161694632, 40.75659895798), (-73.971591643035, 40.756593410934)]

##    dlist = [(-73.946942654932 ,40.806222154761), (-73.946977239811, 40.80617461534), (-73.947156723315, 40.806250005546), ( -73.947138469349, 40.806275095875), (-73.947122138526, 40.806297544119),( -73.947066845689, 40.8062743192),( -73.946942654932, 40.806222154761)]
'''
