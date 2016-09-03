# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import os

import pytest

from quantopian import session, settings

@pytest.fixture
def unauthenticated_browser():
    if session.browser.is_authenticated:
        assert session.browser.logout()


@pytest.fixture
def authenticated_browser():
    assert settings.QUANTOPIAN_EMAIL
    assert settings.QUANTOPIAN_PWD
    if not session.browser.is_authenticated:
        assert session.browser.login()  # Environment vars contain email and password


@pytest.fixture
def sample_mean_reversion_alg_code():
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'sample_mean_reversion_alg.py')) as alg:
        return alg.read()
