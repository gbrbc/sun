import os
import sys
import pandas as pd
from shapely.geometry import Polygon
from sklearn.neighbors import BallTree
import numpy as np
import geopandas as gpd
from shapely  import wkt
from shapely.wkt  import loads



# This assumes the CSV file has columns such as 'ID', 'X', and 'Y', where each row represents a point.
# Points that have the same 'ID' create a polygon.

def Deb(msg=""):
  print(f"Debug {sys._getframe().f_back.f_lineno}: {msg}",flush=True)
  sys.stdout.flush()



##arg1 is the geometry
def convert_multipolygon(gdf9):
    gdf_approx = gpd.GeoDataFrame({'id': [1], 'geometry': [gdf9]}, crs="WGS84")

    # Calculate the convex hull and assign it back to a new GeoDataFrame or replace the geometry
    convex_hull_gs = gdf_approx.geometry.convex_hull
    # To put it into a GeoDataFrame, you can create a new one or update an existing one
    gdf_convex_hull = gpd.GeoDataFrame(gdf_approx.drop(columns=['geometry']), geometry=convex_hull_gs, crs=gdf_approx.crs)
    
    return gdf_convex_hull.iloc[0,1]




def create_balltree_from_polygons_csv(csv_file_path):
    """
    Reads polygon data from a CSV file, creates a BallTree, and returns it.

    Args:
        csv_file_path (str): The path to the CSV file containing polygon coordinates.

    Returns:
        sklearn.neighbors.BallTree: The created BallTree.
        list: A list of Shapely Polygon objects corresponding to the data.
    """

    df = pd.read_csv(csv_file_path)

    df['geometry'] = df['geometry'].apply(loads)
    gdf1 = gpd.GeoDataFrame(df, crs="EPSG:3395")  # Replace "your_crs"
# Calculate the centroid for each polygon


#####3 lines of gdf1>df1
    gdf1['centroid'] = gdf1['geometry'].centroid

# Extract the X and Y coordinates from the centroid points
    gdf1['X'] = gdf1['centroid'].map(lambda p: p.x)
    gdf1['Y'] = gdf1['centroid'].map(lambda p: p.y)

    Deb("gdf1")
    print(type(gdf1))
    print(gdf1)
    sys.stdout.flush()          


    polygons = []
    """

    # This groups by polygon ID and creates Shapely Polygon objects
    for name, group in gdf1.groupby('building_id'):
        if len(group) >= 3: # A polygon requires at least 3 points
            # Creates a Polygon from the points (assuming X and Y columns)
            # For Python 3.x, use list(zip(group.X, group.Y))
            print("/" * 30)
            poly = Polygon(list(zip(group.X, group.Y)))
            polygons.append(poly)
            Deb("poly")
            print(type(poly))
            print(poly)
            print("=" * 30)
            Deb("polygons")
            print(type(polygons))
            print(polygons)
            sys.stdout.flush()

    # Converts the polygons into a format appropriate for BallTree (e.g., centroids or bounding boxes)
    # BallTree typically operates on points (n_samples, n_features)
    # In this case, the centroid of each polygon is used as the representative point
    # A custom distance metric for polygon proximity might be needed if using the BallTree for direct polygon-to-polygon distance queries.
    polygon_centroids = np.array([(p.centroid.x, p.centroid.y) for p in polygons])

    Deb("polygon_centroids")
    print("/" * 30)
    print(type(polygon_centroids))
    print(polygon_centroids)
    sys.stdout.flush()    


    """
    pd.set_option('display.max_columns', None)
#    gdf1.set_option('display.max_columns', None)
    print(gdf1.info(),flush=True)
    Deb(type(gdf1.iloc[0].geometry.centroid))
    Deb(gdf1.iloc[0].geometry.centroid.x)
    Deb(len(gdf1))
#    exit()

    gdf1['geometry'] = gdf1['geometry'].apply(convert_multipolygon)

    for k in range(len(gdf1)):
#      poly = Polygon(list(gdf1.iloc[k].X, gdf1.iloc[k].Y))
      poly = Polygon(gdf1.iloc[k].geometry)
      polygons.append(poly)
      polygon_centroids.append(np.array(gdf1.iloc[k].geometry.centroid.x,gdf1.iloc[k].geometry.centroid.y))


#      polygon_centroids = np.array([(p.centroid.x, p.centroid.y) for p in gdf1])

    # Creates the BallTree
    # Different metrics can be selected depending on the data and requirements
    # 'euclidean' is a common metric
    ball_tree = BallTree(polygon_centroids, leaf_size=15, metric='euclidean')

    return ball_tree, polygons

if __name__ == "__main__":
    # Example usage:
    # Creates a dummy CSV file for demonstration

    if 0:
        csv_data = """ID,X,Y
        1,0,0
        1,1,0
        1,1,1
        1,0,1
        2,2,2
        2,3,2
        2,3,3
        2,2,3
        3,5,5
        3,6,5
        3,6,6
        3,5,6
        """
#        with open("pathall.csv", "w") as f:
#            f.write(csv_data)

# Builds the BallTree
ball_tree, polygons = create_balltree_from_polygons_csv("pathmn.csv")

# The BallTree can now be used for nearest neighbor queries or other operations
# For instance, query the nearest polygon to a given point:
query_point = np.array([[0.5, 0.5]])
distances, indices = ball_tree.query(query_point, k=1)

nearest_polygon_index = indices[0][0]
nearest_polygon = polygons[nearest_polygon_index]

print(f"Nearest polygon to {query_point[0]} is: {nearest_polygon}")

# The BallTree can also find neighbors within a certain radius
# For example, query for polygons within a radius of 1.0 from the query point
radius = 1.0
neighbors_indices = ball_tree.query_radius(query_point, r=radius)

print(f"Polygons within a radius of {radius} from {query_point[0]}:")
for index in neighbors_indices[0]:
    print(polygons[index])
