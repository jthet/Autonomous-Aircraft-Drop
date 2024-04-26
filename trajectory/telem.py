from pymavlink from mavwp, mavutil

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)
wp = mavwp.MAVWPLoader()

#*******Tested and Working*******       
def receive_GLOBAL_POSITION_INT():
    '''
    receives data from the pixhawk
    '''
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'], blocking=True)
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
                    waypoints[i]['lat'],waypoints[i]['lon'], altitude))
        seq += 1                                                                                  

    master.waypoint_clear_all_send()                                     
    master.waypoint_count_send(wp.count())                          

    for i in range(wp.count()):
        msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
        master.mav.send(wp.wp(msg.seq))                                                                      
        print(f'Sending waypoint {msg.seq}')    

def receive_WIND():
    msg = master.recv_match(type=['WIND'], blocking=True)
    if msg:
        return msg

def main():
    # Define the filename
    filename = 'flight_data.csv'

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "alt", "v_x", "v_y", "v_z", "wind_speed", "wind_direction"])  # Write header

    while True:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)

            pos = receive_GLOBAL_POSITION_INT()
            wind = receive_WIND()
            row = [pos.lat, pos.lon, pos.alt, pos.vx, pos.vy, pos.vz, wind.speed, wind.direction]  # Create row of data
            writer.writerow(row)  # Write row to CSV file
        time.sleep(5)

if __name__ == "__main__":
    main()
