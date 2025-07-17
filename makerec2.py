import warnings
import os,sys
import geopandas
from shapely.geometry import LineString, Polygon
from pyproj import CRS, Transformer


warnings.filterwarnings("error", category=UserWarning)


## function for debugging
#
# more details
#
def Deb(msg=""):
    print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()





def makerec(line_lonlat, dim2, k):

#    if not isinstance(line,LineString):
#        raise TypeError("supply LineString instead")

    h=5/0
    Deb("makerec line_lonlat   k=" + str(k))
    Deb(line_lonlat)
    Deb(dim2)

##################################

    testkey=""                      # set if running as test
    if 'TESTKEY' in os.environ:
        testkey="_" + os.getenv( 'TESTKEY')






    # 1. Define the initial LineString in long/lat
#    line_lonlat = LineString([(10, 0), (10, 1)])  # Example LineString

    # 2. Define the source and target CRSs
    source_crs = CRS("EPSG:4326")  # WGS 84 (long/lat)
#ORIG    target_crs = CRS("EPSG:3857")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions


    match k:
        case 0:
            target_crs = CRS("EPSG:3857")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions
        case 1:
            target_crs = CRS("EPSG:2831")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions
        case 2:
            target_crs = CRS("EPSG:6538")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions
        case 3:
            target_crs = CRS("EPSG:32118")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions
        case 4:
            target_crs = CRS("EPSG:32218")  # Web Mercator (projected in meters) - Choose a suitable UTM zone for better accuracy if working with specific regions

    # 3. Create a transformer to convert between CRSs
    transformer_to_projected = Transformer.from_crs(source_crs, target_crs, always_xy=True)
    transformer_to_lonlat = Transformer.from_crs(target_crs, source_crs, always_xy=True)

    # 4. Transform the LineString to the projected CRS
    line_projected = LineString(transformer_to_projected.transform(*line_lonlat.coords.xy))

    Deb("    line_projected")
    Deb( line_projected)


    # 5. Create the offset LineString in the projected CRS
    offset_distance_meters = dim2   #3
#fail    offset_line_projected = line_lonlat.offset_curve(offset_distance_meters, join_style=1, mitre_limit=5,quad_segs=1) # join_style=1 for mitered corners
    offset_line_projected = line_projected.offset_curve(offset_distance_meters, join_style=1, mitre_limit=5) # join_style=1 for mitered corners

    Deb("    offset_line_projected")
    Deb(    offset_line_projected)


    # 6. Transform the offset LineString back to long/lat
    offset_line_lonlat = LineString(transformer_to_lonlat.transform(*offset_line_projected.coords.xy))

    # 7. Create connecting lines to close the rectangle
    # Get the start and end points of both lines
    start_point_original = line_lonlat.coords[0]
    end_point_original = line_lonlat.coords[-1]
    start_point_offset = offset_line_lonlat.coords[0]
    end_point_offset = offset_line_lonlat.coords[-1]

    # Create connecting lines
    connecting_line_start = LineString([start_point_original, start_point_offset])
    connecting_line_end = LineString([end_point_original, end_point_offset])

    # 8. Create a GeoSeries of all lines
    all_lines = geopandas.GeoSeries([line_lonlat, offset_line_lonlat, connecting_line_start, connecting_line_end])

    # 9. Use polygonize to create the rectangle
    polygon = list(all_lines.polygonize())[0]

    # Now, 'polygon' is your rectangle defined in long/lat coordinates.
    # You can then create a GeoDataFrame if needed:
    gdf = geopandas.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")

    print("Original LineString (lon/lat):", line_lonlat)
    print("Offset LineString (lon/lat):", offset_line_lonlat)
    print("Resulting Polygon (lon/lat):", polygon)

    return gdf
