from django.db import router
from django.db.migrations.operations.base import Operation
from django.core.management import call_command
from django.core.management.sql import emit_post_migrate_signal


class LoadFixtureMigration(Operation):

    def __init__(self, fixturemigration):
        super(LoadFixtureMigration, self).__init__()
        self.fixturemigration = fixturemigration

    def reversible(self):
        return True

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            emit_post_migrate_signal(2, False, 'default')
            call_command('load_fixturemigration', self.fixturemigration, state=from_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def state_forwards(self, app_label, state):
        pass
