# -*- coding: utf-8 -*-
"""
Sessions handle the details of authentication and transporting requests.
"""
from __future__ import print_function, absolute_import, division, unicode_literals

import logging

import mechanicalsoup
import requests

from quantopian import settings
from quantopian.exceptions import AlreadyLoggedIn, NotLoggedIn, RequestError
from quantopian.helpers import build_url

log = logging.getLogger(__name__)


class QBrowser(mechanicalsoup.Browser):
    def __init__(self):
        self.is_authenticated = False
        self._csrf_tokens = {}
        super(QBrowser, self).__init__(session=requests.Session(), soup_config={"features": "html.parser"})

    def get_csrf_token(self, url):
        if url not in self._csrf_tokens:
            response = self.get(url)
            if not response.ok:
                raise RequestError('failed to get csrf token page', response)

            meta_tag = response.soup.find('meta', attrs={'name': 'csrf-token'})
            if not meta_tag or 'content' not in meta_tag.attrs:
                raise RequestError('failed to find csrf token in dom', response)

            self._csrf_tokens[url] = meta_tag.attrs['content']

        return self._csrf_tokens[url]

    def login(self, email=settings.QUANTOPIAN_EMAIL, password=settings.QUANTOPIAN_PWD):
        if self.is_authenticated:
            raise AlreadyLoggedIn()
        response = self.get(build_url('signin'))
        form_candidates = response.soup.select("form#new_user")
        if len(form_candidates) != 1:
            raise RequestError('failed to get login form', response)

        login_form = form_candidates[0]
        login_form.select("#user_email")[0]['value'] = email
        login_form.select("#user_password")[0]['value'] = password

        response = self.submit(login_form, build_url(login_form.attrs['action']))
        if not response.ok:
            raise RequestError('failed to submit login form', response)

        # Check authentication worked by accessing the account
        response = self.get(build_url('account'), allow_redirects=False)
        if not response.ok:
            raise RequestError('failed to verify the user is authenticated', response)

        # If not logged in the requests is redirected to the login page
        if response.is_redirect:
            return False

        self.is_authenticated = True
        return True

    def logout(self):
        self.assert_logged_in()
        self.session.close()
        self.__init__()
        return not self.is_authenticated

    def assert_logged_in(self):
        if not self.is_authenticated:
            raise NotLoggedIn()


browser = QBrowser()
