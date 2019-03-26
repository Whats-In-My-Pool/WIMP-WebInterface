from django.test import TestCase
from WIMPsite.color_match import get_delta_e

# Create your tests here.


class ColorMatchTests(TestCase):
    def setUp(self):
        pass

    def test_color_match(self):
        color1 = (51, 16, 22)
        color2 = (39, 15, 20)

        print(get_delta_e(color1, color2))
