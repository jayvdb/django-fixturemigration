from django import VERSION

is_django_1_7 = VERSION[:2] == (1, 7)
default_app_config = 'fixturemigration.apps.FixtureMigrationConfig'
