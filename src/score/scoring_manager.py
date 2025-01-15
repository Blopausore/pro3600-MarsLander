from numpy import sqrt
from numpy.linalg import norm
from environment.environment import Environment
from environment.entities.lander import Lander
from environment.surface import Surface
from environment.utils.constants import X_SCALE, Y_SCALE, ROTATE_SCALE

from utils.point import Point
from utils.segment import Segment

from score.utils.constants import (
    SCORE_MAX_LANDING_OFF_SITE, SCORE_MIN_LANDING_ON_SITE,
    MAX_SPEED, SCORING_H_SPEED, SCORING_V_SPEED, SCORING_SPEED,
    SCORING_BEST_ANGLE, SCORING_ANGLE
)

class ScoringManager:
    """
    This class will permit to compute the score from the environments and the lander.

    For distance :
    If it lands on site, his score will be above a certain level. 
    Otherwise it depends of the distance with a lower maximum level.

    For speed :
    If it lands on site, it will be a combination of the vertical and horizontal speed.
    Otherwise, it will be the norm of the speed.

    For angle :

    """

    def landing_distance(self, surface: Surface, lander: Lander, collision_land: Segment):
        """ Compute the distance by "walke" of the collision to the landing site
        To do so, it browse the list of points that composed the map.
        If it encounters the collision point first, it starts calculating the distance from the collision point to the runway. 
        If not, it encounters the runway first and calculates the distance to the collision point.
        """
        if collision_land is None:
            return X_SCALE*Y_SCALE
        
        
        if collision_land == surface.landing_area:
            return 0.0

        point_lander = Point(lander.x, lander.y)
        run = False
        distance = 0
        for point in surface.get_points():
            if not run :
                if point == collision_land.point_a: # from left to the right 
                    point_from = point
                    point_to = collision_land.point_b
                    point_final = surface.landing_area.point_a
                    distance = point_lander.distance(collision_land.point_b)
                    run = True

                elif point == surface.landing_area.point_b: # from right to the left
                    point_from = surface.landing_area.point_a
                    point_to = point
                    point_final = collision_land.point_a
                    distance = collision_land.point_a.distance(point_lander)
                    run = True
                    
            else:
                point_from, point_to = point_to, point
                distance += point_from.distance(point_to)
                if point == point_final:
                    break
        return distance
    

    def scoring_distance_off_site(self, distance, surface_length):
        """Compute the score of the distance from the landing site"""
        return max(0, round(SCORE_MAX_LANDING_OFF_SITE*(1 - abs(distance)/surface_length)))
    
    def scoring_distance_on_site(self):
        """Compute the score of the distance from the landing site"""
        return SCORE_MIN_LANDING_ON_SITE
        
        
    def scoring_speed_on_site(self, lander: Lander, on_site: bool):
        """Compute speed score"""
        score = max(0, SCORING_V_SPEED*(1 - abs(lander.v_speed)/MAX_SPEED))
        score += max(0, SCORING_H_SPEED*(1 - abs(lander.h_speed)/MAX_SPEED))
        return score 
    
    def scoring_speed_off_site(self, lander: Lander, on_site: bool):
        """Compute speed score"""
        speed_norm = norm([lander.v_speed, lander.h_speed])
        return max(0, SCORING_SPEED*(1 - speed_norm/MAX_SPEED))
    
    def scoring_angle(self, lander):
        """Compute the score of the angle of the lander
        """
        if lander.rotate == 0:
            return SCORING_BEST_ANGLE
        
        return SCORING_ANGLE*(1 - abs(lander.rotate)/ROTATE_SCALE)
        

    def compute_score(self, environment: Environment):
        """Compute the global score"""
        
        if environment.exit_zone():
            return 0
        
        if environment.landing_on_site():
            distance_score = self.scoring_distance_on_site()
            speed_score = self.scoring_speed_on_site(
                lander=environment.lander, 
                on_site=environment.landing_on_site()
            )
            angle_score = self.scoring_angle(environment.lander)
            score = distance_score + speed_score + angle_score
            return max(SCORE_MIN_LANDING_ON_SITE, score)
        
        else:
            distance_score = self.scoring_distance_off_site(
                distance=self.landing_distance(
                    surface=environment.surface,
                    lander=environment.lander,
                    collision_land=environment.collision_area
                ),
                surface_length=environment.surface.length
            )
            speed_score = self.scoring_speed_off_site(
                lander=environment.lander, 
                on_site=environment.landing_on_site()
            )
            score = distance_score + speed_score
            return min(SCORE_MAX_LANDING_OFF_SITE, score)
