# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import datetime

from quantopian import algorithms, backtests


def test_run_backtest(unauthenticated_browser, sample_mean_reversion_alg_code):
    title = 'Backtest Test ({})'.format(datetime.datetime.now().isoformat())
    algorithm_id = algorithms.new_algorithm(title)
    algorithm = algorithms.get_algorithm(algorithm_id)
    algorithm['code'] = sample_mean_reversion_alg_code
    assert algorithms.save_algorithm(algorithm)

    results = list(backtests.run_backtest(algorithm,
                                          start_date=datetime.date(2016, 1, 1),
                                          end_date=datetime.date(2016, 2, 1),
                                          capital_base=1000000, data_frequency='minute'))
    assert algorithms.delete_algorithm(algorithm)
    print(results)
