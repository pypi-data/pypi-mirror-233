from django.contrib import admin

from .models import Country, Territory


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "iso2",
        "iso3",
        "name",
    )


class TerritoryAdmin(admin.ModelAdmin):
    list_display = (
        "abbr",
        "country",
        "name",
    )


admin.site.register(Country, CountryAdmin)
admin.site.register(Territory, TerritoryAdmin)
