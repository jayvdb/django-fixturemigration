fixturemigration
================

A django app that allows you to load a fixture in a particular migration state.

##What's the problem?

If your django apps use fixtures then you already know that initial loading of fixtures has been deprecated since django version 1.7. If you want to load initial data you must use a data migration.

Using a [https://docs.djangoproject.com/en/1.8/topics/migrations/#data-migrations]data migration is quite easy, you can add a RunPython migration that calls a function like:

    def load_data(apps, schema_editor):
        Book = apps.get_model('library', 'Book')
        Book.objects.bulk_create([
            Book(name='The Litte Prince'),
            Book(name='The Ingenious Gentleman Don Quixote of La Mancha'),
        ])

That works great but if you need to create many objects it could be a pain to write this function. Some people try to load a full fixture file from a migration by doing a RunPython migration with the following code:

    def load_data(apps, schema_editor):
        call_command('loaddata', 'books_data.json')

Well, that seems to work but it has a serious problem. If your models continue evolving you will add more schema migrations and everything will seem to work right unless you try to migrate from scratch.

When you arrive to the data migration the loaddata command will try to deserialize the objects in your fixture using the current code in your models but currently you are half way applying migrations and your old
fixture is not compatible with your models. Then you have to remove the data migration, apply all the migrations, update your old fixture to the new changes and load it manually.

Si finally you'll end mantaining a fixture file and loading it manually after all migrations are applied.

##What's the solution?

Well, if you really want to load a fixture in a migration step then you could use fixturemigration. It creates a migration step that will load any fixture using the current migration state instead of getting the final models.

Installation
============

1.  Install fixturemigration from PyPI

        $ pip install django-fixturemigration

2.  Edit your project's `settings.py`:

        INSTALLED_APPS = (
            ...
            'fixturemigration'
        )

Instructions to use
===================

1.  Create your fixture like you always do, right now fixturemigration require that the fixture file will be in json format

        $ ./manage.py dumpdata --format=json --indent=4 app1 app2 > aap1/fixtures/20150723_data.json

    We have entered the data in the name but you can use any name you want.

2.  Add a special migration and tell it to load this fixture

        $ ./manage.py make_fixturemigration app1 --fixture 20150723_data.json

    Note that you need one app to store your new migration. The new migration will have dependencies with the latest migration of each app so when it load the fixture the state will be the same that when it was created.
