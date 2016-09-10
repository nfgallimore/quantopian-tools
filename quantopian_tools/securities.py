# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from quantopian_tools import schema, session
from quantopian_tools.exceptions import RequestError, ResponseValidationError
from quantopian_tools.helpers import build_url


def lookup_sid(sid):
    """Lookup a security by id.

    >>> lookup_sid(45149)
    {u'symbol': u'HTBX', u'name': u'HEAT BIOLOGICS INC', u'sid': 45149}
    >>> lookup_sid(1111111)  # Returns None of no security is found

    :param sid: Security id.
    :type sid: int
    :return: A dictionary containing the security's name, sid, and symbol or ``None`` if no security is found.
    :rtype: dict
    :raises quantopian_tools.exceptions.RequestError: If the request to the quantopian_tools server failed.
    :raises quantopian_tools.exceptions.ResponseValidationError: If the response from the quantopian_tools server is not
     of the format expected.
    """
    url = build_url('securities/', q=sid)
    headers = {
        'x-csrf-token': session.browser.get_csrf_token(build_url('algorithms')),
        'x-requested-with': 'XMLHttpRequest'
    }
    response = session.browser.get(url, headers=headers)
    if not response.ok:
        raise RequestError('failed to lookup sid %d' % sid, response)

    valid, data_or_errors = schema.validate(response.json(), {
        "data": schema.dictionary(
            required=True,
            nullable=False,
            schema={
                "matches": schema.list_(
                    required=True,
                    nullable=True,
                    coerce='falsey_to_none',
                    schema=schema.dictionary(
                        schema={
                            'name': schema.string(required=True, nullable=False, empty=False),
                            'sid': schema.integer(required=True, nullable=False, min=1),
                            'symbol': schema.string(required=True, nullable=False, empty=False)
                        }
                    )
                )
            }
        )
    }, allow_unknown=True)
    if not valid:
        raise ResponseValidationError('GET', url, None, data_or_errors)
    for security in data_or_errors['data']['matches'] or []:
        if security['sid'] == sid:
            return security
    return None
