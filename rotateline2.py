import os,sys
import geopandas as gpd
from shapely.geometry import LineString
from shapely.affinity import rotate
import math


def Deb(msg=""):
    print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()


def rotateline(line,current_azimuth_degrees,new_azimuth_degrees):

    Deb('In rotateline')
    Deb(line)

    # Create a sample LineString
#    line = LineString([(0, 0), (10, 5)])

    # Calculate the centroid of the LineString
    line_centroid = line.centroid

    # Calculate the current azimuth (using a simple arctan2 for illustrative purposes)
    # Assuming a simple 2D cartesian coordinate system
    first_point = line.coords[0]
    last_point = line.coords[-1]
    dx = last_point[0] - first_point[0]
    dy = last_point[1] - first_point[1]
    current_azimuth_radians = math.atan2(dx, dy)
#    current_azimuth_degrees = math.degrees(current_azimuth_radians)

    Deb(f"Original LineString: {line}")
    print(f"Line Centroid: {line_centroid}")
    print(f"Current Azimuth (degrees): {current_azimuth_degrees}")

    # Define the desired new azimuth in degrees
    #new_azimuth_degrees = 90  # Example: Rotate to a 90-degree azimuth (due East)

    # Calculate the rotation angle needed
    rotation_angle_degrees = new_azimuth_degrees - current_azimuth_degrees

    # Rotate the LineString around its centroid to the new azimuth
    rotated_line = rotate(line, rotation_angle_degrees, origin=line_centroid)

    print(f"Rotated LineString: {rotated_line}")

    return rotated_line
