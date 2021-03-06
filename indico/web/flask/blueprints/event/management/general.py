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

from MaKaC.webinterface.rh import conferenceModif
from indico.web.flask.blueprints.event.management import event_mgmt


# General settings
event_mgmt.add_url_rule('/general/', 'conferenceModification', conferenceModif.RHConferenceModification)
event_mgmt.add_url_rule('/general/screendates', 'conferenceModification-screenDates',
                        conferenceModif.RHConfScreenDatesEdit, methods=('GET', 'POST'))
event_mgmt.add_url_rule('/general/data', 'conferenceModification-data', conferenceModif.RHConfDataModif,
                        methods=('GET', 'POST'))
event_mgmt.add_url_rule('/general/data/save', 'conferenceModification-dataPerform',
                        conferenceModif.RHConfPerformDataModif, methods=('POST',))

# Contribution types
event_mgmt.add_url_rule('/contribution-types/add', 'conferenceModification-addContribType',
                        conferenceModif.RHConfAddContribType, methods=('GET', 'POST'))
event_mgmt.add_url_rule('/contribution-types/delete', 'conferenceModification-removeContribType',
                        conferenceModif.RHConfRemoveContribType, methods=('POST',))
event_mgmt.add_url_rule('/contribution-types/<contribTypeId>', 'conferenceModification-editContribType',
                        conferenceModif.RHConfEditContribType, methods=('GET', 'POST'))
