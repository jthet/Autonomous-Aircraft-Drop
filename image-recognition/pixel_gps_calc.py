import math

# Constants
NM_TO_M = 1e-6  # nanometers to meters
MM_TO_M = 1e-3  # millimeters to meters
CM_TO_M = 100  # millimeters to meters

def pixels_to_meters(px, altitude, sensor_width=5.02257946*MM_TO_M, focal_length=4.28*MM_TO_M, image_width=640):
    '''
    GSD = meter/pixel
    focal_length = 4.28 mm
    sensor_width = 5.0225794 mm
    '''
    GSD = (sensor_width * altitude) / (focal_length * image_width)
    return px * GSD

def offset_coordinates(lat, lon, x_pixels, y_pixels, altitude, bearing):
    '''
    Adjusts GPS coordinates based on pixel offsets and bearing.
    bearing is given in degrees and converted to radians for calculations.
    '''
    R = 6378137.0 # Earth's radius in meters

    # bearing to radians
    bearing = math.radians(bearing)
    
    dx = pixels_to_meters(x_pixels * math.cos(bearing) - y_pixels * math.sin(bearing), altitude)
    dy = pixels_to_meters(x_pixels * math.sin(bearing) + y_pixels * math.cos(bearing), altitude)
    
    new_longitude = lon + (dx / R) * (180 / math.pi) / math.cos(math.radians(lat))
    new_latitude = lat + (dy / R) * (180 / math.pi)
    
    return new_latitude, new_longitude

def dev():
    center_latitude = 40.0000000  
    center_longitude = 70.0000000 
    x_pixel_offset = 0  
    y_pixel_offset = 300  
    altitude = 100     
    bearing = 45  # bearing in degrees (rotation to the right from north)

    new_lat, new_lon = offset_coordinates(center_latitude, center_longitude, x_pixel_offset, y_pixel_offset, altitude, bearing)
    print(f"New GPS Coordinates: Latitude = {new_lat}, Longitude = {new_lon}")

if __name__ == '__main__':
    dev()