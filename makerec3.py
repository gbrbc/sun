import geopandas as gpd
from shapely.geometry import LineString, Polygon
from shapely.ops import transform
from functools import partial
import pyproj

def makerec3(line_coords,buffer_distance,k):


    # 1. Define the initial LineString in longitude/latitude
    #line_coords = [(-74.006, 40.7128), (-74.005, 40.7130)]
#    line_coords = [(-73.971558876777, 40.756579563884), (-73.971583976616, 40.756537332775)]


    original_line = LineString(line_coords)

    # 2. Define the buffer distance in meters
#    buffer_distance = 3

    # 3. Reproject to a local Azimuthal Equidistant (aeqd) projection for accurate buffering in meters
    #    Center the projection on the midpoint of the line for best accuracy.
    centroid = original_line.centroid
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

    projected_line = transform(project_to_aeqd, original_line)

    # 4. Create the buffer (rectangle) in the projected CRS
    buffered_shape = projected_line.buffer(buffer_distance, cap_style=2) # cap_style=2 for flat ends

    # 5. Reproject the buffered shape back to longitude/latitude (WGS84)
    final_polygon = transform(project_to_wgs84, buffered_shape)

    # 6. Create a GeoDataFrame from the polygon
    gdf = gpd.GeoDataFrame(geometry=[final_polygon], crs='epsg:4326')

#    print(f"Original LineString: {original_line}")
#    print(f"Resulting Polygon (GeoDataFrame): {gdf}")

    fake=17
    bname = "/tmp/bldg" + str(fake) + ".json"
    pebbles = gdf.to_json(to_wgs84=True)  # True)  #  crs="WGS84"
    with open(bname, "w") as w:
        w.write(pebbles)
        w.close()


    return gdf
