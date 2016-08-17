# -*- coding: utf-8 -*-
import re

import semantic_version
import pytest
import validators
from datetime import datetime

import quantopian


def test_valid_pkg_name():
    assert quantopian
    assert re.match(r'[a-z][a-z_.]+', quantopian.__pkg_name__)


def test_valid_version():
    assert semantic_version.validate(quantopian.__version__)


def test_valid_release_date():
    try:
        datetime.strptime(quantopian.__release_date__, '%m/%d/%Y')
    except ValueError:
        pytest.fail()


def test_valid_project_name():
    assert quantopian.__project_name__


def test_valid_project_description():
    assert quantopian.__project_description__


def test_valid_project_url():
    assert validators.url(quantopian.__project_url__)


def test_valid_license():
    assert quantopian.__license__ == 'BSD'


def test_valid_author():
    assert quantopian.__author__
    assert validators.email(quantopian.__author_email__)


def test_valid_maintainer():
    assert quantopian.__maintainer__
    assert validators.email(quantopian.__maintainer_email__)
