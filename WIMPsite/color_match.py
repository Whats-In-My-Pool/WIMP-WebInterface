from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def get_delta_e(color1, color2):
    color1_rgb = sRGBColor(color1[0] / 255.0, color1[1] / 255.0, color1[2] / 255.0)
    color2_rgb = sRGBColor(color2[0] / 255.0, color2[1] / 255.0, color2[2] / 255.0)

    color1_lab = convert_color(color1_rgb, LabColor)

    color2_lab = convert_color(color2_rgb, LabColor)

    return delta_e_cie2000(color1_lab, color2_lab)
