import unittest
import numpy as np
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(".."))))

from src.environment.surface import Surface 
from src.environment.entities.lander import Lander
from src.environment.environment import Environment
from src.environment.action import Action
from src.environment.utils.constants import X_SCALE, Y_SCALE
from src.score.scoring_manager import ScoringManager
from src.score.utils.constants import (
    SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE
)                                       
from src.utils.segment import Segment,Point

class TestEnvironment(unittest.TestCase):
    def test_dynamic_free_fall(self):
        with open("./data/maps/level_one_cg.json", "r") as json_file:
            initial_parameters = json.load(json_file) 
        points = initial_parameters.get('points')
        surface = Surface(list(map(lambda point: Point(*point), points)))
        initial_state = initial_parameters.get('lander_state')

        environment = Environment(surface, initial_state)

        with open('./tests/data/free_fall_level_one.jsonl', 'r',encoding='utf-8') as result_file:
            states = []
            for json_state in result_file:
                states.append(json.loads(json_state))
        if states[0] != initial_state:
            raise Exception("Test error : initial state is not the same as the one in the test file")

        for state in states:
            if abs(state['y'] - environment.lander.y) > 1:
                print(state['y'], environment.lander.y)
            
            for key in state.keys():
                self.assertAlmostEqual(int(getattr(environment.lander, key)), int(state[key]), delta=1)
            environment.step(Action(0, 0))

    def test_collision(self):
        with open("./data/maps/flat_surface.json", "r") as json_file:
            flat_surface = json.load(json_file)

        surface = Surface(list(map(lambda point: Point(*point), flat_surface.get('points'))))
        lander_initial_state = flat_surface.get('lander_state')
        map_y = surface.landing_area[0].y
        lander_initial_state['y'] = map_y + 1
        environment = Environment(surface, lander_initial_state)
        
        # Collision : 
        environment.lander.update(h_speed = -10)
        environment.step(Action(0, 0))
        self.assertTrue(environment.landing_on_site())
        self.assertEqual(environment.lander.rotate, 0)
        self.assertEqual(environment.lander.power, 0)
        environment.reset()

        # Crash
        environment.lander.update(h_speed = -100)
        environment.step(Action(0, 0))
        self.assertFalse(environment.successful_landing())
        environment.reset()

        # Exit
        environment.lander.update(x=6800, y=map_y+1000, h_speed = 0, v_speed = 10000) 
        environment.step(Action(0, 0))
        self.assertFalse(environment.landing_on_site())
        self.assertTrue(environment.exit_zone())
        