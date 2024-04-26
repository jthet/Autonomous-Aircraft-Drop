from pymavlink import mavutil

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)

#*******Tested and Working*******       
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
