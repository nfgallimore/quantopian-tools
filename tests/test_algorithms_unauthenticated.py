# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import datetime

from quantopian import algorithms


def test_get_algorithm_ids(unauthenticated_browser):
    assert algorithms.get_algorithm_ids()


def test_get_algorithm(unauthenticated_browser):
    ids = algorithms.get_algorithm_ids()
    assert len(ids) > 1
    assert sorted(algorithms.get_algorithm(ids[-1]).keys()) == ['code', 'id', 'title']


def test_save_algorithm(unauthenticated_browser):
    ids = algorithms.get_algorithm_ids()
    assert len(ids) > 1
    algo_id = ids[-1]
    algo = algorithms.get_algorithm(algo_id)
    assert sorted(algo.keys()) == ['code', 'id', 'title']

    algo['title'] = 'Hello World Algorithm ({})'.format(datetime.datetime.now().isoformat())
    assert algorithms.save_algorithm(algo)

    assert algorithms.get_algorithm(algo_id) == algo


def test_new_algorithm(unauthenticated_browser):
    title = 'Test ({})'.format(datetime.datetime.now().isoformat())
    algorithm_id = algorithms.new_algorithm(title)
    algorithm = algorithms.get_algorithm(algorithm_id)
    assert algorithm['title'] == title
    assert algorithms.delete_algorithm(algorithm)
