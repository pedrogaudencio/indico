# -*- coding: utf-8 -*-
##
##
## This file is part of CDS Indico.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
##
## CDS Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Indico; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Network-related utility functions
"""

from MaKaC.common.info import HelperMaKaCInfo


def _get_remote_ip(req):
    hostIP = str(req.get_remote_ip())

    minfo = HelperMaKaCInfo.getMaKaCInfoInstance()
    if minfo.useProxy():
        # if we're behind a proxy, use X-Forwarded-For
        return req.headers_in.get("X-Forwarded-For", hostIP).split(", ")[-1]
    else:
        return hostIP