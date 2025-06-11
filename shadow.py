import pandas as pd

import geopandas as gpd


## the one I used for SPA on gbrmail is avialble as py module
## https://github.com/s-bear/sun-position

#https://www.fs.usda.gov/nac/buffers/guidelines/5_protection/6.html#:~:text=Use%20the%20formula%20s%20%3D%20h,shadow%20direction%20on%20the%20ground.

'''
Use the formula s = h/tan A to calculate shadow length. See the table below for an example. Sun angle calculators are available on the Web which will provide the sun angle (A) and azimuth angle for a given location based on the date and time.



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

