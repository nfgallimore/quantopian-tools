# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import datetime

import cerberus
import six

from quantopian_tools.exceptions import SchemaValidationError


def validate(data, schema, raise_exc=False, **kwargs):
    validator = CustomValidator(schema, **kwargs)
    if not validator.validate(data):
        if raise_exc:
            raise SchemaValidationError(data, schema, validator.errors)
        return False, validator.errors
    if raise_exc:
        return validator.document
    return True, validator.document


class CustomValidator(cerberus.Validator):
    def _normalize_rename_handler(self, mapping, schema, field):
        """ {'oneof': [
                {'type': 'callable'},
                {'type': 'list',
                 'schema': {'oneof': [{'type': 'callable'},
                                      {'type': 'string'}]}},
                {'type': 'string'}
                ]} """
        if 'rename' in schema[field]:
            new_field = schema[field]['rename']
            schema[new_field] = schema[field]
            del schema[field]
            field = new_field
        super(CustomValidator, self)._normalize_rename_handler(mapping, schema, field)

    # Custom coerce functions
    def _normalize_coerce_millis_timestamp(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, int):
            return datetime.datetime.fromtimestamp(value / 1000.0)
        else:
            raise ValueError("cannot coerce type {} to a datetime".format(type(value).__name__))

    def _normalize_coerce_datetime_to_date(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        else:
            raise ValueError("cannot coerce type {} to a date".format(type(value).__name__))

    def _normalize_coerce_int(self, value):
        if value is None:
            return None
        elif isinstance(value, six.integer_types + six.string_types + (float,)):
            try:
                return int(value)
            except Exception as ex:
                raise ValueError(str(ex))
        raise ValueError("cannot coerce type {} to an int".format(type(value).__name__))

    def _normalize_coerce_number(self, value):
        if value is None:
            return None
        elif isinstance(value, six.integer_types + (float,)):
            return value
        elif isinstance(value, six.string_types):
            try:
                try:
                    return int(value)
                except ValueError:
                    return float(value)
            except Exception as ex:
                raise ValueError(str(ex))
        raise ValueError("cannot coerce type {} to a number".format(type(value).__name__))

    def _normalize_coerce_bool(self, value):
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        elif isinstance(value, six.string_types) and value.lower().strip() in ['true', '1']:
            return True
        elif isinstance(value, six.string_types) and value.lower().strip() in ['', 'false', '0']:
            return False
        raise ValueError("cannot coerce type {} to a bool".format(type(value).__name__))

    def _normalize_coerce_str(self, value):
        if value is None:
            return None
        if not isinstance(value, six.string_types):
            value = str(value)
        return value

    def _normalize_coerce_strip(self, value):
        if value is None:
            return None
        if hasattr(value, 'strip') and callable(getattr(value, 'strip')):
            return value.strip()
        raise ValueError("cannot coerce type {}; no strip() method found".format(type(value).__name__))

    def _normalize_coerce_filter_falsey(self, value):
        if value is None:
            return None
        if isinstance(value, (list, tuple, set)):
            return [item for item in value if item]
        raise ValueError("cannot coerce type {} to a list".format(type(value).__name__))

    def _normalize_coerce_falsey_to_none(self, value):
        return value or None

    def _normalize_coerce_first_item(self, value):
        if value is None:
            return None
        if isinstance(value, (list, tuple, set)):
            if len(value) >= 1:
                return value[0]
            return None
        raise ValueError("cannot get first item of type {}".format(type(value).__name__))


# Schema helpers

def string(required=False, nullable=False, empty=True, strip=False, **kwargs):
    schema = {
        'type': 'string',
        'required': required,
        'nullable': nullable,
        'empty': empty,
        'coerce': 'str' if not strip else ('str', 'strip')
    }
    schema.update(kwargs)
    return schema


def boolean(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'boolean',
        'required': required,
        'nullable': nullable,
        'coerce': 'bool'
    }
    schema.update(kwargs)
    return schema


def datetime_(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'datetime',
        'required': required,
        'nullable': nullable
    }
    schema.update(kwargs)
    return schema


def date_(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'date',
        'required': required,
        'nullable': nullable
    }
    schema.update(kwargs)
    return schema


def integer(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'integer',
        'required': required,
        'nullable': nullable,
        'coerce': 'int'
    }
    schema.update(kwargs)
    return schema


def number(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'number',
        'required': required,
        'nullable': nullable,
        'coerce': 'number'
    }
    schema.update(kwargs)
    return schema


def dictionary(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'dict',
        'required': required,
        'nullable': nullable
    }
    schema.update(kwargs)
    return schema


def list_(required=False, nullable=False, **kwargs):
    schema = {
        'type': 'list',
        'required': required,
        'nullable': nullable
    }
    schema.update(kwargs)
    return schema
