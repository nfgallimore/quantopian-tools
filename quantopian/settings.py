# -*- coding: utf-8 -*-
"""
Settings for the project. All settings can be configured in the environment.
"""
from __future__ import print_function, absolute_import, division, unicode_literals

import os


def get_str_env_var(name, default=None):
    return os.environ.get(name) or default


QUANTOPIAN_HOST = get_str_env_var('QUANTOPIAN_HOST', 'www.quantopian.com')
QUANTOPIAN_LOGIN_PATH = get_str_env_var('QUANTOPIAN_LOGIN_PATH', '/users/signin')

QUANTOPIAN_EMAIL = get_str_env_var('QUANTOPIAN_EMAIL')
QUANTOPIAN_PWD = get_str_env_var('QUANTOPIAN_PWD')
