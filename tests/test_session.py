# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from quantopian import session


def test_login_success():
    assert session.QBrowser().login()  # Environment vars contain email and password


def test_login_failure():
    assert not session.QBrowser().login('foo', 'bar')
