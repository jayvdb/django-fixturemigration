from optparse import make_option

from django.apps import apps
from django.core.management.commands.makemigrations import (
    Command as MigrationCommand)
from django.db.migrations import Migration
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.questioner import InteractiveMigrationQuestioner
from django.db.migrations.state import ProjectState

from fixturemigration.operations import LoadFixtureMigration


class Command(MigrationCommand):
    help = "Creates new fixture migration in app."
    option_list = MigrationCommand.option_list + (
        make_option('-f', '--fixture', dest='fixture_name',
            help="Name of the fixture to load"),
        )
    args = 'app_label'

    def handle(self, app_label, **options):

        self.verbosity = options.get('verbosity')
        fixture_name = options.get('fixture_name')
        self.dry_run = False

        # Make sure the app they asked for exists
        try:
            apps.get_app_config(app_label)
        except LookupError:
            self.stderr.write(
                "App '%s' could not be found. Is it in INSTALLED_APPS?" %
                app_label)

        # Load the current graph state. Pass in None for the connection so
        # the loader doesn't try to resolve replaced migrations from DB.
        loader = MigrationLoader(None, ignore_no_migrations=True)

        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            InteractiveMigrationQuestioner(specified_apps=[app_label]),
            )

        migration = Migration("custom", app_label)
        migration.operations.append(LoadFixtureMigration(fixture_name))
        migration.dependencies += loader.graph.nodes.keys()

        changes = {
            app_label: [migration]
        }
        changes = autodetector.arrange_for_graph(
            changes=changes,
            graph=loader.graph,
        )
        self.write_migration_files(changes)
        return
