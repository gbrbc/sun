import pandas as pd

import geopandas as gpd


## the one I used for SPA on gbrmail is avialble as py module
## https://github.com/s-bear/sun-position

#https://www.fs.usda.gov/nac/buffers/guidelines/5_protection/6.html#:~:text=Use%20the%20formula%20s%20%3D%20h,shadow%20direction%20on%20the%20ground.

'''
Use the formula s = h/tan A to calculate shadow length. See the table below for an example. Sun angle calculators are available on the Web which will provide the sun angle (A) and azimuth angle for a given location based on the date and time.



'''


'''
In an urban environment, determining whether the sun is visible from a specific location involves more than just knowing sunrise and sunset times. It requires considering the
Sky View Factor (SVF), which is the proportion of the sky visible from a certain point, taking into account obstructions like buildings. 
Sky View Factor (SVF):

    The SVF is a dimensionless value between 0 and 1, where 0 represents a completely blocked space (no sky visible) and 1 represents an open area (entire sky visible).
    It is essentially a geometric concept that provides the proportion of the visible area of the sky within a specific location, like a street canyon.
    While there isnt a single, simple formula for direct sun visibility in an urban environment, the SVF helps in estimating the amount of direct sunlight penetration and the potential for solar access. 

Calculating SVF:

    Calculating SVF can involve various methods, including:
        Geometric methods: Utilizing building dimensions and distances to determine the visible sky area.
        Fish-eye photography: Taking images with a fish-eye lens and analyzing them to calculate the visible sky proportion.
        Simulation methods: Using Digital Surface Models (DSMs) and 3D city models to simulate sky visibility.
    A simplified approach for calculating SVF in a 2D street canyon involves considering the height (H) of the obstacle (building) and the width (W) between the obstacles (street).
        SVF true = cos arctan (H / (0.5 * W)) 

Obstruction Angle Algorithm:

    A more detailed calculation method for urban sky obstruction involves the obstruction angle algorithm.
    This method considers the obstruction between an urban surface and the sky hemisphere, expressed as azimuth and obstructed elevation angles.
    Obstructions like buildings can be simplified into rectangular planes, and the obstruction by each plane is determined by the range of obstructed azimuths and the maximum obstructed elevation angle at each azimuth. 

Other Factors Influencing Sun Visibility:

    Sun position: The suns position in the sky varies depending on the time of day, day of the year, and geographic location.
    Building height and distance: Taller buildings and closer proximity to them can significantly reduce the amount of direct sunlight received.
    Street orientation: The orientation of streets and buildings can affect how sunlight penetrates urban canyons. 

In summary, while there is no single formula to definitively say "the sun is visible" in an urban environment, the SVF provides a crucial measure of sky visibility, which in turn helps in estimating the extent of direct sunlight penetration and solar access at a specific location, taking into account the obstruction caused by urban structures. 

'''



#from geodatasets import get_path

#path_to_data = get_path("nybb")
gdf1 = gpd.read_file("~/Downloads/path.csv",ignore_geometry=False)


gdf=gpd.GeoDataFrame(gdf1)
gdf=gdf.set_geometry('the_geom',inplace=True)


gs=gdf['the_geom']

print('blue')
print(gs)


if not isinstance(gs,pd.DataFrame):
    print(type(gs))

print("blah")
print(gdf[['the_geom']])

gdf.plot(markersize=.5)

#print(gdf["centroid"])


###https://people.csail.mit.edu/ericchan/bib/pdf/p275-atherton.pdf
##doesnt take sun into account
##
##have pysolar in Downloads

