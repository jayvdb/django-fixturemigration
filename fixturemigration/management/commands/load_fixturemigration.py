import os
import warnings

from django.core.management.base import CommandError
from django.core.management.commands.loaddata import (
    Command as LoadDataCommand, humanize)
from django.db import (
    DatabaseError, IntegrityError, router,
)
from django.utils.encoding import force_text

from fixturemigration import is_django_1_7
from fixturemigration.serializers.json import Deserializer


class Command(LoadDataCommand):

    def handle(self, *fixture_labels, **options):
        self.state = options.get('state')
        super(Command, self).handle(*fixture_labels, **options)

    def load_label(self, fixture_label):
        """
        Loads fixtures files for a given label.
        """
        for fixture_file, fixture_dir, fixture_name in (
                self.find_fixtures(fixture_label)):
            _, ser_fmt, cmp_fmt = self.parse_name(
                os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]
            fixture = open_method(fixture_file, mode)
            try:
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write(
                        "Installing %s fixture '%s' from %s." %
                        (ser_fmt, fixture_name, humanize(fixture_dir)))

                objects = Deserializer(
                    fixture, using=self.using, ignorenonexistent=self.ignore,
                    state=self.state)

                for obj in objects:
                    objects_in_fixture += 1
                    if is_django_1_7:
                        router_allow = router.allow_migrate
                    else:
                        router_allow = router.allow_migrate_model
                    if router_allow(
                            self.using, obj.object.__class__):
                        loaded_objects_in_fixture += 1
                        self.models.add(obj.object.__class__)
                        try:
                            obj.save(using=self.using)
                        except (DatabaseError, IntegrityError) as e:
                            e.args = (
                                "Could not load %(app_label)s."
                                "%(object_name)s(pk=%(pk)s): "
                                "%(error_msg)s" % {
                                    'app_label': obj.object._meta.app_label,
                                    'object_name': (
                                        obj.object._meta.object_name),
                                    'pk': obj.object.pk,
                                    'error_msg': force_text(e)
                                },)
                            raise

                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = (
                        "Problem installing fixture '%s': %s" %
                        (fixture_file, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture_name,
                    RuntimeWarning
                )
