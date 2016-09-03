# -*- coding: utf-8 -*-
"""
Sessions handle the details of authentication and transporting requests.
"""
from __future__ import print_function, absolute_import, division, unicode_literals

import json


class RequestError(Exception):
    def __init__(self, message, response):
        Exception.__init__(self, message)

        self.response = response

    def __str__(self):
        return "%d Error: %s" % (self.response.status_code, Exception.__str__(self))


class ResponseValidationError(Exception):
    def __init__(self, method, url, body, errors):
        self.method = method
        self.url = url
        self.body = body
        self.errors = errors

    def __str__(self):
        return "{} {}\nbody={}\nerrors={}".format(self.method,
                                                  self.url,
                                                  json.dumps(self.body, sort_keys=True, indent=4),
                                                  json.dumps(self.errors, sort_keys=True, indent=4))


class SchemaValidationError(Exception):
    def __init__(self, data, schema, errors):
        self.data = data
        self.schema = schema
        self.errors = errors

    def __str__(self):
        return "\ndata={}\nschema={}\nerrors={}".format(json.dumps(self.data, sort_keys=True, indent=4),
                                                        json.dumps(self.schema, sort_keys=True, indent=4),
                                                        json.dumps(self.errors, sort_keys=True, indent=4))


class AlreadyLoggedIn(Exception):
    pass


class NotLoggedIn(Exception):
    pass
