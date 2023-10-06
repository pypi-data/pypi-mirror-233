from django.db import models
from django.http import Http404


class CountryManager(models.Manager):
    def find(self, identifier):
        try:
            id = int(identifier)
            return self.get(pk=id)
        except ValueError:
            return self.get(
                models.Q(iso2__iexact=identifier)
                | models.Q(iso3__iexact=identifier)
                | models.Q(name__iexact=identifier)
            )

    def find_or_404(self, identifier):
        try:
            return self.find(identifier)
        except:
            raise Http404


class TerritoryManager(models.Manager):
    def by_country(self, country=None):
        if country:
            try:
                country_id = int(country)
                return self.filter(country__id=country_id)
            except ValueError:
                return self.filter(
                    models.Q(country__iso2__iexact=country)
                    | models.Q(country__iso3__iexact=country)
                    | models.Q(country__name__iexact=country)
                )

        return self.all()

    def by_country_iso2(self, iso2=None):
        if iso2:
            return self.filter(country__iso2__iexact=iso2).order_by("abbr")
        return self.all()

    def by_country_iso3(self, iso3=None):
        if iso3:
            return self.filter(country__iso3__iexact=iso3).order_by("abbr")
        return self.all()

    def by_country_id(self, country_id=None):
        if country_id:
            return self.filter(country__id=country_id).order_by("abbr")
        return self.all()
