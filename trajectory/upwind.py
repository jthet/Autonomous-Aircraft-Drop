from pymavlink import mavwp, mavutil
from math import sin, cos, radians

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
                    waypoints[i]['lat'],waypoints[i]['lon'], altitude))
        seq += 1                                                                                  

    master.waypoint_clear_all_send()                                     
    master.waypoint_count_send(wp.count())                          

    for i in range(wp.count()):
        msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
        master.mav.send(wp.wp(msg.seq))                                                                      
        print(f'Sending waypoint {msg.seq}') 

def calculate_upwind_coordinates(wind_direction, distance, target_lat, target_lon):
    '''
    Calculate upwind coordinate
    '''
    if(wind_direction < 0):
        wind_direction = wind_direction + 360

    x_disp = distance*cos(radians(wind_direction))*(-1)
    y_disp = distance*sin(radians(wind_direction))*(-1)
    lat = target_lat + x_disp*(1/111320)
    lon = target_lon + y_disp*(1/111320)

    return lat, lon

def main(target1_lat, target1_lon, target2_lat, target2_lon):
    upwind1_lat, upwind1_lon = calculate_upwind_coordinates(wind_direction, 91.44, target1_lat, target1_lon)
    upwind2_lat, upwind2_lon = calculate_upwind_coordinates(wind_direction, 91.44, target2_lat, target2_lon)
    waypoints = []
    waypoints.append({'lat': upwind1_lat, 'lon': upwind1_lon})
    waypoints.append({'lat': upwind2_lat, 'lon': upwind2_lon})
    send_GLOBAL_POSITION_INT(waypoints)

if __name__ == "__main__":
    main()