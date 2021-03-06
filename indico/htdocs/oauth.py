# -*- coding: utf-8 -*-
##
##
## This file is part of Indico
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN)
##
## Indico is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico.  If not, see <http://www.gnu.org/licenses/>.

from MaKaC.webinterface.rh import oauth


def request_token(req, **params):
    return oauth.RHOAuthRequestToken(req).process(params)


def authorize(req, **params):
    return oauth.RHOAuthAuthorization(req).process(params)


def access_token(req, **params):
    return oauth.RHOAuthAccessTokenURL(req).process(params)

def authorize_consumer(req, **params):
    return oauth.RHOAuthAuthorizeConsumer(req).process(params)

def thirdPartyAuth(req, **params):
    return oauth.RHOAuthThirdPartyAuth(req).process(params)


def userThirdPartyAuth(req, **params):
    return oauth.RHOAuthUserThirdPartyAuth(req).process(params)
