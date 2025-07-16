
## Function to extract coordinates from the MultiPolygon
#
def to_coords(multipolygon):
    """
    Extracts coordinates from a MultiPolygon object, including holes.

    Args:
        multipolygon: A Shapely MultiPolygon object.

    Returns:
        A list of coordinate tuples.
    """
    coords_list = []
    for polygon in multipolygon.geoms:
        coords_list.extend(list(polygon.exterior.coords[:-1]))
        for interior in polygon.interiors:
            coords_list.extend(list(interior.coords[:-1]))
    return coords_list

