from django import template
from django.urls import reverse

register = template.Library()

navbar_options = [
    ("Home", reverse("Home")),
    ("Testing Strips", reverse("Testing Strips")),
    ("Scheduled Tests", reverse("Scheduled Tests"))
]

option_format = '<li class="nav-item{}"> <a class="nav-link" href="{}">{} </a> </li>'


@register.simple_tag
def get_navbar(page):
    navbar = ""

    for option in navbar_options:
        if page == option[0]:
            active = ' active'
        else:
            active = ''

        navbar += option_format.format(active, option[1], option[0])

    return navbar