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


# Booking and event assignment list
event_mgmt.add_url_rule('/rooms/', 'conferenceModification-roomBookingList',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingList))
event_mgmt.add_url_rule('/rooms/book/select-event', 'conferenceModification-roomBookingChooseEvent',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingChooseEvent))

# View/modify booking
event_mgmt.add_url_rule('/rooms/booking/<path:roomLocation>/<resvID>/', 'conferenceModification-roomBookingDetails',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingDetails))
event_mgmt.add_url_rule('/rooms/booking/<path:roomLocation>/<resvID>/modify',
                        'conferenceModification-roomBookingModifyBookingForm',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingBookingForm), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/booking/<path:roomLocation>/<resvID>/clone',
                        'conferenceModification-roomBookingCloneBooking',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingCloneBooking), methods=('GET', 'POST'))

# Book room
event_mgmt.add_url_rule('/rooms/book/search',
                        'conferenceModification-roomBookingSearch4Rooms',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingSearch4Rooms), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/book/search/results', 'conferenceModification-roomBookingRoomList',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingRoomList), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/book/confirm', 'conferenceModification-roomBookingBookingForm',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingBookingForm), methods=('GET', 'POST'))
event_mgmt.add_url_rule('/rooms/book/save',
                        'conferenceModification-roomBookingSaveBooking',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingSaveBooking), methods=('GET', 'POST'))

# Room details
event_mgmt.add_url_rule('/rooms/room/<path:roomLocation>/<roomID>/',
                        'conferenceModification-roomBookingRoomDetails',
                        rh_as_view(conferenceModif.RHConfModifRoomBookingRoomDetails), methods=('GET', 'POST'))