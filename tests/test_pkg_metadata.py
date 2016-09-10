# -*- coding: utf-8 -*-
import re

import semantic_version
import pytest
import validators
from datetime import datetime

import quantopian_tools


def test_valid_pkg_name():
    assert quantopian_tools
    assert re.match(r'[a-z][a-z_.]+', quantopian_tools.__pkg_name__)


def test_valid_version():
    assert semantic_version.validate(str(semantic_version.Version.coerce(quantopian_tools.__version__)))


def test_valid_release_date():
    try:
        datetime.strptime(quantopian_tools.__release_date__, '%m/%d/%Y')
    except ValueError:
        pytest.fail()


def test_valid_project_name():
    assert quantopian_tools.__project_name__


def test_valid_project_description():
    assert quantopian_tools.__project_description__


def test_valid_project_url():
    assert validators.url(quantopian_tools.__project_url__)


def test_valid_license():
    assert quantopian_tools.__license__ == 'BSD'


def test_valid_author():
    assert quantopian_tools.__author__
    assert validators.email(quantopian_tools.__author_email__)


def test_valid_maintainer():
    assert quantopian_tools.__maintainer__
    assert validators.email(quantopian_tools.__maintainer_email__)
