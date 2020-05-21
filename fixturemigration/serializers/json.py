from __future__ import unicode_literals, absolute_import, unicode_literals

from django.conf import settings
from django.core.serializers import base
from django.core.serializers.base import DeserializationError
from django.core.serializers.pyyaml import Deserializer, Serializer
from django.db import DEFAULT_DB_ALIAS, models
from django.utils import six
from django.utils.encoding import force_text

import yaml
import sys

from fixturemigration import is_django_1_7


def StatePythonDeserializer(object_list, **options):
    """
    Deserialize simple Python objects back into Django ORM instances.

    It's expected that you pass the Python objects themselves (instead of a
    stream or a string) to the constructor
    """
    db = options.pop('using', DEFAULT_DB_ALIAS)
    ignore = options.pop('ignorenonexistent', False)
    state = options.get('state')

    for d in object_list:
        # Look up the model and starting build a dict of data for it.
        try:
            Model = _get_model(d["model"], state)
        except base.DeserializationError:
            if ignore:
                continue
            else:
                raise
        data = {}
        if 'pk' in d:
            data[Model._meta.pk.attname] = Model._meta.pk.to_python(d.get("pk", None))
        m2m_data = {}
        if is_django_1_7:
            field_names = Model._meta.get_all_field_names()
        else:
            field_names = {f.name for f in Model._meta.get_fields()}

        # Handle each field
        for (field_name, field_value) in six.iteritems(d["fields"]):

            if ignore and field_name not in field_names:
                # skip fields no longer on model
                continue

            if isinstance(field_value, str):
                field_value = force_text(
                    field_value, options.get("encoding", settings.DEFAULT_CHARSET), strings_only=True
                )

            field = Model._meta.get_field(field_name)

            # Handle M2M relations
            if hasattr(field, 'rel') and field.rel and isinstance(field.rel, models.ManyToManyRel):
                if hasattr(field.rel.to._default_manager, 'get_by_natural_key'):
                    def m2m_convert(value):
                        if hasattr(value, '__iter__') and not isinstance(value, six.text_type):
                            return field.rel.to._default_manager.db_manager(db).get_by_natural_key(*value).pk
                        else:
                            return force_text(field.rel.to._meta.pk.to_python(value), strings_only=True)
                else:
                    m2m_convert = lambda v: force_text(field.rel.to._meta.pk.to_python(v), strings_only=True)
                m2m_data[field.name] = [m2m_convert(pk) for pk in field_value]

            # Handle FK fields
            elif hasattr(field, 'rel') and field.rel and isinstance(field.rel, models.ManyToOneRel):
                if field_value is not None:
                    if hasattr(field.rel.to._default_manager, 'get_by_natural_key'):
                        if hasattr(field_value, '__iter__') and not isinstance(field_value, six.text_type):
                            obj = field.rel.to._default_manager.db_manager(db).get_by_natural_key(*field_value)
                            value = getattr(obj, field.rel.field_name)
                            # If this is a natural foreign key to an object that
                            # has a FK/O2O as the foreign key, use the FK value
                            if field.rel.to._meta.pk.rel:
                                value = value.pk
                        else:
                            value = field.rel.to._meta.get_field(field.rel.field_name).to_python(field_value)
                        data[field.attname] = value
                    else:
                        data[field.attname] = field.rel.to._meta.get_field(field.rel.field_name).to_python(field_value)
                else:
                    data[field.attname] = None

            # Handle all other fields
            else:
                data[field.name] = field.to_python(field_value)

        obj = base.build_instance(Model, data, db)
        yield base.DeserializedObject(obj, m2m_data)


def _get_model(model_identifier, state):
    """
    Helper to look up a model from an "app_label.model_name" string.
    """
    try:
        if is_django_1_7:
            apps = state.render()
        else:
            apps = state.apps
        return apps.get_model(model_identifier)
    except (LookupError, TypeError):
        raise base.DeserializationError("Invalid model identifier: '%s'" % model_identifier)
