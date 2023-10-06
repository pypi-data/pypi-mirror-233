from django.contrib import admin


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from .views import countries, territories


admin.autodiscover()

urlpatterns = [
    re_path(r"^countries/(?:all/?)?$", countries, name="locality-countries"),
    re_path(r"^(?P<format>(?:json|xml|yaml))/countries/(?:all/?)?$", countries, name="locality-countries"),
    re_path(
        r"^country/(?P<country>(?:\d+|\w{2}|\w{3}))/?$",
        countries,
        name="locality-countries-find",
    ),
    re_path(
        r"^(?P<format>(?:json|xml|yaml))/country/(?P<country>(?:\d+|\w{2}|\w{3}))/?$",
        countries,
        name="locality-countries-find",
    ),
    re_path(r"^territories/(?:all/?)?$", territories, name="locality-territories"),
    re_path(r"^(?P<format>(?:json|xml|yaml))/territories/(?:all/?)?$", territories, name="locality-territories"),
    re_path(
        r"^(?P<format>(?:json|xml|yaml))/territories(?:/(?P<country>(?:\d+|\w{2}|\w{3}))/?)?$",
        territories,
        name="locality-territories-by-country",
    ),
    re_path(
        r"^territories(?:/(?P<country>(?:\d+|\w{2}|\w{3}))/?)?$",
        territories,
        name="locality-territories-by-country",
    ),
]
