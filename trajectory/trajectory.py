from util import Vector3
from math import sin, cos, radians, sqrt, log
import matplotlib.pyplot as plt

def wind_gradient(v1, z1, z2, alpha):
    v2 = v1*(z2/z1)**alpha
    return v2

def trapezoidal(x, y):
    area = 0
    for i in range(len(x) - 1):
        # Calculate the width of the trapezoid
        base = x[i + 1] - x[i]
        
        # Calculate the average height of the trapezoid
        height = (y[i] + y[i + 1]) / 2
        
        # Calculate the area of the trapezoid and add it to the total area
        area += base * height
        
    return area

def extract_param(parameter_name):
  file_name = 'mav.parm'
  parameter_value = None
  with open(file_name, 'r') as file:
    for line in file:
      parts = line.split()
      if len(parts) > 1 and parts[0] == parameter_name:
        parameter_value = parts[1]
        break
  return parameter_value

# initial conditions

target_coordinate = Vector3(0, 0, 0)
# target_coordinate = Vector3(extract_param('GPS_POS1_X'), extract_param('GPS_POS1_Y'), extract_param('GPS_POS1_Z'))

air_speed = 20  # m/s
# air_speed = extract_param('TRIM_ARSPD_CM')

bearing = 0  # deg (0 - N, 90 - E, 180 - S, 270 - W)
vertical_speed = 2  # m/s
aircraft_velocity = Vector3(air_speed*sin(radians(bearing)), air_speed*cos(radians(bearing)), vertical_speed)

altitude = 150  # ft

wind_speed = 2
wind_direction = 0 
wind_velocity = Vector3(wind_speed*sin(radians(wind_direction)), wind_speed*cos(radians(wind_direction)), 0)

payload_velocity = aircraft_velocity

g = -9.81  # m/s^2

ground_speed = 1
ground_direction = 0
ground_altitude = 0.000001  # m

v2_x = abs(wind_speed*sin(radians(wind_direction)))
v1_x = abs(ground_speed*sin(radians(ground_direction)))
v2_y = abs(wind_speed*cos(radians(wind_direction)))
v1_y = abs(ground_speed*cos(radians(ground_direction)))

#alpha_x = (log(v2_x) - log(v1_x))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in x
alpha_y = (log(v2_y) - log(v1_y))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in y

t = (-vertical_speed - sqrt(vertical_speed**2 - 4*altitude/3.28084*g/2))/g  # time for payload to hit ground
displacement = Vector3(payload_velocity.x*t*3.28084, payload_velocity.y*t*3.28084, -150)  # Standardized to ft

# time array
time_array = []
altitude_array = []
for i in range(150, 0, -10):
    time_array.append((-vertical_speed - sqrt(vertical_speed**2 - 4*(altitude - i)/3.28084*g/2))/g)
    altitude_array.append(i)

# wind speed
wind_array_x = []
wind_array_y = []
for alt in altitude_array:
    #wind_array_x.append(wind_gradient(ground_speed*sin(radians(ground_direction)), ground_altitude, alt, alpha_x))
    wind_array_y.append(wind_gradient(ground_speed*cos(radians(ground_direction)), ground_altitude, alt, alpha_y))

drop_coordinate = target_coordinate - displacement

drop_coordinate.y -= trapezoidal(time_array, wind_array_y)*cos(wind_direction)

print(drop_coordinate)
