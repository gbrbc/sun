#!/opt/local/bin/python3 
#  -*- compile-command: "env TESTKEY=`incr1o testkey` python3 testwall.py"; compile-read-command: t ; grep-command: "grep -d skip -I -Hni      `./active`" ; -*-



#import warnings
#warnings.filterwarnings("error", category=UserWarning)
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

#import geographiclib

#from rotateline import *
##for new rotate
from testline3 import *



from to_coords import *


from geographiclib.geodesic import Geodesic
from makerec import *

from getpos import *
from geotools import * 
from geopy.distance import geodesic
from datetime import datetime


#logd=open("/Users/reilly/time.log","a")

def logme(a):
    with open("/Users/reilly/time.log","a") as logd:
        current_datetime = datetime.now()
        timestamp_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S ")
        logd.write(str(timestamp_string)+str(a)+"\n")
        logd.close()


def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugTW {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()



os.environ["PROJ_ONLY_BEST_DEFAULT"]="1"
    
sunposition=get_position('now', -73.97206, 40.75643)
Deb(sunposition)
logme(sunposition)

#######SUPPORT FOR SWAP LAT LONG###########

def swappoint(apoint):
    return([apoint.y,apoint.x])




def wall2polygon2(alist,height):
    """!
@callergraph



@callgraph
    """


    global total
    global compaz
    global sunaz

    wallnum=0
    
    for wall1 in alist:
        for wall2 in wall1:
#            Deb(wall2)

            b=wall2

            wallnum=wallnum+1

            Deb("############################################")
            Deb(f"wallnum {wallnum:d}")


            sunaz=sunposition['azimuth']  #149.617534
            assert (0.0+sunaz)<=360

            elevation=1.0*sunposition['altitude']  #13.197431

            dshit2 = gpd.GeoDataFrame(geometry=[LineString(b)], crs="WGS84")


            barney = dshit2.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

            with open("/tmp/prerot" + str(wallnum) + ".json", "w") as w1:
                w1.write(barney)
                w1.close()

            dshit3=dshit2.to_crs("EPSG:3857")

#            Deb(type(dshit2))
#            Deb(type(dshit3))


            dshit3['centroid']=dshit3['geometry'].centroid


###compaz is perpindicular to incoming rays of sun

            if sunaz > 269:
                compaz=sunaz-90
            else:
                compaz=sunaz+90




    ##skip rotate
            skiprotate=False
            if skiprotate:
                dshit4=dshit2
                dshit=dshit2
            else:
        ## Previously added 180 to line's az
                wallaz= calculate_azimuth_line(LineString(b))
                Deb("Rotate "+str(wallaz)+"  to  "+str(compaz))

#    Deb(isinrange(f_p.x, -75,-72))
                assert (-74 > -75)
                assert (-74 < -72)
                assert isinrange(-74,-75,-72)
                assert isinrange(40,38,41)

                assert notflip(LineString(b))

                dshitline = rotateline_line(LineString(b), compaz)

                assert notflip(LineString(dshitline))

                #dshit = rotateline(dshit3.geometry.get_coordinates(),wallaz, sunaz)

                dshit4 = gpd.GeoDataFrame(geometry=[dshitline], crs="WGS84")
                dshit2=dshit4
                dshit=dshit4


            result_az = calculate_azimuth_gdf(dshit4)
#            Deb(type(result_az))

            Deb(f"Compare in {compaz:.1f}  out {result_az:.1f}")

            barney = dshit4.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

            with open("/tmp/postrot" + str(wallnum) + ".json", "w") as w1:
                w1.write(barney)
                w1.close()


##https://www.suncalc.org/#/40.7143,-74.006,10/2025.07.21/11:06/45/3
## says 28m for shadow length

            tanrad=(math.tan(np.deg2rad(elevation)))

            slength=  height / tanrad


            #############################################
            #############################################
            #####now call makerec2 to make shadow box####
            #############################################
            #############################################



            deglengthlat=slength * (1/111111)
            deglengthlon=slength * (1/(111111*math.cos(40)))
            deglength=3*math.fabs((deglengthlat+deglengthlon))/2

            Deb(f"Shadow len {slength:.2f} -> {deglength:.7f}   {(deglength*111111):.2f}  m  hgt {height:.1f} tanrad {tanrad:.1f}")





############################################
##JSON files################################
############################################
############################################

##  
##  
##  
##  wall2polygon2
##    write /tmp/prerotN of each wall of input
##  
##    call rotateline for each wall
##    write /tmp/postrotN of result
##
##  wall2polygon2->makerec3
##          makes bldg17 -- should be rectangle
##  
##    /tmp/postrectNN out of makerecN
##    makes /tmp/bigwall after call to makerec
##    returns union of all shadows
##  
##  
##  
##  
##  


            for k in range(0,1):
                wallaz=calculate_azimuth_line(LineString(dshitline))

#                if wallaz>180:
                if sunaz<180:
                    slength=slength
                else:
                    slength=-slength
                Deb(f"sunaz {sunaz:.1f}  compaz {compaz:.1f}    slength {slength:.1f}    wallaz {wallaz:.1f}  wallnum {wallnum:d}")
                fstr = f"sunaz {sunaz:.1f}  compaz {compaz:.1f}    slength {slength:.1f}    wallaz {wallaz:.1f}  wallnum {wallnum:d}"
                logme(fstr)

                newshadow = makerec(dshitline, slength, wallnum) # was b

#                Deb(f"newshadow  {newshadow}  {type(newshadow)}")

                barney = newshadow.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"





                with open("/tmp/postrect" + str(wallnum) + ".json", "w") as w1:
                    w1.write(barney)
                    w1.close()


                if wallnum==1:
                    total=newshadow
                else:
#                    elucidate(total)
#                    elucidate(newshadow)

                    try:
                        gdfunion=gpd.overlay(total,newshadow,how='union',keep_geom_type=True,make_valid=True)
                        total=gdfunion
                    except NotImplementedError as e:
                        # Handle the NotImplementedError exception
                        print(f"Error: Feature not implemented yet: {e}")

                    except shapely.errors.GEOSException as e:
                        print(f"Error: Feature not implemented yet: {e}")


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




def unwraplist(alist):
    for wall1 in alist:
        for wall2 in wall1:
            Deb(wall2)


def main():
    df = pd.read_csv(
        "/Src/sun/path1.csv", sep=",")    


    df['geometry'] = df['geometry'].apply(loads)

    pd.set_option('display.max_colwidth',None)
    pd.set_option('display.max_columns',None)
    
    pd.set_option('display.max_rows',None)





    dfrows=len(df)





    Deb(f"df rows {dfrows:d}")
    for rower in range(0,dfrows):

        print(f"Trying {df['NAME'].iloc[rower]} in row {rower:d}")
        logme(f"Trying {df['NAME'].iloc[rower]} in row {rower:d}")

        newshadow=mainengine(df,rower)

###try to insert the name of the bldg into the dataframe->json

        maybename=df['NAME'].iloc[rower]
        Deb('maybename')
        Deb(maybename)
        Deb(type(maybename))
        if len(str(maybename))>0:
            df['bldg']=str(maybename)

        writeGDF(newshadow,"/tmp/site"+str(rower)+".json")

#        Deb("newshadow")
#        Deb(newshadow)
#        assert notflip(newshadow)

        if rower==0:
            totalpack=newshadow
        else:
            try:
                gdfunion=gpd.overlay(totalpack,newshadow,how='union',keep_geom_type=False,make_valid=True)
                totalpack=gdfunion
            except NotImplementedError as e:
                        # Handle the NotImplementedError exception
                print(f"Error: Feature not implemented yet: {e}")


#    Deb("totalpack")
#    Deb(totalpack)
#    assert notflip(totalpack)



    barney = totalpack.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"

    with open("/tmp/totalpack.json", "w") as w1:
        w1.write(barney)
        w1.close()



def mainengine(df,rower):
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

#    df = []
#    rower=0


    dshit12 = gpd.GeoDataFrame(df, crs="WGS84")
    dshit12['walls'] = dshit12.geometry.boundary.apply(extract_wall_coords)

#    print(dshit12[['NAME', 'walls']].iloc[rower])
#    print(dshit12)

#    Deb(type(dshit12[['walls']].iloc[rower])   )
    prepredlist=dshit12[['walls']]
#    Deb(type(prepredlist))
#    Deb(type(prepredlist.iloc[rower]))
    predlist=pd.Series(prepredlist.iloc[rower])
    dlist=predlist.to_list()
#    Deb(dlist)
    
####get height

    height=int(dshit12['Ground Elevation'].iloc[rower]+0)
#    Deb(dshit12['NAME'].iloc[rower])
#    Deb(f"height  {height:d}")
    

    assert height>0

    dshit8=wall2polygon2(dlist,height)   
#    dshit8=unwraplist(dlist)   


    
#    Deb(type(dshit8))

#    if not (dshit8.is_valid).all():
#        Deb("dshit is not valid")


    dshit8=dshit8.union_all()

#    Deb(type(dshit8))
#    Deb(dshit8.geom_type)
    dshit9=gpd.GeoDataFrame(geometry=[dshit8],crs="EPSG:4326")

        
    barney = dshit9.to_json(to_wgs84=True)  # =True)  #  crs="EPSG:3627"
#    barney = dshit9.to_file("/tmp/total99.json",driver='GeoJSON')

    with open("/tmp/total" + str(rower) + ".json", "w") as w1:
        w1.write(barney)
        w1.close()


#    dshit9.set_crs("EPSG:2263",inplace=True)
##?    dshit8=dshit9
##?    dshit8['centroid']=dshit8['geometry'].centroid
#    Deb(type(dshit8['centroid']))
#    Deb(dshit8['centroid'])
    return dshit9

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


'''
kimberly or what is in path138.csv

shadow wrong way
3
4
7
8
11
12



coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)]
bowtie = Polygon(coords)
clean = bowtie.buffer(0)
<MULTIPOLYGON (((0 0, 0 2, 1 1, 0 0)), ((1 1, 2 2, 2 0, 1 1)))>
len(clean.geoms)
list(clean.geoms[0].exterior.coords)
list(clean.geoms[1].exterior.coords)


"shapely.buffer" how to determine the left vs right side of a "linestring" which is ""single_sided=True" to choose "distance" being negative or positive

what is the formula for direction of "linestring" with regard to "shapely.buffer" and "geos"



where to find algorithm to create a 5 meter line with an azimuth every 45 degrees from 0 to 360 without using libraries at the long/lat point -74.006,40.7143

https://geographiclib.sourceforge.io/cgi-bin/GeodSolve


'''
