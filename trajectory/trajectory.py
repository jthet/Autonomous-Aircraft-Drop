from util import Vector3
from math import sin, cos, radians, sqrt

target_coordinate = Vector3(0, 0, 0)

air_speed = 20  # m/s
bearing = 0  # deg (0 - N, 90 - E, 180 - S, 270 - W)
vertical_speed = 2  # m/s
aircraft_velocity = Vector3(air_speed*sin(radians(bearing)), air_speed*cos(radians(bearing)), vertical_speed)

altitude = 150/3.28084  # m

wind_speed = 0
wind_direction = 180 
wind_velocity = Vector3(wind_speed*sin(radians(wind_direction)), wind_speed*cos(radians(wind_direction)), 0)

payload_velocity = aircraft_velocity + wind_velocity

g = 9.81  # m/s^2

t = sqrt(altitude*2/g)
displacement = Vector3(payload_velocity.x*t*3.28084, payload_velocity.y*t*3.28084, -150)  # ft

drop_coordinate = target_coordinate - displacement

print(drop_coordinate)
