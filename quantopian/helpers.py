# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from requests.compat import urlencode

from quantopian import settings


def build_url(*parts, **query):
    q = urlencode(query)
    url = '{scheme}://{base}/{path}{query}'.format(scheme='https',
                                                   base=settings.QUANTOPIAN_HOST,
                                                   path='/'.join(p.lstrip('/') for p in parts),
                                                   query='?' + q if q else '')
    return url
