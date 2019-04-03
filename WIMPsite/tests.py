from django.test import TestCase
from WIMPsite.color_match import get_delta_e
from math import sqrt

# Create your tests here.


class ColorMatchTests(TestCase):
    def setUp(self):
        pass

    def test_color_match(self):

        color_range = [(209, 187, 76), (154, 159, 83), (108, 134, 94), (100, 127, 101), (81, 101, 96)]

        color2 = (112, 99, 87)

        correct_shifts = []

        for r in range(0, 255):
            for g in range(0, 255):
                for b in range(0, 255):

                    color_match = color_range[0]
                    min_distance = get_delta_e(color_match, color2)
                    color_match_ndx = 0
                    ndx = 0
                    for color in color_range[1:]:
                        color2 = max(color2[0] + 112, 0), max(color2[1] + 135, 0), max(color2[2] + 120, 0)
                        dist = get_delta_e(color, color2)

                        if dist < min_distance:
                            color_match = color
                            min_distance = dist
                            color_match_ndx = ndx

                        ndx += 1

                    if color_match_ndx == 1:
                        print(r, g, b)
                        correct_shifts.append((r, g, b))

        print(correct_shifts)
