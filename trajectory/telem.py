from pymavlink import mavutil, mavwp

# Set the connection parameters
connection_string = '/dev/ttyS0'

# Connect to Pixhawk
master = mavutil.mavlink_connection(connection_string)

# Receive telemetry data from pixhawk to jetson
def receive_telem():
    # Get gps coordinates
    params = master.recv_match(type=['GLOBAL_POSITION_INT'],blocking=True)             
    if params:
        print("Global Position: Lat={}, Lon={}, Alt={}".format(params.lat, params.lon, params.alt))      
        return params
