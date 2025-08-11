import geopandas as gpd
from shapely.geometry import LineString, Polygon

# rec3  from shapely.ops import transform
from pyproj import Transformer
from functools import partial
from shapely.ops import transform
from shapely.validation import make_valid, explain_validity
import pyproj
from shapely import force_2d


from geotools import *


def Deb(msg=""):
    """!
    @callergraph



    @callgraph
    """

    print(f"DebugMR {sys._getframe().f_back.f_lineno}: {msg}", flush=True, file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()


def makerec(line_coords, buffer_distance, k):
    """!
    @callergraph



    @callgraph
    """

    ## FIX wgx84/4326     32618
    ## transformer2m = Transformer.from_crs("EPSG:4326", "EPSG:32618")
    ## transformer2lat = Transformer.from_crs( "EPSG:32618","EPSG:4326")

    ## transformer2m(2,3)
    ## transformer2lat(3,2)

    #    Deb("STARTED MAKEREC")

    # 1. Define the initial LineString in longitude/latitude

    original_line = LineString(line_coords)

    l_az = calculate_azimuth_line(line_coords)
    #    Deb(f"makerec wallnum {k:d} az {l_az:.1f}")
    if l_az >= 180:
        Deb("MR negate buffer")
    #         buffer_distance = -buffer_distance

    # 2. Define the buffer distance in meters
    #    buffer_distance = 3

    # 3. Reproject to a local Azimuthal Equidistant (aeqd) projection for accurate buffering in meters
    #    Center the projection on the midpoint of the line for best accuracy.

    ###NEED TO LOOK AT DIRECTIONS MORE CAREFULLY
    ##https://pyproj4.github.io/pyproj/stable/api/transformer.html

    transformer2m = pyproj.Transformer.from_crs(crs_from="EPSG:4326", crs_to="EPSG:32618", always_xy=True, only_best=True)
    # ,errcheck=True

    transformer2lat = pyproj.Transformer.from_crs("EPSG:32618", "EPSG:4326", always_xy=True, only_best=True)
    # ,errcheck=True

    centroid = original_line.centroid

    assert original_line.is_valid
    original_line0 = force_2d(original_line)
    original_line = original_line0

    projected_line0 = transform(transformer2m.transform, original_line)
    projected_line = force_2d(projected_line0)

    ### NOT IN LONG/LAT assert projected_line.is_valid

    # 4. Create the buffer (rectangle) in the projected CRS
    # Deb('RecStep6')

    if abs(buffer_distance) < 2:
        Deb(f"buffer_distance {buffer_distance:.1f} < 2")
        return None

    assert notflip(original_line)
    writeWGS(original_line, "/tmp/bs1.json")

    ### NOT IN LONG/LAT    assert notflip(projected_line)
    writeWGS(projected_line, "/tmp/bs2.json")

    buffered_shape0 = projected_line.buffer(buffer_distance, cap_style=2, single_sided=True)  # cap_style=2 for flat ends

    buffered_shape = force_2d(buffered_shape0)

    writeWGS(buffered_shape, "/tmp/bs3.json")

    # 5. Reproject the buffered shape back to longitude/latitude (WGS84)
    #    final_polygon = transform(project_to_wgs84, buffered_shape)

    assert buffered_shape.is_valid

    final_polygon = transform(transformer2lat.transform, buffered_shape)

    assert final_polygon.is_valid

    # 6. Create a GeoDataFrame from the polygon

    gdf = gpd.GeoDataFrame(geometry=[final_polygon], crs="wgs84")

    if not (gdf.is_valid).all():
        newgdf = make_valid(gdf)
        gdf = newgdf

    assert (gdf.is_valid).all()

    fake = k
    bname = "/tmp/bldg" + str(fake) + ".json"
    pebbles = gdf.to_json(to_wgs84=True)  # True)  #  crs="WGS84"
    with open(bname, "w") as w:
        w.write(pebbles)
        w.close()

    return gdf
