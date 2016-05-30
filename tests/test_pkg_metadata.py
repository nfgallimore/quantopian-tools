# -*- coding: utf-8 -*-
import re

import semantic_version
import pytest
import validators
from datetime import datetime

import python_template


def test_valid_pkg_name():
    assert python_template
    assert re.match(r'[a-z][a-z_.]+', python_template.__pkg_name__)


def test_valid_version():
    assert semantic_version.validate(python_template.__version__)


def test_valid_release_date():
    try:
        datetime.strptime(python_template.__release_date__, '%m/%d/%Y')
    except ValueError:
        pytest.fail()


def test_valid_project_name():
    assert python_template.__project_name__


def test_valid_project_description():
    assert python_template.__project_description__


def test_valid_project_url():
    assert validators.url(python_template.__project_url__)


def test_valid_license():
    assert python_template.__license__ == 'BSD'


def test_valid_author():
    assert python_template.__author__
    assert validators.email(python_template.__author_email__)


def test_valid_maintainer():
    assert python_template.__maintainer__
    assert validators.email(python_template.__maintainer_email__)
