import geopandas as gpd
from shapely.geometry import LineString, Polygon
# rec3  from shapely.ops import transform
from pyproj import Transformer
from functools import partial
from shapely.ops import transform

from geotools import *


def Deb(msg=""):
    """!
@callergraph



@callgraph
    """

    print(f"DebugMR {sys._getframe().f_back.f_lineno}: {msg}", flush=True,file=sys.stderr)
    sys.stdout.flush()
    sys.stderr.flush()





def makerec(line_coords,buffer_distance,k):

## FIX wgx84/4326     32618
## transformer2m = Transformer.from_crs("EPSG:4326", "EPSG:32618")
## transformer2lat = Transformer.from_crs( "EPSG:32618","EPSG:4326")

## transformer2m(2,3)
## transformer2lat(3,2)

    Deb("STARTED MAKEREC")

    # 1. Define the initial LineString in longitude/latitude



    original_line = LineString(line_coords)

    l_az=calculate_azimuth_line(line_coords)
    Deb(f"makerec wallnum {k:d} az {l_az:.1f}")
    if l_az >= 180:
         Deb('MR negate buffer')
#         buffer_distance = -buffer_distance 

    # 2. Define the buffer distance in meters
    #    buffer_distance = 3

    # 3. Reproject to a local Azimuthal Equidistant (aeqd) projection for accurate buffering in meters
    #    Center the projection on the midpoint of the line for best accuracy.




###NEED TO LOOK AT DIRECTIONS MORE CAREFULLY
##https://pyproj4.github.io/pyproj/stable/api/transformer.html    

    transformer2m = Transformer.from_crs(crs_from="EPSG:4326", crs_to="EPSG:32618", always_xy=True,only_best=True)
 # ,errcheck=True

    transformer2lat = Transformer.from_crs( "EPSG:32618","EPSG:4326", always_xy=True,only_best=True)
 # ,errcheck=True


    centroid = original_line.centroid

    """
    local_aeqd = f"+proj=aeqd +R=6371000 +units=m +lat_0={centroid.y} +lon_0={centroid.x}"
    project_to_aeqd = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'), # Source CRS (WGS84)
        pyproj.Proj(local_aeqd)       # Target CRS (local aeqd)
    )
    project_to_wgs84 = partial(
        pyproj.transform,
        pyproj.Proj(local_aeqd),      # Source CRS (local aeqd)
        pyproj.Proj(init='epsg:4326')  # Target CRS (WGS84)
    )
    """


#    projected_line = transform(project_to_aeqd, original_line)

    projected_line=transform(transformer2m.transform,original_line)

########lands a line 1/2 round globe, using wrong epsg
    """
    if k==10:
        parallel_line_mitre = original_line.parallel_offset(buffer_distance, 'mitre')
        gdfp = gpd.GeoDataFrame(geometry=[parallel_line_mitre], crs='wgs84')
        bname = "/tmp/wilma10.json"
        pebbles = gdfp.to_json(to_wgs84=True)  # True)  #  crs="WGS84"
        with open(bname, "w") as w:
            w.write(pebbles)
            w.close()
    """


    # 4. Create the buffer (rectangle) in the projected CRS
    buffered_shape = projected_line.buffer(buffer_distance, cap_style=2,single_sided=True) # cap_style=2 for flat ends

    # 5. Reproject the buffered shape back to longitude/latitude (WGS84)
#    final_polygon = transform(project_to_wgs84, buffered_shape)
    final_polygon = transform(transformer2lat.transform,buffered_shape)
    # 6. Create a GeoDataFrame from the polygon

##    final_polygon['newwallnum']=k


    gdf = gpd.GeoDataFrame(geometry=[final_polygon], crs='epsg:4326')


#    print(f"Original LineString: {original_line}")
#    print(f"Resulting Polygon (GeoDataFrame): {gdf}")

    fake=k
    bname = "/tmp/bldg" + str(fake) + ".json"
    pebbles = gdf.to_json(to_wgs84=True)  # True)  #  crs="WGS84"
    with open(bname, "w") as w:
        w.write(pebbles)
        w.close()


    Deb("LEFT MAKEREC")
    return gdf
