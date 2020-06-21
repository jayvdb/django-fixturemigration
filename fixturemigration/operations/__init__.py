from django.apps import apps as global_apps
from django.db import router
from django.db.migrations.operations.base import Operation
from django.core.management import call_command
from django.core.management.sql import emit_post_migrate_signal
from django.contrib.auth.management import create_permissions

class LoadFixtureMigration(Operation):

    def __init__(self, fixturemigration, use_content_types=False, permission_apps=None):
        super(LoadFixtureMigration, self).__init__()
        self.fixturemigration = fixturemigration
        self.use_content_types = use_content_types
        self.permission_apps = permission_apps

    def reversible(self):
        return True

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            if self.use_content_types:
                emit_post_migrate_signal(2, False, 'default')

            if self.permission_apps:
                for permission_app_label in self.permission_apps:
                    permission_app = global_apps.get_app_config(
                        permission_app_label)
                    create_permissions(
                        permission_app, verbosity=2, interactive=False)

            call_command('load_fixturemigration', self.fixturemigration, state=from_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def state_forwards(self, app_label, state):
        pass
