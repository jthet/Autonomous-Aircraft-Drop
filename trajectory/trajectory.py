from math import sin, cos, atan, degrees, radians, sqrt, log
import pandas as pd
from util import Vector3

def get_variables():
    '''
    Retrieves variables from flight_data.csv
    '''
    vars = pd.read_csv('flight_data.csv')

    lon, lat, alt = vars.iloc[-1][0], vars.iloc[-1][1], vars.iloc[-1][2]/1000
    v_x, v_y, v_z = vars.iloc[-1][3]/100, vars.iloc[-1][4]/100, vars.iloc[-1][5]/100
    wind_speed, wind_direction = vars.iloc[-1][6], vars.iloc[-1][7]

    air_speed = sqrt(v_x**2 + v_y**2)
    bearing = 90 - degrees(atan(v_y/v_x))
    if bearing < 0:
        bearing += 360

    arca_alt = 182.88  # m
    alt = alt - arca_alt

    return air_speed, bearing, v_z, alt, wind_speed, wind_direction

def wind_gradient(v1, z1, z2, alpha):
    '''
    Calculates wind speed at specific altitudes to help determine the gradient between 0 and 150 ft
    '''
    v2 = v1*(z2/z1)**alpha
    return v2

def trapezoidal(x, y):
    '''
    Calculates area under speed-time curve using trapezoidal method
    '''
    area = 0
    for i in range(len(x) - 1):
        base = x[i + 1] - x[i]
        height = (y[i] + y[i + 1])/2
        
        area += base*height
        
    return area

def calculate_drop_coordinates(air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction):
    '''
    Calculates drop coordinates using variables extracted from Pixhawk and kinematics
    '''
    target_coordinates = Vector3(0, 0, 0)

    payload_velocity = Vector3(air_speed*sin(radians(bearing)), air_speed*cos(radians(bearing)), vertical_speed)
    wind_velocity = Vector3(wind_speed*sin(radians(wind_direction)), wind_speed*cos(radians(wind_direction)), 0)

    g = -9.81  # m/s^2

    ### FEED SEPARATELY
    ground_speed = 1
    ground_direction = 0
    ground_altitude = 0.000001  # m

    alpha = (log(abs(wind_velocity.y)) - log(abs(ground_speed*cos(radians(ground_direction)))))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in y

    time = (-vertical_speed - sqrt(vertical_speed**2 - 4*altitude/3.28084*g/2))/g  # time for payload to hit ground
    displacement = Vector3(payload_velocity.x*time*3.28084, payload_velocity.y*time*3.28084, -150)  # Standardized to ft

    times = []
    wind_speeds = []
    for z in range(150, 0, -10):
        times.append((-vertical_speed - sqrt(vertical_speed**2 - 4*(altitude - z)/3.28084*g/2))/g)
        wind_speeds.append(wind_gradient(ground_speed*cos(radians(ground_direction)), ground_altitude, z, alpha))

    drop_coordinates = target_coordinates - displacement
    drop_coordinates.y -= trapezoidal(times, wind_speeds)*cos(wind_direction)

    return drop_coordinates

def main():
    air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction = get_variables()
    print(calculate_drop_coordinates(air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction))

if __name__ == "__main__":
    main()
