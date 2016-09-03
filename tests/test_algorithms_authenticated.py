# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import datetime

from quantopian import algorithms


def test_get_algorithm_ids(authenticated_browser):
    assert algorithms.get_algorithm_ids()


def test_get_algorithm(authenticated_browser):
    ids = algorithms.get_algorithm_ids()
    assert len(ids) > 1
    assert sorted(algorithms.get_algorithm(ids[-1]).keys()) == ['code', 'id', 'title']


def test_save_algorithm(authenticated_browser):
    ids = algorithms.get_algorithm_ids()
    assert len(ids) > 1
    algo_id = ids[-1]
    algo = algorithms.get_algorithm(algo_id)
    assert sorted(algo.keys()) == ['code', 'id', 'title']

    algo['title'] = 'Hello World Algorithm ({})'.format(datetime.datetime.now().isoformat())
    assert algorithms.save_algorithm(algo)

    assert algorithms.get_algorithm(algo_id) == algo


def test_new_algorithm(authenticated_browser):
    title = 'Test ({})'.format(datetime.datetime.now().isoformat())
    algorithm_id = algorithms.new_algorithm(title)
    algorithm = algorithms.get_algorithm(algorithm_id)
    assert algorithm['title'] == title
    assert algorithms.delete_algorithm(algorithm)


def test_validate_algorithm_success(authenticated_browser):
    algorithm = {
        'id': '57b11da5187a9054fb00041e',
        'code': "def initialize(context):    pass\n"
    }
    assert algorithms.validate_algorithm(algorithm,
                                         start_date=datetime.date(2016, 1, 1),
                                         end_date=datetime.date(2016, 1, 2)) == (True, [
        {
            'errorcode': None,
            'extra': {},
            'line': None,
            'name': 'Tier1.test_has_before_trading_start',
            'offset': None,
            'passed': True,
            'trace': None,
            'type': 'unit'
        },
        {
            'errorcode': None,
            'extra': {},
            'line': None,
            'name': 'Tier1.test_has_handle_data',
            'offset': None,
            'passed': True,
            'trace': None,
            'type': 'unit'
        },
        {
            'errorcode': None,
            'extra': {},
            'line': None,
            'name': 'Tier1.test_has_initialize_method',
            'offset': None,
            'passed': True,
            'trace': None,
            'type': 'unit'
        }
    ])


def test_validate_algorithm_failure(authenticated_browser):
    algorithm = {
        'id': '57b11da5187a9054fb00041e',
        'code': "def foo(context):    pass\n"
    }
    assert algorithms.validate_algorithm(algorithm,
                                         start_date=datetime.date(2016, 1, 1),
                                         end_date=datetime.date(2016, 1, 2)) == (False, [
        {
            'errorcode': None,
            'extra': {},
            'line': None,
            'name': 'Tier1.test_has_before_trading_start',
            'offset': None,
            'passed': True,
            'trace': None,
            'type': 'unit'
        },
        {
            'errorcode': None,
            'extra': {},
            'line': None,
            'name': 'Tier1.test_has_handle_data',
            'offset': None,
            'passed': True,
            'trace': None,
            'type': 'unit'
        },
        {
            'errorcode': 14,
            'extra': {'reason': 'None is not callable', 'type': 'NotCallable'},
            'line': None,
            'name': 'Tier1.test_has_initialize_method',
            'offset': None,
            'passed': False,
            'trace': 'InvalidInitializeMethod: 0014 None is not callable\n',
            'type': 'unit'
        }])
