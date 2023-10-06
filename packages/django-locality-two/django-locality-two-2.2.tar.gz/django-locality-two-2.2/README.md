# django-locality-two

`django-locality-two` is a drop-in replacement for django-locality with modern python (3.5+) and django (1.11+) support,
and more tests.
Locality is a light collection of helpers for handling countries and
territories in Django.

Currently, it includes:

  * `locality.json`, a fixture with the world's countries and territories (if
    you notice any missing, [open an
    issue](https://github.com/dekomote/django-locality-two/issues) or [submit a pull
    request](https://github.com/dekomote/django-locality-two/compare/))
  * views returning serialized lists of countries and territories
  * simple form field and widget

## Installation

Install from the cheese shop

    pip install django-locality-two

OR

Install from GitHub with pip:

    pip install -e git+https://github.com/dekomote/django-locality-two.git#egg=django-locality-two==2.1.1

Then add `locality` to `INSTALLED_APPS` in your Django settings. To load the
included data, run:

    python manage.py loaddata locality

(or whichever equivalent method you use to run "manage.py" commands)

## Usage

List all countries:

    >>> from locality.models import Country
    >>> print Country.objects.all()
    [<Country: Andorra>, <Country: United Arab Emirates>,
    <Country: Antigua and Barbuda>, ...]

or list territories by country:

    >>> from locality.models import Country
    >>> for country in locality.models.Country.objects.all():
    >>>     print country.territories.all()
    ...
    [<Territory: Salta, Argentina>, <Territory: Buenos Aires, Argentina>,
    <Territory: Ciudad Autónoma de Buen os Aires, Argentina>, ...]

You can create your own models around countries and territories:

    class Address(models.Model):
        country = models.ForeignKey('locality.models.Country')
        territory = models.ForeignKey('locality.models.Territory')

## Bugs / TODO

Please report all bugs to the [GitHub issue
tracker](https://github.com/dekomote/django-locality-two/issues)
