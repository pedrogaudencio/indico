# -*- coding: utf-8 -*-
##
##
## This file is part of Indico.
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN).
##
## Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico;if not, see <http://www.gnu.org/licenses/>.


from MaKaC.webinterface.rh import fileAccess

# We have to use a function different from "index" as when serving URLs like
#   http://foo.com/indico/getFile.py?id=1 which were outputing a PDF file were
#   causing troubles with IE; everything seems to work fine when we use URLs not
#   ending in ".py"; we couldn't find any documentation regarding this issue
#   so, for the moment, we decided to change the request handler so everything
#   works fine, even if the resulting URL is not very nice.

def access(req, **params):
    return fileAccess.RHFileAccess( req ).process( params )

def accessKey(req, **params):
    return fileAccess.RHFileAccessStoreAccessKey( req ).process( params )

def wmv(req, **params):
    return fileAccess.RHVideoWmvAccess( req ).process( params )

def flash(req, **params):
    return fileAccess.RHVideoFlashAccess( req ).process( params )

def offlineEvent(req, **params):
    return fileAccess.RHOfflineEventAccess( req ).process( params )
