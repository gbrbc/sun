import os,sys
import geopandas as gpd
from shapely.geometry import LineString,Point
from shapely.affinity import rotate
import math
from geotools import * 

"""!
@callergraph



@callgraph
"""


def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugRot3 {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()





def rotateline(line,new_azimuth_degrees):

    """!
@callergraph



@callgraph
    """


    Deb(f"In rotateline  line  {line}   newdeg {new_azimuth_degrees}")
    if not isinstance(line,LineString):
        raise TypeError("supply LineString instead")

    # Create a sample LineString
#    line = LineString([(0, 0), (10, 5)])

#    line2=line.copy()

 
    assert line.is_valid, "Rotate line not valid"

##https://stackoverflow.com/questions/56989956/creating-a-centroid-column-from-geometry-shape-field-produces-attributeerror-n


#    line2["geometry"] = line2["geometry"].centroid

    # Calculate the centroid of the LineString
    line_centroid = line.centroid

    # Calculate the current azimuth (using a simple arctan2 for illustrative purposes)
    # Assuming a simple 2D cartesian coordinate system
    first_point = line.coords[0]
    last_point = line.coords[-1]
    dx = last_point[0] - first_point[0]
    dy = last_point[1] - first_point[1]
    current_azimuth_radians = math.atan2(dx, dy)
    current_azimuth_degrees = math.degrees(current_azimuth_radians)
    current_azimuth_degrees = calculate_azimuth_line(line)

    Deb(f"Original LineString: {line}")
    Deb(f"Line Centroid: {line_centroid}")
    Deb(f"Current Azimuth (degrees): {current_azimuth_degrees}")
    Deb(f"Requested Azimuth (degrees): {new_azimuth_degrees}")

    # Define the desired new azimuth in degrees
    #new_azimuth_degrees = 90  # Example: Rotate to a 90-degree azimuth (due East)

    # Calculate the rotation angle needed
    rotation_angle_degrees = new_azimuth_degrees - current_azimuth_degrees
#    if rotation_angle_degrees > 360:
#        rotation_angle_degrees = rotation_angle_degrees - 360

    # Rotate the LineString around its centroid to the new azimuth

    rotated_line = rotate(line, rotation_angle_degrees, origin=line_centroid)

#    rotated_line = rotate(line, rotation_angle_degrees, origin='center')

    if not os.path.exists("/tmp/bf455.json"):
      #  Deb("Rotate1")
        geo55=gpd.GeoSeries([line],[rotated_line])
      #  Deb("Rotate2")
        gdf55 = gpd.GeoDataFrame(geo55, geometry=0, crs="WGS84") # 'geometry=0' specifies the column containing the geometries
      #  Deb("Rotate3")
        gdf55.to_file("/tmp/bf455.json", driver="GeoJSON")
      #  Deb("Rotate4")
        geo66=gpd.GeoSeries(line_centroid)
      #  Deb("Rotate5")
        gdf66 = gpd.GeoDataFrame(geo66, geometry=0, crs="WGS84") # 'geometry=0' specifies the column containing the geometries
      #  Deb("Rotate6")
        gdf66.to_file("/tmp/mypoint.json")
      #  Deb("Rotate7")


#    Deb(f"Rotated LineString: {rotated_line}")
    Deb(f"Rotate Result Azimuth (degrees): {calculate_azimuth_line(rotated_line):1f}  vs   newdeg {new_azimuth_degrees}")

#    if rotation_angle_degrees<=0 or rotation_angle_degrees>360:
#        raise TypeError("az below 0 or over 360")



    return rotated_line
