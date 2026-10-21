"""Runs without VectorCraft or an API key."""
import math
import unittest
from geometry_core import triangle_points, verify_selected_target, triangle_tool_arguments

class GeometryTests(unittest.TestCase):
    def test_three_equal_sides(self):
        p = triangle_points()
        self.assertEqual(len(p), 3)
        sides = [math.dist(p[i], p[(i+1)%3]) for i in range(3)]
        self.assertLess(max(sides)-min(sides), 0.003)
    def test_invalid_geometry_rejected(self):
        for r in (0, -2, float('nan'), float('inf')):
            with self.assertRaises(ValueError): triangle_points(radius=r)
    def test_native_draw_path_contract(self):
        args = triangle_tool_arguments()
        self.assertTrue(args["closed"])
        self.assertEqual(len(args["points"]), 3)
    def test_target_selection_guard(self):
        verify_selected_target({"selection":[{"id":17}]}, 17)
        for wrong in ({"selection":[{"id":18}]}, {"selection":[17,18]}, {}, {"selection":[]}):
            with self.assertRaises(ValueError): verify_selected_target(wrong, 17)

if __name__ == "__main__":
    unittest.main()
