from django.db import models
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _

from locality import managers


class Country(models.Model):
    iso2 = models.CharField(_("ISO 3166-1 Alpha 2 Name"), max_length=2, unique=True)
    iso3 = models.CharField(_("ISO 3166-1 Alpha 3 Name"), max_length=3, unique=True)
    name = models.CharField(_("Country Name"), max_length=128, unique=True)

    objects = managers.CountryManager()

    def __str__(self):
        return self.name

    @property
    def abbr(self):
        return self.iso2

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = (
            "iso2",
            "name",
        )


class Territory(models.Model):
    abbr = models.CharField(_("Territory Abbreviation"), max_length=10)
    name = models.CharField(_("Territory Name"), max_length=128)
    country = models.ForeignKey(Country, related_name="territories", on_delete=models.CASCADE)

    objects = managers.TerritoryManager()

    def __str__(self):
        return f"{self.name}, {self.country.name}"

    class Meta:
        verbose_name = _("Territory")
        verbose_name_plural = _("Territories")
        ordering = (
            "abbr",
            "name",
        )
