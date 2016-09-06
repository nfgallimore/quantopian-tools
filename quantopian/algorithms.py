# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import re

from quantopian import schema
from quantopian.exceptions import RequestError, ResponseValidationError
from quantopian.helpers import build_url
from quantopian.session import browser


def get_algorithm_ids():
    response = browser.get(build_url('algorithms'))
    if not response.ok:
        raise RequestError('failed to get algorithm ids', response)

    rows = response.soup.find_all('tr', attrs={'data-algo-id': re.compile(r'^[a-fA-F\d]{24}$')})
    return [row.attrs['data-algo-id'] for row in rows]


def get_algorithm(algorithm_id):
    response = browser.get(build_url('algorithms', algorithm_id))
    if not response.ok:
        raise RequestError('failed to get algorithm %s' % algorithm_id, response)

    title = response.soup.find(lambda tag: 'value' in tag.attrs, attrs={'name': 'algorithm[title]'})
    code = response.soup.find(attrs={'name': 'algorithm[code]'})
    if not title or not code:
        if not response.ok:
            raise RequestError('failed to find code and title for algorithm %s' % algorithm_id, response)

    return {
        'id': algorithm_id,
        'title': title.attrs['value'],
        'code': code.text.lstrip()
    }


def save_algorithm(algorithm):
    url = build_url('algorithms', algorithm['id'], 'autosave')
    headers = {
        'x-csrf-token': browser.get_csrf_token(build_url('algorithms', algorithm['id'])),
        'x-requested-with': 'XMLHttpRequest'
    }
    response = browser.post(url, data=algorithm, headers=headers)
    if not response.ok:
        raise RequestError('failed to save algorithm %s' % algorithm['id'], response)

    valid, data_or_errors = schema.validate(response.json(), {
        "status": schema.string(required=True, nullable=False)
    }, allow_unknown=True)
    if not valid:
        raise ResponseValidationError('POST', url, algorithm, data_or_errors)

    return data_or_errors['status'].lower() == 'ok'


def new_algorithm(title):
    url = build_url('algorithms')
    headers = {
        'x-csrf-token': browser.get_csrf_token(build_url('algorithms')),
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {'title': title}
    response = browser.post(url, data=data, headers=headers)
    if not response.ok:
        raise RequestError('failed to create a new algorithm', response)

    valid, data_or_errors = schema.validate(response.json(), {
        "to": schema.string(required=True, nullable=False, regex=r'^/algorithms/[a-fA-F\d]{24}$')
    }, allow_unknown=True)
    if not valid:
        raise ResponseValidationError('POST', url, data, data_or_errors)

    return data_or_errors['to'].lower().replace('/algorithms/', '')


def delete_algorithm(algorithm):
    url = build_url('algorithms', 'delete')
    headers = {
        'x-csrf-token': browser.get_csrf_token(build_url('algorithms')),
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {'ids[]': algorithm['id']}
    response = browser.post(url, data=data, headers=headers)
    return response.ok


def validate_algorithm(algorithm, start_date=None, end_date=None, data_frequency='minute'):
    assert browser.is_authenticated, "You must be authenticated to validate algorithms"
    url = build_url('algorithms', algorithm['id'], 'validate')
    data = {
        'code': algorithm['code'],
        'algo_id': algorithm['id'],
        'data_frequency': data_frequency,
        'start_date_str': start_date.strftime('%m/%d/%Y'),
        'end_date_str': end_date.strftime('%m/%d/%Y')
    }
    headers = {
        'x-csrf-token': browser.get_csrf_token(build_url('algorithms', algorithm['id'])),
        'x-requested-with': 'XMLHttpRequest'
    }
    response = browser.post(url, data=data, headers=headers)
    if not response.ok:
        raise RequestError('validate algorithm request failed', response)

    valid, data_or_errors = schema.validate(response.json(), {
        "data": schema.dictionary(required=True, schema={
            "test_results": schema.list_(required=True, schema=schema.dictionary(schema={
                "passed": schema.boolean(required=True, nullable=False)
            }))
        })
    }, allow_unknown=True)
    if not valid:
        raise ResponseValidationError('POST', url, data, data_or_errors)

    test_results = data_or_errors['data']['test_results']

    return all(result['passed'] for result in test_results), test_results
