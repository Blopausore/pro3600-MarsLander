import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.point import Point

folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def load_map(map_name):
    """Convert a json map into his initial points and the lander initial state"""
    map_path = os.path.join(folder_path, "data/maps", map_name)
    with open(map_path, "r") as json_file:
        map = json.load(json_file)
    
    point_coords = map.get('points')
    initial_state = map.get('lander_state')
    points = [Point(x, y) for x, y in point_coords]

    return points, initial_state

