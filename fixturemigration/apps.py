from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FixtureMigrationConfig(AppConfig):
    name = 'fixturemigration'
    verbose_name = _(u'Fixture migration')
