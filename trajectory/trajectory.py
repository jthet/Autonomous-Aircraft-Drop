from util import Vector3
from math import sin, cos, radians, sqrt, log
import matplotlib.pyplot as plt

def wind_gradient(v1, z1, z2, alpha):
    v2 = v1*(z2/z1)**alpha
    return v2

def trapezoidal(x, y):
    area = 0
    for i in range(len(x) - 1):
        base = x[i + 1] - x[i]
        height = (y[i] + y[i + 1])/2
        
        area += base*height
        
    return area

def calculate_drop_coordinate():
    '''
    Variables needed from Pixhawk:
      target_coordinate - from GPS and converted to standardized coordinates
      air_speed
      bearing
      vertical_speed
      altitude
      wind_speed
      wind_direction
    '''
    target_coordinate = Vector3(0, 0, 0)

    air_speed = 20  # m/s
    bearing = 37  # deg (0 - N, 90 - E, 180 - S, 270 - W)
    vertical_speed = 2  # m/s
    aircraft_velocity = Vector3(air_speed*sin(radians(bearing)), air_speed*cos(radians(bearing)), vertical_speed)

    altitude = 150  # ft

    wind_speed = 2
    wind_direction = 0  # Should be 0 or 180 (head or tail wind) 
    wind_velocity = Vector3(wind_speed*sin(radians(wind_direction)), wind_speed*cos(radians(wind_direction)), 0)

    payload_velocity = aircraft_velocity

    g = -9.81  # m/s^2

    ground_speed = 1
    ground_direction = 0
    ground_altitude = 0.000001  # m

    alpha = (log(abs(wind_velocity.y)) - log(abs(ground_speed*cos(radians(ground_direction)))))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in y

    time = (-vertical_speed - sqrt(vertical_speed**2 - 4*altitude/3.28084*g/2))/g  # time for payload to hit ground
    displacement = Vector3(payload_velocity.x*time*3.28084, payload_velocity.y*time*3.28084, -150)  # Standardized to ft

    # time array
    times = []
    wind_speeds = []
    for z in range(150, 0, -10):
        times.append((-vertical_speed - sqrt(vertical_speed**2 - 4*(altitude - z)/3.28084*g/2))/g)
        wind_speeds.append(wind_gradient(ground_speed*cos(radians(ground_direction)), ground_altitude, z, alpha_y))

    drop_coordinate = target_coordinate - displacement
    drop_coordinate.y -= trapezoidal(times, wind_speeds)*cos(wind_direction)

    return drop_coordinate
