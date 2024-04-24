from pymavlink from mavwp, mavutil

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)
wp = mavwp.MAVWPLoader()

#*******Tested and Working*******  
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 91.44
    if phase == 'surveillance':
        return 45.72
      
def receive_GLOBAL_POSITION_INT():
    '''
    receives data from the pixhawk
    '''
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'], blocking=True)
    if msg:
        return msg

def send_GLOBAL_POSITION_INT(lat, lon, alt):
    '''
    sends gps coordinates back to pixhawk
    '''
    # send message
    master.mav.mission_item_send(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0,
        lat, lon, alt)

    # send waypoints
    # msg = master.mav.mission_item_message(
    #     master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    #     mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0,
    #     lat, lon, alt)
    # master.mav.send(msg)

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
