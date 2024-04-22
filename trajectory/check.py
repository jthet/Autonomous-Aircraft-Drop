from solution import calculate_drop_coordinate

drop_coordinates = calculate_drop_coordinate()
#live_coordinates = get_live_coordinates()

print(drop_coordinates)

distance = 15 # air_speed (m/s) * 1 (s) = distance (m)

if live_coordinates.x - distance <= drop_coordinates.x <= live_coordinates.x + distance and live_coordinates.y - distance <= drop_coordinates.y <= live_coordinates.y + distance:
    # trigger release
    pass
