#!/usr/bin/env python3

# Situation:
# We have 2 pictures, where we know GPS location, time, speed, etc
# We are able to find a target in a given picture and we know the pixels of the location of the target in the frame of the picture
# The origin (center) of the picture should be the GPS coordinates * cos(camera_angle)

## With GPS, 6 digits behind the decimal place are significant

from math import radians, degrees, asin, atan2, sin, cos, tan

class Picture:
    def __init__(self, gps_coordinates, altitude, bearing, angle_of_depression):
        self.gps_coordinates = (gps_coordinates)  # (latitude, longitude)
        self.altitude = float(altitude)  # in meters
        self.bearing = float(bearing)  # directional angle, in degrees
        self.angle_of_depression = float(angle_of_depression)  # vertical angle, in degrees

    def calculate_new_gps(self, lat, lon, bearing, distance):
        R = 6371e3  # Radius of the Earth in meters
        bearing = radians(bearing)

        lat1 = radians(lat)
        lon1 = radians(lon)

        # https://stackoverflow.com/questions/45158779/create-coordinate-based-on-distance-and-direction

        lat2 = asin(sin(lat1) * cos(distance / R) + 
                    cos(lat1) * sin(distance / R) * cos(bearing))
        lon2 = lon1 + atan2(sin(bearing) * sin(distance / R) * cos(lat1), cos(distance / R) - sin(lat1) * sin(lat2))

        return degrees(lat2), degrees(lon2)

    def find_center_coordinates(self):
        # Calculate distance to the center based on the angle of depression
        distance_to_center = self.altitude / tan(radians(self.angle_of_depression))

        # Calculate the new GPS coordinates at this distance in the direction of the bearing
        center_lat, center_lon = self.calculate_new_gps(self.gps_coordinates[0], 
                                                        self.gps_coordinates[1], 
                                                        self.bearing, 
                                                        distance_to_center)
        return center_lat, center_lon



def main():
    # Example usage
    pic = Picture((30.2672, 97.7431), 150, 45, 30)  # Example coordinates, altitude in meters, bearing, and angle of depression
    center_coordinates = pic.find_center_coordinates()
    print("Center of the picture's coordinates:", center_coordinates)
    return  


if __name__ == '__main__':
    main()