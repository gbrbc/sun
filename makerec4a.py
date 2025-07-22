import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform

# 1. Define the input polygon in EPSG:2263 (NAD83 / New York Long Island, US survey feet)
# This is an example polygon roughly located in New York
# (coordinates are in US survey feet)
original_polygon_2263 = Polygon([(980000, 170000), (990000, 170000), (990000, 180000), (980000, 180000)])

print("Original Polygon (EPSG:2263):", original_polygon_2263)

# 2. Create the Transformer for converting from 2263 to 32618
transformer_to_32618 = pyproj.Transformer.from_crs(2263, 32618, always_xy=True)

# 3. Transform the polygon to EPSG:32618 (WGS 84 / UTM Zone 18N)
transformed_polygon_32618 = transform(transformer_to_32618.transform, original_polygon_2263)

print("Transformed Polygon (EPSG:32618):", transformed_polygon_32618)

# 4. Create the Transformer for converting back from 32618 to 2263
transformer_to_2263 = pyproj.Transformer.from_crs(32618, 2263, always_xy=True)

# 5. Transform the polygon back to EPSG:2263
retransformed_polygon_2263 = transform(transformer_to_2263.transform, transformed_polygon_32618)

print("Retransformed Polygon (EPSG:2263):", retransformed_polygon_2263)

# Verify the difference between the original and retransformed polygon (should be very small)
# This will show a very small difference due to precision limitations in floating point calculations
print("Difference between original and retransformed (should be close to 0):", 
      original_polygon_2263.difference(retransformed_polygon_2263).area)
