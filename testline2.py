from shapely.geometry import Polygon, MultiPolygon, Point, LineString
import geopandas as gpd
from geopy.distance import geodesic
from geopy.point import Point
import geopy.distance

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






# 1. Define your centroid (latitude, longitude)
centroid_lat =  40.75643  # Example: New York City latitude
centroid_lon =  -73.97206 # Example: New York City longitude
centroid = Point(centroid_lat, centroid_lon)

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
for bearing in range(0, 361, 20):
    # Calculate the first end point of the line
    point1 = geodesic(kilometers=half_segment_length_km).destination(point=centroid, bearing=bearing)
    print(f"manufacture bearing {bearing}")
    # Calculate the second end point of the line (in the opposite direction)
    # The opposite bearing is (bearing + 180) % 360 to keep it within 0-360 range
    opposite_bearing = (bearing + 180) % 360
    point2 = geodesic(kilometers=half_segment_length_km).destination(point=centroid, bearing=opposite_bearing)
    print("#$#", type(point2))
    # Store the line segment (you might want to order them or just store as a pair)
    generated_line_segments.append((point1, point2))
    jlk=(point1, point2)
    print("$#$JLK ",type(jlk))
    howlong(point1, point2)



print(f"Generated {len(generated_line_segments)} line segments with centroid as midpoint:")
ls=1
for i, (p1, p2) in enumerate(generated_line_segments):
#    print(f"Line {i+1}:")

    print(f"line{ls} = LineString([( {p1.longitude:.9f},{p1.latitude:.9f}),({p2.longitude:.9f}, {p2.latitude:.9f})])")

    gorgo1= gpd.GeoDataFrame(geometry=[LineString([(p1.longitude,p1.latitude),(p2.longitude,p2.latitude)])], crs="WGS84")    

    barney = gorgo1.to_json(to_wgs84=True) 
    with open("/tmp/gorgo" + str(ls) +".json", "w") as w1:
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
