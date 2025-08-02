import math
from shapely.geometry import LineString

#line_orig = LineString([(4, 5), (6, 7), (8, 7), (10, 8), (12, 8), (13, 7)])

def lengthen_line(line, extension_factor):

    if not isinstance(line,LineString):
        raise TypeError("supply LineString instead") 


    coords = list(line.coords)
    
    # Extend the first segment
    first_x1, first_y1 = coords[0]
    first_x2, first_y2 = coords[1]
    
    # Calculate direction vector for the first segment
    dx_first = first_x2 - first_x1
    dy_first = first_y2 - first_y1
    
    # Calculate new first point
    new_first_x = first_x1 - dx_first * extension_factor
    new_first_y = first_y1 - dy_first * extension_factor
    
    # Extend the last segment
    last_x1, last_y1 = coords[-2]
    last_x2, last_y2 = coords[-1]
    
    # Calculate direction vector for the last segment
    dx_last = last_x2 - last_x1
    dy_last = last_y2 - last_y1
    
    # Calculate new last point
    new_last_x = last_x2 + dx_last * extension_factor
    new_last_y = last_y2 + dy_last * extension_factor
    
    new_coords = [(new_first_x, new_first_y)] + coords[1:-1] + [(new_last_x, new_last_y)]
    return LineString(new_coords)

# Lengthen the line by a factor of 0.25 (meaning 25% of the end segments are extended)
#line_edited = lengthen_line(line_orig, 0.25) 
#print(line_edited)
# Output: LINESTRING (3.5 4.5, 6 7, 8 7, 10 8, 12 8, 13.25 6.75) 
# Note: output will vary depending on your starting coordinates and extension factor
