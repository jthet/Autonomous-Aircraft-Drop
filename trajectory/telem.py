from pymavlink import mavutil, mavwp

# Set the connection parameters (change accordingly)
connection_string = 'udp:127.0.0.1:14550' # sim connection

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string)

# Receive telemetry data from pixhawk to jetson
def receive_telem():
    #message
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'],blocking=True)             
    # Check if message is not None
    if msg:
        print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, msg.alt))        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg


# # Send telemetry data to pixhawk from jetson
# def send_telem(coords, phase):
#     MAX_BANK_ANGLE = 45  #Maximum allowable bank angle in degrees
#     #Convert maximum bank angle to radians for MAVLink parameter
#     max_bank_angle_rad = MAX_BANK_ANGLE * (math.pi / 180) #Maximum allowable bank angle in radians

#     altitude = altitude_handle(phase)
#     # Send telemetry data to Pixhawk

#     master.mav.mission_item_send(
#         master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
#         mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, max_bank_angle_rad, 0, 0,
#         coords['latitude'], coords['longitude'], altitude)