# test_picture.py
import pytest
from target_coord_calculator import Picture  # Replace 'your_module' with the name of your Python file containing the Picture class

def test_find_center_coordinates():
    
    # Test data setup
    test_cases = [
        {'gps': (40.7128, -74.0060), 'altitude': 100, 'bearing': 45, 'depression': 30},
        {'gps': (35.6895, 139.6917), 'altitude': 200, 'bearing': 90, 'depression': 60},
        {'gps': (51.5074, -0.1278), 'altitude': 150, 'bearing': 135, 'depression': 45},
        {'gps': (34.0522, -118.2437), 'altitude': 250, 'bearing': 180, 'depression': 15},
        {'gps': (48.8566, 2.3522), 'altitude': 50, 'bearing': 270, 'depression': 75}
    ]

    # Expected results for each test case (these values need to be calculated based on the formula used in your Picture class)
    expected_results = [
        (40.71390143041409, -74.00454686773445),
        
    ]

    # Running tests
    for i, test in enumerate(test_cases):
        pic = Picture(test['gps'], test['altitude'], test['bearing'], test['depression'])
        assert pic.find_center_coordinates() == pytest.approx(expected_results[i], 0.001)





def test_calculate_new_gps():
    # Example values for testing
    lat, lon, bearing, distance = 40.7128, -74.0060, 90, 1000  # 1000 meters to the East
    pic = Picture((lat, lon), 150, bearing, 45)

    # Expected result for 1000 meters to the East
    expected_lat, expected_lon = 40.7128, -73.99290535448697

    # Get the actual result from the method
    actual_lat, actual_lon = pic.calculate_new_gps(lat, lon, bearing, distance)

    # Assert if the actual result is close to the expected result
    assert pytest.approx(expected_lat, 0.001) == actual_lat
    assert pytest.approx(expected_lon, 0.001) == actual_lon

# Additional tests can be written for edge cases and other scenarios
