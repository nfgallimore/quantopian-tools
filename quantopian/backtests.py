# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import json
from contextlib import closing

import attrdict
import websocket

from . import schema
from .exceptions import RequestError, ResponseValidationError
from .helpers import build_url
from .session import browser


def log_payload_schema():
    return {
        'count': schema.integer(required=True, nullable=False, min=0, rename='num_lines')
    }


def position_schema():
    return {
        'a': schema.number(required=True, nullable=False, rename='amount'),
        'cb': schema.number(required=True, nullable=False, rename='cost_basis'),
        's': schema.integer(required=True, nullable=False, min=0, rename='sid'),
        'ls': schema.number(required=True, nullable=False, rename='last_sale_price')
    }


def performance_schema():
    return {
        "be": schema.number(required=True, nullable=True, default=None, rename='beta'),
        "al": schema.number(required=True, nullable=True, default=None, rename='alpha'),
        "vo": schema.number(required=True, nullable=True, default=None, rename='volatility'),
        "bv": schema.number(required=True, nullable=True, default=None),  # , rename='bv'),  # TODO: Find actual name
        "pnl": schema.number(required=True, nullable=True, default=None),
        "br": schema.number(required=True, nullable=True, default=None, rename='benchmark_returns'),
        "in": schema.number(required=True, nullable=True, default=None, rename='information_ratio'),
        "cu": schema.number(required=True, nullable=True, default=None, rename='cushion'),
        "md": schema.number(required=True, nullable=True, default=None, rename='max_drawdown'),
        "ml": schema.number(required=True, nullable=True, default=None, rename='max_leverage'),
        "tr": schema.number(required=True, nullable=True, default=None, rename='total_returns'),
        "sh": schema.number(required=True, nullable=True, default=None, rename='sharpe'),
        "so": schema.number(required=True, nullable=True, default=None, rename='sorentino')
    }


def daily_result_schema():
    return {
        'o': schema.list_(required=True, nullable=True, default=None),  # , rename='o'),  # TODO: Find actual name
        'rv': schema.dictionary(required=True, nullable=True, default=None, rename='custom_data'),
        'd': schema.date_(required=True, nullable=True, min=0, default=None, rename='date',
                          coerce=('millis_timestamp', 'datetime_to_date')),
        'c': schema.dictionary(required=True, nullable=True, default=None, rename='performance',
                               schema=performance_schema()),
        'l': schema.number(required=True, nullable=True, default=None, rename='leverage'),
        'ec': schema.number(required=True, nullable=True, default=None, rename='equity_with_loan'),
        'p': schema.list_(required=True, nullable=True, default=None, rename='positions',
                          schema=schema.dictionary(schema=position_schema())),
        'pnl': schema.number(required=True, nullable=True, default=None),
        't': schema.list_(required=True, nullable=True, default=None),  # , rename='t'),  # TODO: Find actual name
        'cb': schema.number(required=True, nullable=True, default=None),  # , rename='t'),  # TODO: Find actual name
        'bm': schema.number(required=True, nullable=True, default=None)  # , rename='t')  # TODO: Find actual name
    }


def performance_payload_schema():
    return {
        'cursor': schema.integer(required=True, nullable=False),
        'pc': schema.number(required=True, nullable=False, rename='percent_complete'),
        'sa': schema.datetime_(required=True, nullable=False, min=0, rename='timestamp', coerce='millis_timestamp'),
        'daily': schema.dictionary(required=True, nullable=True, default=None, rename='daily_performance',
                                   coerce='first_item', schema=daily_result_schema())
    }


def stack_schema():
    return {
        'lineno': schema.integer(required=True, nullable=True, min=0),
        'line': schema.string(required=True, nullable=True, empty=True),
        'method': schema.string(required=True, nullable=True, empty=True),
        'filename': schema.string(required=True, nullable=True, empty=True)
    }

def exception_payload_schema():
    return {
        'date': schema.datetime_(required=True, nullable=False, min=0, rename='timestamp', coerce='millis_timestamp'),
        'message': schema.string(required=True, nullable=False),
        'name': schema.string(required=True, nullable=False),
        'stack': schema.list_(required=True, nullable=False, schema=stack_schema())
    }


def run_backtest(algorithm, start_date, end_date, capital_base, data_frequency='minute'):
    url = build_url('backtests', 'start_ide_backtest')
    headers = {
        'x-csrf-token': browser.get_csrf_token(build_url('algorithms', algorithm['id'])),
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        'algo_id': algorithm['id'],
        'code': algorithm['code'],
        'backtest_start_date_year': start_date.year,
        'backtest_start_date_month': start_date.month,
        'backtest_start_date_day': start_date.day,
        'backtest_end_date_year': end_date.year,
        'backtest_end_date_month': end_date.month,
        'backtest_end_date_day': end_date.day,
        'backtest_capital_base': capital_base,
        'backtest_data_frequency_value': data_frequency
    }
    response = browser.post(url, data=data, headers=headers)
    if not response.ok:
        raise RequestError('failed to start backtest', response)

    valid, data_or_errors = schema.validate(response.json(), {
        "data": schema.dictionary(required=True, schema={
            "ws_open_msg": schema.string(required=True, nullable=False, empty=False),
            "ws_url": schema.string(required=True, nullable=False, empty=False)
        })
    }, allow_unknown=True)
    if not valid:
        raise ResponseValidationError('POST', url, algorithm, data_or_errors)

    with closing(websocket.create_connection(data_or_errors['data']['ws_url'])) as ws:
        ws.send(json.dumps({
            'e': 'open',
            'p': {
                'a': data_or_errors['data']['ws_open_msg'],
                'cursor': 0,
                'include_txn': True
            }
        }))
        while True:
            msg = json.loads(ws.recv())
            if msg['e'] == 'log':
                yield attrdict.AttrDict(schema.validate(msg['p'], log_payload_schema(), raise_exc=True))

            elif msg['e'] == 'performance':
                yield attrdict.AttrDict(schema.validate(msg['p'], performance_payload_schema(), raise_exc=True))

            elif msg['e'] == 'risk_report':
                yield msg['p']

            elif msg['e'] == 'done':
                yield msg['p']
                break

            elif msg['e'] == 'exception':
                exc = schema.validate(msg['p'], exception_payload_schema(), raise_exc=True)
                trace = '\n'.join('  File "{}", line {}, in {}\n    {}'.format(s['filename'], s['lineno'], s['method'],
                                                                               s['line'])
                                  for s in exc['stack'])
                raise RuntimeError("Traceback (most recent call last):\n{}\n{}: {}".format(trace, exc['name'],
                                                                                           exc['message']))

            else:
                raise Exception("unknown event '{}'".format(msg['e']))
