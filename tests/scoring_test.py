import unittest
import numpy as np

from src.environment.surface import Surface 
from src.environment.entities.lander import Lander
from src.environment.utils.constants import X_SCALE, Y_SCALE
from src.score.scoring_manager import ScoringManager
from src.score.utils.constants import (
    SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE
)                                       
from src.utils.segment import Segment


flat_surface = Surface([[0, 1000], [X_SCALE, 1000]])
flat_land = Segment((0, 1000), (X_SCALE, 1000))

plateau_surface = Surface([[0, 0], [X_SCALE/3, 1000], [2*X_SCALE/3, 1000], [X_SCALE, 0]])
slope_land = Segment((0, 0), (X_SCALE/3, 1000))
p = np.array([X_SCALE/3, 1000])
"""
Shape of plateau_surface
       _____________
      /
     /
    /

"""


static_lander = Lander(x=3500, y=2000, h_speed=0, v_speed=0, fuel=0, rotate=0)


class TestScoringManager(unittest.TestCase):
    def test_landing_distance(self):
        scoring_manager = ScoringManager()
        static_lander.update(x=3500, y=1010)
        # self.assertEqual(
        #     scoring_manager.landing_distance(flat_surface, static_lander, flat_land),
        #     0
        # )

        c = np.array([X_SCALE/9, 333])
        static_lander.update(x=c[0], y=c[1])

        distance_0 = scoring_manager.landing_distance(plateau_surface, static_lander, slope_land)
        self.assertAlmostEqual(distance_0, np.linalg.norm(p-c), delta=0.1)

        static_lander.update(x=2*X_SCALE/9, y=666)
        distance_1 = scoring_manager.landing_distance(plateau_surface, static_lander, slope_land)
        self.assertLess(distance_1, distance_0)        
        

        static_lander.update(x=3*X_SCALE/9, y=1000)
        distance_2 = scoring_manager.landing_distance(plateau_surface, static_lander, slope_land)
        self.assertAlmostEqual(distance_2, 0, delta=0.1)
        self.assertLess(distance_2, distance_1)

    
        