from django import forms
from django.core.validators import EMPTY_VALUES
from django.db.models import Q
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _

from locality.models import Country


class CountrySelectField(forms.Field):
    """
    A form field that validates its input to iso2 or iso3 abbreviations
    or the name of countries in the database.
    """

    default_error_messages = {
        "invalid": _("Select a Country."),
    }

    def clean(self, value):
        super().clean(value)

        if value in EMPTY_VALUES:
            return ""

        country = Country.objects.filter(Q(name__iexact=value) | Q(iso2__iexact=value) | Q(iso3__iexact=value))

        if not country.exists():
            raise forms.ValidationError(self.default_error_messages["invalid"])

        return country[0]


class CountrySelectWidget(forms.Select):
    """
    A select widget that uses all countries in alphabetical order as its choices.
    """

    def __init__(self, attrs=None, choices=None):
        choices = Country.objects.values_list("iso2", "name").order_by("name")
        super().__init__(attrs=attrs, choices=choices)
