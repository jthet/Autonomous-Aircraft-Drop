import csv
from math import sqrt, log, sin, cos, asin, acos, atan, degrees, radians
import pandas as pd
from pymavlink import mavutil, mavwp

connection_string = '/dev/ttyUSB0'
master = mavutil.mavlink_connection(connection_string, baud=57600)

class Vector3:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<%.9f, %.9f, %.3f>' % (self.x, self.y, self.z)

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def unit(self):
        mag = self.magnitude()
        return Vector3(self.x/mag, self.y/mag, self.z/mag)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def angle(self, other):
        m = self.unit()
        n = other.unit()
        r = m.dot(n)

        return degrees(acos(r))

def receive_GLOBAL_POSITION_INT():
    '''
    receives data from the pixhawk
    '''
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'], blocking=True)
    if msg:
        return msg   

def receive_WIND():
    msg = master.recv_match(type=['WIND'], blocking=True)
    if msg:
        return msg

def send_GLOBAL_POSITION_INT(waypoints):
    '''
    sends gps coordinates back to pixhawk
    '''
    wp = mavwp.MAVWPLoader()   
    altitude = 45.72                                                 
    seq = 1
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    radius = 10
    N = len(waypoints)
    for i in range(N):                  
        wp.add(mavutil.mavlink.MAVLink_mission_item_message(master.target_system,
                    master.target_component,
                    seq,
                    frame,
                    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                    0, 0, 0, radius, 0, 0,
                    waypoints[i]['lat'], waypoints[i]['lon'], altitude))
        seq += 1                                                                                  

    master.waypoint_clear_all_send()                                     
    master.waypoint_count_send(wp.count())                          

    for i in range(wp.count()):
        msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
        master.mav.send(wp.wp(msg.seq))                                                                      
        print(f'Sending waypoint {msg.seq}')

def get_variables():
    '''
    Retrieves variables from flight_data.csv

    Returns:
        air_speed (m/s)
        bearing (degrees)
        vertical_speed (m/s)
        altitude (m)
        wind_speed (m/s)
        wind_direction (degrees)
    '''

    filename = 'flight_data.csv'

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)

        pos = receive_GLOBAL_POSITION_INT()
        wind = receive_WIND()
        row = [pos.lat, pos.lon, pos.alt, pos.vx, pos.vy, pos.vz, wind.speed, wind.direction]  # Create row of data
        writer.writerow(row)  # Write row to CSV file

    vars = pd.read_csv('flight_data.csv')

    lon, lat, alt = vars.iloc[-1][0], vars.iloc[-1][1], vars.iloc[-1][2]/1000
    v_x, v_y, v_z = vars.iloc[-1][3]/100, vars.iloc[-1][4]/100, vars.iloc[-1][5]/100
    wind_speed, wind_direction = vars.iloc[-1][6], vars.iloc[-1][7]

    air_speed = sqrt(v_x**2 + v_y**2)
    bearing = 90 - degrees(atan(v_y/v_x))
    if bearing < 0:
        bearing += 360

    return lon, lat, air_speed, bearing, v_z, alt, wind_speed, wind_direction

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

def calculate_drop_coordinates(target_latitude, target_longitude, latitude, air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction):
    '''
    Calculates drop coordinates using variables extracted from Pixhawk and kinematics
    '''
    target_coordinates = Vector3(target_longitude, target_latitude, 0)

    payload_velocity = Vector3(air_speed*sin(radians(bearing)), air_speed*cos(radians(bearing)), vertical_speed)
    wind_velocity = Vector3(wind_speed*sin(radians(wind_direction)), wind_speed*cos(radians(wind_direction)), 0)

    g = -9.81  # m/s^2

    ### FEED SEPARATELY
    ground_speed = 1
    ground_direction = wind_direction
    ground_altitude = 0.00001  # m

    alpha_x = (log(abs(wind_velocity.x)) - log(abs(ground_speed*sin(radians(ground_direction)))))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in x
    alpha_y = (log(abs(wind_velocity.y)) - log(abs(ground_speed*cos(radians(ground_direction)))))/(log(altitude) - log(ground_altitude))  # shear coeff for wind in y

    time = (-vertical_speed - sqrt(vertical_speed**2 - 4*altitude/3.28084*g/2))/g  # time for payload to hit ground
    displacement = Vector3(payload_velocity.x*time*3.28084, payload_velocity.y*time*3.28084, -altitude)  # Standardized to ft

    times = []
    wind_speeds_x = []
    wind_speeds_y = []
    for z in range(150, 0, -10):
        times.append((-vertical_speed - sqrt(vertical_speed**2 - 4*(altitude - z)/3.28084*g/2))/g)
        wind_speeds_x.append(wind_gradient(ground_speed*sin(radians(ground_direction)), ground_altitude, z, alpha_x))
        wind_speeds_y.append(wind_gradient(ground_speed*cos(radians(ground_direction)), ground_altitude, z, alpha_y))

    displacement.x -= trapezoidal(times, wind_speeds_x)*sin(wind_direction)
    displacement.y -= trapezoidal(times, wind_speeds_y)*cos(wind_direction)
    
    displacement.x /= (364000*cos(latitude))
    displacement.y /= 364000

    drop_coordinates = target_coordinates - displacement

    send_GLOBAL_POSITION_INT((drop_coordinates.x, drop_coordinates.y))

    return drop_coordinates  # degrees

def check_drop(lat1, lon1, lat2, lon2):
    '''
    Calculate the great circle distance between two points on the earth (specified in decimal degrees) in feet.
    '''

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))

    # Radius of Earth in feet
    r = 20902000

    if abs(c*r) < 15:
        pass

def main(target_latitude, target_longitude):
    while True:
        longitude, latitude, air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction = get_variables()
        drop_coordinates = calculate_drop_coordinates(target_latitude, target_longitude, latitude, air_speed, bearing, vertical_speed, altitude, wind_speed, wind_direction)
        check_drop(drop_coordinates.x, drop_coordinates.y, latitude, longitude)

if __name__ == '__main__':
    main()
