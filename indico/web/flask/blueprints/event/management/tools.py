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
from indico.web.flask.util import rh_as_view
from indico.web.flask.blueprints.event.management import event_mgmt


# Tools
event_mgmt.add_url_rule('/tools/', 'confModifTools', rh_as_view(conferenceModif.RHConfModifTools))

# Tools: Alarms
event_mgmt.add_url_rule('/tools/alarms/', 'confModifTools-displayAlarm', rh_as_view(conferenceModif.RHConfDisplayAlarm))
event_mgmt.add_url_rule('/tools/alarms/add', 'confModifTools-addAlarm',
                        rh_as_view(conferenceModif.RHConfAddAlarm), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/alarms/add/save', 'confModifTools-saveAlarm',
                        rh_as_view(conferenceModif.RHConfSaveAlarm), methods=('POST',))
event_mgmt.add_url_rule('/tools/alarms/add/trigger', 'confModifTools-sendAlarmNow',
                        rh_as_view(conferenceModif.RHConfSendAlarmNow), methods=('POST',))
event_mgmt.add_url_rule('/tools/alarms/<alarmId>/', 'confModifTools-modifyAlarm',
                        rh_as_view(conferenceModif.RHConfModifyAlarm))
event_mgmt.add_url_rule('/tools/alarms/<alarmId>/', 'confModifTools-modifySaveAlarm',
                        rh_as_view(conferenceModif.RHConfSaveAlarm), methods=('POST',))
event_mgmt.add_url_rule('/tools/alarms/<alarmId>/delete', 'confModifTools-deleteAlarm',
                        rh_as_view(conferenceModif.RHConfDeleteAlarm))
event_mgmt.add_url_rule('/tools/alarms/<alarmId>/trigger', 'confModifTools-sendAlarmNow',
                        rh_as_view(conferenceModif.RHConfSendAlarmNow), methods=('POST',))

# Tools: Clone
event_mgmt.add_url_rule('/tools/clone', 'confModifTools-clone', rh_as_view(conferenceModif.RHConfClone))
event_mgmt.add_url_rule('/tools/clone', 'confModifTools-performCloning',
                        rh_as_view(conferenceModif.RHConfPerformCloning), methods=('POST',))

# Tools: Delete
event_mgmt.add_url_rule('/tools/delete', 'confModifTools-delete', rh_as_view(conferenceModif.RHConfDeletion),
                        methods=('GET', 'POST'))

# Tools: Lock
event_mgmt.add_url_rule('/tools/lock', 'conferenceModification-close', rh_as_view(conferenceModif.RHConferenceClose),
                        methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/unlock', 'conferenceModification-open', rh_as_view(conferenceModif.RHConferenceOpen),
                        methods=('GET', 'POST'))

# Tools: Posters
event_mgmt.add_url_rule('/tools/posters/', 'confModifTools-posterPrinting',
                        rh_as_view(conferenceModif.RHConfPosterPrinting), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/posters/poster.pdf', 'confModifTools-posterPrintingPDF',
                        rh_as_view(conferenceModif.RHConfPosterPrintingPDF), methods=('POST',))
event_mgmt.add_url_rule('/tools/posters/design', 'confModifTools-posterDesign',
                        rh_as_view(conferenceModif.RHConfPosterDesign), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/posters/background', 'confModifTools-posterGetBackground',
                        rh_as_view(conferenceModif.RHConfPosterGetBackground), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/posters/save-background', 'confModifTools-posterSaveBackground',
                        rh_as_view(conferenceModif.RHConfPosterSaveTempBackground), methods=('POST',))

# Tools: Badges
event_mgmt.add_url_rule('/tools/badges/', 'confModifTools-badgePrinting',
                        rh_as_view(conferenceModif.RHConfBadgePrinting), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/badges/badges.pdf', 'confModifTools-badgePrintingPDF',
                        rh_as_view(conferenceModif.RHConfBadgePrintingPDF), methods=('POST',))
event_mgmt.add_url_rule('/tools/badges/design', 'confModifTools-badgeDesign',
                        rh_as_view(conferenceModif.RHConfBadgeDesign), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/badges/background', 'confModifTools-badgeGetBackground',
                        rh_as_view(conferenceModif.RHConfBadgeGetBackground), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/tools/badges/save-background', 'confModifTools-badgeSaveBackground',
                        rh_as_view(conferenceModif.RHConfBadgeSaveTempBackground), methods=('POST',))

# Tools: Material Package
event_mgmt.add_url_rule('/tools/material-package', 'confModifTools-matPkg',
                        rh_as_view(conferenceModif.RHFullMaterialPackage))
event_mgmt.add_url_rule('/tools/material-package', 'confModifTools-performMatPkg',
                        rh_as_view(conferenceModif.RHFullMaterialPackagePerform), methods=('POST',))