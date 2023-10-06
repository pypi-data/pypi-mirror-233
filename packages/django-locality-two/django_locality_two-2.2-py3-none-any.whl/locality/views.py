from django.core import serializers
from django.http import HttpResponse

from locality.models import Country, Territory


def countries(request, country=None, format="json"):
    if country:
        data = [Country.objects.find(country)]
    else:
        data = Country.objects.all()
    return HttpResponse(serializers.serialize(format, data), content_type=f"application/{format}; charset=utf-8")


def territories(request, country=None, format="json"):
    if country:
        data = Territory.objects.by_country(country)
    else:
        data = Territory.objects.all()
    return HttpResponse(serializers.serialize(format, data), content_type=f"application/{format}; charset=utf-8")
