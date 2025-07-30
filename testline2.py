#!/opt/local/bin/python3 

import inspect
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
import geopandas as gpd
from geopy.distance import geodesic
from geopy.point import Point
from geographiclib.geodesic import Geodesic
import geopy.distance



inspect.getmembers(gpd, inspect.ismodule)

inspect.getmembers(geopy.distance, inspect.ismodule)

inspect.getmembers(geopy.distance, inspect.ismodule)




def howlong(point1, point2):
    print(type(point1))
    print(type(point2))
## the args arrive as type==geopy.point.Point

    a=LineString([point1, point2])
    fgh=geopy.distance.geodesic(a.coords[0],a.coords[-1]).meters
    abc=geopy.distance.geodesic(point1, point2).meters
    print(f"DaLength {abc:.3f}  vs  {fgh:.3f}")


def howlongline(aline):
    if not isinstance(aline,LineString):
        raise  TypeError("supply LineString instead")

    fgh=geopy.distance.geodesic(a.coords[0],a.coords[-1]).meters
    return fgh



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
    




# 1. Define your centroid (latitude, longitude)
centroid_lat =  40.75643  # Example: New York City latitude
centroid_lon =  -73.97206 # Example: New York City longitude
centroid = Point(centroid_lat, centroid_lon)
print(f"STEP1  cent {centroid}")
print(type(centroid))

# 2. Choose the TOTAL length of your lines (e.g., 200 kilometers)
total_line_length_km = 0.005

# The distance for each half-segment from the centroid
# Each half-segment will be half of the total line length
half_segment_length_km = total_line_length_km / 2

# Store the generated line segments as tuples of (start_point, end_point)
generated_line_segments = []

# 3. Iterate through angles from 0 to 180 degrees
# We only need to go up to 180 because 180-360 will be covered by the opposite direction.
# We'll increment by 10 degrees for demonstration, adjust as needed.
print(f"Centr  {centroid }  {type(centroid)}")


for bearing in range(0, 361, 20):

    print ( '#' * 45)


    if bearing==80:
        bearing=90
    print ("args  ",half_segment_length_km,centroid, bearing)
    # Calculate the first end point of the line
    point1 = geodesic(kilometers=half_segment_length_km).destination(point=centroid, bearing=bearing)

    print(f"STEP2  pt1 post-geodesic {point1}")
    print(type(point1))


    print(f"manufacture bearing {bearing}")
    # Calculate the second end point of the line (in the opposite direction)
    # The opposite bearing is (bearing + 180) % 360 to keep it within 0-360 range
    opposite_bearing = (bearing + 180) % 360
    point2 = geodesic(kilometers=half_segment_length_km).destination(point=centroid, bearing=opposite_bearing)

    print(f"STEP2a  pt2 post-geodesic {point2}")
    print(type(point2))


    print("#$#", type(point2))
    # Store the line segment (you might want to order them or just store as a pair)
    generated_line_segments.append((point1, point2))
    jlk=(point1, point2)
##blameme   points have equal value, but linestring has diff seconds for long
##blame the lines are 5meters apart in southern direction
    testl=LineString([point1, point2])
    myaz=calculate_azimuth_line(testl)


    if int(bearing)==90:

        mandras1= gpd.GeoDataFrame(geometry=[LineString([(point1.longitude,point1.latitude),(point2.longitude,point2.latitude)])], crs="WGS84")    
#        mandras1= gpd.GeoDataFrame(geometry=[testl], crs="WGS84")    

        barney = mandras1.to_json(to_wgs84=True) 
        with open("/tmp/mandras" + str(bearing) +".json", "w") as w1:
            w1.write(barney)
            w1.close()


    print("$#$JLK ",type(jlk),"   az  ",calculate_azimuth_line(testl),  " manufac ",bearing)
    print("#$%centroid  ",centroid)
    print("%#%Lineme STEP3 post-geodesic  ", testl)
    print("%^$AZ ",calculate_azimuth_line(testl))
    print("%$%typeme  ", type(testl))

    howlong(point1, point2)
    print("Line3  ",point1, point2)

print(    generated_line_segments)

print(f"Generated {len(generated_line_segments)} line segments with centroid as midpoint:")
ls=1
for i, (p1, p2) in enumerate(generated_line_segments):
#    print(f"Line {i+1}:")

#    print(f"line{ls} = LineString([( {p1.longitude:.9f},{p1.latitude:.9f}),({p2.longitude:.9f}, {p2.latitude:.9f})])")

    print(f"(Point( {p1.longitude:.9f},{p1.latitude:.9f},0.0), Point({p2.longitude:.9f}, {p2.latitude:.9f},0.0))")




    gorgo1= gpd.GeoDataFrame(geometry=[LineString([(p1.longitude,p1.latitude),(p2.longitude,p2.latitude)])], crs="WGS84")    

    barney = gorgo1.to_json(to_wgs84=True) 
    with open("/tmp/gorgo" + str(bearing) +".json", "w") as w1:
        w1.write(barney)
        w1.close()


    ls=ls+1


#    print(f"  End 1: Lat: {p1.latitude:.7f}, Lon: {p1.longitude:.7f}")
#    print(f"  End 2: Lat: {p2.latitude:.7f}, Lon: {p2.longitude:.7f}")
#    print("-" * 30)

# Example: Accessing coordinates of the first line's endpoints
# print(generated_line_segments[0][0].latitude) # Latitude of the first point of the first line
# print(generated_line_segments[0][1].longitude) # Longitude of the second point of the first line

cmd="listlin=["

for i in range(1,20):
    cmd = cmd + ", line" + str(i)

print(cmd)    
