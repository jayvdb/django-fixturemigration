from django.db import router
from django.db.migrations.operations.base import Operation
from django.core.management import call_command


class LoadFixtureMigration(Operation):

    def __init__(self, fixturemigration):
        self.fixturemigration = fixturemigration

    def reversible(self):
        return True

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            call_command('load_fixturemigration', self.fixturemigration, state=from_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def state_forwards(self, app_label, state):
        pass
