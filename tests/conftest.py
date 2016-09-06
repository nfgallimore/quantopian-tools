# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import os

import pytest

from quantopian import session, settings

_authenticated_browser = session.QBrowser()
_unauthenticated_browser = session.QBrowser()


@pytest.fixture
def unauthenticated_browser(monkeypatch):
    if _unauthenticated_browser.is_authenticated:
        assert _unauthenticated_browser.logout()
    monkeypatch.setattr('quantopian.session.browser', _unauthenticated_browser)
    return _unauthenticated_browser


@pytest.fixture
def authenticated_browser(monkeypatch):
    if not _authenticated_browser.is_authenticated:
        assert settings.QUANTOPIAN_EMAIL
        assert settings.QUANTOPIAN_PWD
        assert _authenticated_browser.login()  # Environment vars contain email and password
    monkeypatch.setattr('quantopian.session.browser', _authenticated_browser)
    return _authenticated_browser


@pytest.fixture
def sample_mean_reversion_alg_code():
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'sample_mean_reversion_alg.py')) as alg:
        return alg.read()
