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
## along with Indico. If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint

import MaKaC.plugins.Collaboration.handlers as handlers
from indico.web.flask.util import rh_as_view


blueprint = Blueprint('collaboration', __name__, url_prefix='/Collaboration')

blueprint.add_url_rule('/elecAgree', 'elecAgree', rh_as_view(handlers.RHElectronicAgreement))
blueprint.add_url_rule('/uploadElecAgree', 'uploadElecAgree', rh_as_view(handlers.RHUploadElectronicAgreement),
                       methods=('POST',))
blueprint.add_url_rule('/getPaperAgree', 'getPaperAgree', rh_as_view(handlers.RHElectronicAgreementGetFile))
blueprint.add_url_rule('/elecAgreeForm', 'elecAgreeForm', rh_as_view(handlers.RHElectronicAgreementForm))

blueprint.add_url_rule('/<plugin>/<path:filepath>', 'htdocs', rh_as_view(handlers.RHCollaborationHtdocs))
blueprint.add_url_rule('/<path:filepath>', 'htdocs', rh_as_view(handlers.RHCollaborationHtdocs))