# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from quantopian import securities


def test_lookup_sid():
    assert securities.lookup_sid(45149) == {
        'sid': 45149,
        'symbol': 'HTBX',
        'name': 'HEAT BIOLOGICS INC'
    }
    assert securities.lookup_sid(1111111) is None
