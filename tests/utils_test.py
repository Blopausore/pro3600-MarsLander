import unittest


from src.utils.point import Point   
from src.utils.segment import Segment

class TestUtils(unittest.TestCase):

    def test_point(self):
        point = Point(1, 2)
        # Test constructor
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)
        
        self.assertEqual(point[0], 1)
        self.assertEqual(point[1], 2)
        self.assertEqual(point[0], point.x)
        self.assertEqual(point[1], point.y)
        
        # Test getter
        self.assertEqual(point, Point(1, 2))
        self.assertEqual(point, [1, 2])
        self.assertEqual(point, (1, 2))

        self.assertEqual(point.distance(Point(3, 4)), 2.8284271247461903)

    def test_segment(self):
        segment = Segment([1, 2], [3, 4])
        # Test constructor
        self.assertEqual(segment.point_a, Point(1, 2))
        self.assertEqual(segment.point_b, Point(3, 4))
        self.assertEqual(segment, Segment([1, 2], [3, 4]))
        self.assertEqual(segment, [Point(1, 2), Point(3, 4)])

        # Test getter
        self.assertEqual(segment[0], Point(1, 2))   
        self.assertEqual(segment[0], segment.point_a)
        self.assertEqual(segment[0], (1, 2))
        self.assertEqual(segment[0], [1, 2])

        self.assertEqual(segment[1], Point(3, 4))
        self.assertEqual(segment[1], segment.point_b)
        self.assertEqual(segment[1], (3, 4))
        self.assertEqual(segment[1], [3, 4])

        # Test contains
         
        self.assertTrue(Point(1, 2) in segment)
        self.assertTrue(Point(3, 4) in segment)
        self.assertFalse(Point(1, 3) in segment)
        self.assertFalse(Point(3, 2) in segment)
        
        # Test lenght
        self.assertEqual(segment.lenght(), 2.8284271247461903)
        self.assertEqual(segment.lenght(), segment.point_a.distance(segment.point_b))   
        self.assertEqual(segment.lenght(), segment.point_b.distance(segment.point_a))
        self.assertNotEqual(segment.lenght(), 2)

        # Collision test
        self.assertTrue(segment.collision(Segment([2, 2], [2, 4])))
        self.assertFalse(segment.collision(Segment([2, 2], [2, 3])))
        self.assertFalse(segment.collision(Segment([2, 2], [2, 1])))
        
        ## Colinear case
        self.assertFalse(segment.collision(Segment([1, 2], [3, 4])))
        self.assertFalse(segment.collision(Segment([2, 1], [4, 3])))