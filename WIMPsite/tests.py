from django.test import TestCase
from WIMPsite.color_match import get_delta_e
from math import sqrt

# Create your tests here.


class ColorMatchTests(TestCase):
    def setUp(self):
        pass

    def test_color_match(self):
        color_range = [(79, 101, 142), (86, 100, 148), (105, 102, 153), (128, 96, 138), (147, 99, 145)]

        color2 = (60, 69, 71)

        correct_shifts = []

        for color in color_range:
            print(get_delta_e(color, color2))

        print(correct_shifts)
