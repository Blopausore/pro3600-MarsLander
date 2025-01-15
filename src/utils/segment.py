import numpy as np
import numba as nb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.point import Point



class Segment:
    """Define a segment in space
        point_a : Point
        point_b : Point
    """
    @staticmethod
    def ccw(A : Point, B : Point, C : Point) -> bool:
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    def __init__(self, point_a : Point, point_b : Point ):
        if not isinstance(point_a, Point):
            point_a = Point(*point_a)
        if not isinstance(point_b, Point):
            point_b = Point(*point_b)
        self.point_a = point_a
        self.point_b = point_b


    def __getitem__(self, key):
        if key == 0:
            return self.point_a
        elif key == 1:
            return self.point_b
        else:
            raise IndexError("Index out of range")
        
    def __contains__(self, point : Point) -> bool:
        """Look if the point is in one of the extremity segment"""
        return point == self.point_a or point == self.point_b
    
    def __iter__(self):
        return iter([self.point_a, self.point_b])

    def __next__(self):
        return next(self)

    def __eq__(self, other) -> bool:
        return self.point_a == other[0] and self.point_b == other[1]

    def __str__(self) -> str:
        return f"{self.point_a} | {self.point_b}"

    def lenght(self) -> float:
        return self.point_a.distance(self.point_b)

    def collision(self, other) -> bool:
        """Look if the segment self and [other.point_a, other.point_b] segment's intersect
        It is import to notice that it does not consider the case where an extremity of a segment is in the other segment, it return False in this case
        And it does not consider the case where the segment are colinear, it return False in this case
        """
        return Segment.ccw(self.point_a, other.point_a ,other.point_b) != Segment.ccw(self.point_b, other.point_a, other.point_b) \
            and Segment.ccw(self.point_a, self.point_b, other.point_a) != Segment.ccw(self.point_a, self.point_b, other.point_b)
    
    