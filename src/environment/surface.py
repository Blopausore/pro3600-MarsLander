import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.point import Point
from utils.segment import Segment

class Surface:
    lands : list[Segment]
    landing_area : Segment
    length : float

    def __init__(self, points: list[Point]):
        """Initialize a surface with a list of points
        
        This list of points have to be in order.
        Those points will be linked in order to create the surface.
        
        A surface have two following points with the same height, this segment define the landing area.
        
        Fields :
            * lands : list[Segment]
            * length : float
        """
        self.lands = []
        self.length = 0
        for i in range(len(points)-1):
            land = Segment(points[i], points[i+1])
            self.lands.append(land)
            self.length += land.lenght()
            if points[i][1] == points[i+1][1]:
                self.landing_area = land
                
    def is_landing_area(self, segment):
        """Check if a land his the landing area"""
        if segment:
            return segment.point_a.y == segment.point_b.y
        return False
    

    def they_collide(self, trajectory: Segment) -> bool:
        """Check if a segment intersect with the surface"""
        for land in self.lands:
            if trajectory.collision(land):
                return land
        return None
    
    def get_points(self):
        """Return the points of the surface"""
        yield self.lands[0].point_a
        for segment in self.lands:
            yield segment.point_b
    

