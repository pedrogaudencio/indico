# -*- coding: utf-8 -*-
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
from flask import session

from MaKaC.services.implementation.base import LoggedOnlyService, AdminService
from MaKaC.services.implementation.base import ServiceBase

import MaKaC.user as user
from MaKaC.services.interface.rpc.common import ServiceError, ServiceAccessError, NoReportError

from MaKaC.common import info
from MaKaC.common.logger import Logger

import time
from MaKaC.fossils.user import IAvatarAllDetailsFossil, IAvatarFossil
from MaKaC.common.fossilize import fossilize

from MaKaC.rb_location import CrossLocationQueries

from indico.util.i18n import getLocaleDisplayNames, availableLocales
from MaKaC.webinterface.common.timezones import TimezoneRegistry
from MaKaC.services.implementation.base import ParameterManager
from MaKaC.webinterface.common.person_titles import TitlesRegistry
import MaKaC.common.indexes as indexes
from MaKaC.common.utils import validMail
from indico.util.redis import avatar_links
from indico.web.http_api.auth import APIKey

class UserComparator(object):

    @staticmethod
    def cmpUsers(x, y):
        cmpResult = cmp(x["familyName"].lower(), y["familyName"].lower())
        if cmpResult == 0:
            cmpResult = cmp(x["firstName"].lower(), y["firstName"].lower())
        return cmpResult

    @staticmethod
    def cmpGroups(x, y):
        return cmp(x["name"].lower(), y["name"].lower())

class UserBaseService(LoggedOnlyService):

    def _checkParams(self):
        self._pm = ParameterManager(self._params)
        userId = self._pm.extract("userId", None)
        if userId is not None:
            ah = user.AvatarHolder()
            self._target = ah.getById(userId)
        else:
            raise ServiceError("ERR-U5", _("User id not specified"))

class UserModifyBase(UserBaseService):

    def _checkProtection(self):
        LoggedOnlyService._checkProtection(self)
        if self._aw.getUser():
            if not self._target.canModify( self._aw ):
                raise ServiceError("ERR-U6", _("You are not allowed to perform this request"))
        else:
            raise ServiceError("ERR-U7", _("You are currently not authenticated. Please log in again."))


class UserListEvents(LoggedOnlyService):

    def _checkParams(self):
        LoggedOnlyService._checkParams(self)

        self._time = self._params.get('time', None)
        self._target = self.getAW().getUser()

    def __exportElemDataFactory(self, moment):
        return lambda elem: {
            'id': elem[0].getId(),
            'title': elem[0].getTitle(),
            'roles': [elem[1]],
            'timestamp':time.mktime(elem[0].getStartDate().timetuple()),
            'startDate':str(elem[0].getStartDate().strftime("%d/%m/%Y")),
            'endDate':str(elem[0].getEndDate().strftime("%d/%m/%Y")),
            'startTime':str(elem[0].getStartDate().strftime("%H:%M")),
            'endTime':str(elem[0].getEndDate().strftime("%H:%M")),
            'type': moment,
            'evtType': elem[0].getVerboseType()
        }

    def _getAnswer( self):

        events = []

        self._target.getTimedLinkedEvents().sync()

        if (not self._time) or self._time == 'past':
            events.extend( map( self.__exportElemDataFactory('past'),
                               self._target.getTimedLinkedEvents().getPast()))

        if (not self._time) or self._time == 'present':
            events.extend( map(self.__exportElemDataFactory('present'),
                              self._target.getTimedLinkedEvents().getPresent()))

        if (not self._time) or self._time == 'future':
            events.extend( map(self.__exportElemDataFactory('future'),
                              self._target.getTimedLinkedEvents().getFuture()))

        jsonData = {}

        for event in events:
            if jsonData.has_key(event['id']):
                jsonData[event['id']]['roles'].append(event['roles'][0])
            else:
                jsonData[event['id']] = event

        return jsonData

class UserBasketBase:

    def _checkParams(self):
        ServiceBase._checkParams(self)
        self._pm = ParameterManager(self._params)
        userId = self._pm.extract("userId", pType=str, allowEmpty=True)
        if userId is not None:
            ah = user.AvatarHolder()
            self._target = ah.getById(userId)
        else:
            self._target = self._aw.getUser()

    def _checkProtection(self):
        if not self._aw.getUser():
            raise ServiceAccessError(_("You are currently not authenticated. Please log in again."))
        if not self._target.canUserModify(self._aw.getUser()):
            raise ServiceAccessError('Access denied')

class UserAddToBasket(LoggedOnlyService, UserBasketBase):

    def _checkParams(self):
        UserBasketBase._checkParams(self)

        self._userList = []
        for userData in self._params['value']:
            self._userList.append(user.AvatarHolder().getById(userData['id']))

    def _getAnswer(self):

        ##### Why not?
        #if (self._target in self._userList):
        #    raise ServiceError("ERR-U3","Trying to add user to his own favorites!")

        if (self._userList == []):
            raise ServiceError("ERR-U0","No users specified!")

        for user in self._userList:
            #we do not care if the user is already in the favourites
            self._target.getPersonalInfo().getBasket().addElement(user)

    def _checkProtection(self):
        LoggedOnlyService._checkProtection(self)
        UserBasketBase._checkProtection(self)


class UserRemoveFromBasket(LoggedOnlyService, UserBasketBase):
    def _checkParams(self):
        UserBasketBase._checkParams(self)
        self._userData = self._params['value']

    def _getAnswer( self):
        for obj in self._userData:
            if not self._target.getPersonalInfo().getBasket().deleteUser(obj['id']):
                raise ServiceError("ERR-U0","Element '%s' not found in favorites!" % obj['id'])

    def _checkProtection(self):
        LoggedOnlyService._checkProtection(self)
        UserBasketBase._checkProtection(self)

class UserListBasket(UserBasketBase, ServiceBase):

    """
    Service that lists the users belonging to the the user's "favorites"
    Should return None in case the user is not logged in.
    """

    def _checkParams(self):
        ServiceBase._checkParams(self)
        UserBasketBase._checkParams(self)
        self._allDetails = self._params.get("allDetails", False)

    def _getAnswer( self):

        if self._target:
            users = self._target.getPersonalInfo().getBasket().getUsers().values()

            if self._allDetails:
                fossilToUse = IAvatarAllDetailsFossil
            else:
                fossilToUse = IAvatarFossil

            fossilizedResult = fossilize(users, fossilToUse)
            fossilizedResult.sort(cmp=UserComparator.cmpUsers)
            return fossilizedResult

        else:
            return None

class UserGetEmail(LoggedOnlyService):

    def _checkParams(self):
        LoggedOnlyService._checkParams(self)
        self._target = self.getAW().getUser()


    def _getAnswer( self):
        if self._target:
            return self._target.getEmail()
        else:
            raise ServiceError("ERR-U4","User is not logged in")

class UserGetTimezone(ServiceBase):

    def _getAnswer(self):
        if self.getAW().getUser():
            tz = self.getAW().getUser().getTimezone()
        else:
            tz = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        return tz


class UserGetSessionTimezone(ServiceBase):

    def _getAnswer(self):
        return session.timezone


class UserGetSessionLanguage(ServiceBase):

    def _getAnswer(self):
        if self.getAW().getSession():
            return self.getAW().getSession().getLang()
        else:
            minfo = info.HelperMaKaCInfo.getMaKaCInfoInstance()
            return minfo.getLang()

class UserCanBook(LoggedOnlyService):

    def _checkParams(self):
        LoggedOnlyService._checkParams(self)
        self._user = self.getAW().getUser()
        self._roomID = int(self._params.get("roomID", ""))
        self._roomLocation = self._params.get("roomLocation", "").replace("+"," ")
        self._room = CrossLocationQueries.getRooms(roomID = self._roomID, location = self._roomLocation)

    def _getAnswer( self):
        if self._user and self._room:
            if not self._room.isActive and not self._user.isAdmin():
                return False
            if not self._room.canBook( self._user ) and not self._room.canPrebook( self._user ):
                return False
            return True
        return False

class UserShowPastEvents(UserModifyBase):

    def _getAnswer( self):
        self._target.getPersonalInfo().setShowPastEvents(True)
        return True


class UserHidePastEvents(UserModifyBase):

    def _getAnswer( self):
        self._target.getPersonalInfo().setShowPastEvents(False)
        return True

class UserGetLanguages(UserBaseService):

    def _getAnswer( self):
        return getLocaleDisplayNames()


class UserSetLanguage(UserModifyBase):

    def _checkParams(self):
        UserModifyBase._checkParams(self)
        self._lang = self._params.get("lang",None)

    def _getAnswer( self):
        if self._lang and self._lang in availableLocales:
            self._target.setLang(self._lang)
            return True
        else:
            return False


class UserGetTimezones(UserBaseService):

    def _getAnswer( self):
        return TimezoneRegistry.getList()


class UserSetTimezone(UserModifyBase):

    def _checkParams(self):
        UserModifyBase._checkParams(self)
        self._tz = self._params.get("tz",None)

    def _getAnswer( self):
        if self._tz and self._tz in TimezoneRegistry.getList():
            self._target.setTimezone(self._tz)
            return True
        return False


class UserGetDisplayTimezones(UserBaseService):

    def _getAnswer( self):
        if self._target.getDisplayTZMode() == "Event Timezone":
            tzMode = ["Event Timezone", "MyTimezone"]
        else:
            tzMode = ["MyTimezone", "Event Timezone"]
        return tzMode


class UserSetDisplayTimezone(UserModifyBase):

    def _checkParams(self):
        UserModifyBase._checkParams(self)
        self._tzMode = self._params.get("tzMode",None)

    def _getAnswer( self):
        if self._tzMode and self._tzMode in ["Event Timezone", "MyTimezone"]:
            self._target.setDisplayTZMode(self._tzMode)
            return True
        return False


class UserPersonalDataBase(UserModifyBase):

    _dataTypes = ["title", "surName", "name", "fullName", "straightFullName", "organisation",
                  "email", "secondaryEmails", "address", "telephone", "fax"]

    def _checkParams(self):
        self._pm = ParameterManager(self._params)
        userId = self._pm.extract("userId", None)
        if userId is not None:
            ah = user.AvatarHolder()
            self._user = self._avatar = self._target = ah.getById(userId)
        else:
            raise ServiceError("ERR-U5", _("User id not specified"))
        self._dataType = self._pm.extract("dataType", pType=str, allowEmpty=False)
        if self._dataType not in self._dataTypes:
            raise ServiceError("ERR-U7", _("Data argument is not valid"))


class UserSetPersonalData(UserPersonalDataBase):

    def _checkParams(self):
        UserPersonalDataBase._checkParams(self)
        if (self._dataType == "surName" or self._dataType == "name" or self._dataType == "organisation"):
            self._value = self._pm.extract("value", pType=str, allowEmpty=False)
        elif (self._dataType == "email"):
            self._value = self._pm.extract("value", pType=str, allowEmpty=False)
            if not validMail(self._value):
                raise ServiceAccessError(_("The email address is not valid"))
        else:
            self._value = self._pm.extract("value", pType=str, allowEmpty=True)

    def _buildEmailList(self):
        emailList = []
        if (self._value == ""):
            return emailList
        else:
            # replace to have only one separator
            self._value = self._value.replace(" ",",")
            self._value = self._value.replace(";",",")
            emailList = self._value.split(",")
            return emailList

    def _getAnswer( self):
        if self._user:
            idxs = indexes.IndexesHolder()
            funcGet = "get%s%s" % (self._dataType[0].upper(), self._dataType[1:])
            funcSet = "set%s%s" % (self._dataType[0].upper(), self._dataType[1:])
            if self._dataType == "title":
                if self._value in TitlesRegistry().getList():
                    self._user.setTitle(self._value)
                else:
                    raise NoReportError(_("Invalid title value"))
            elif self._dataType == "surName":
                self._user.setFieldSynced('surName', False)
                surName = idxs.getById("surName")
                surName.unindexUser(self._avatar)
                self._user.setSurName(self._value)
                surName.indexUser(self._avatar)
            elif self._dataType == "name":
                self._user.setFieldSynced('firstName', False)
                name = idxs.getById("name")
                name.unindexUser(self._avatar)
                self._user.setName(self._value)
                name.indexUser(self._avatar)
            elif self._dataType == "organisation":
                self._user.setFieldSynced('affiliation', False)
                org = idxs.getById("organisation")
                org.unindexUser(self._avatar)
                self._user.setOrganisation(self._value)
                org.indexUser(self._avatar)
            elif self._dataType == "email":
                # Check if there is any user with this email address
                if self._value != self._avatar.getEmail():
                    other = user.AvatarHolder().match({"email": self._value}, searchInAuthenticators=False)
                    if other and other[0] != self._avatar:
                        raise NoReportError(_("The email address %s is already used by another user.") % self._value)
                email = idxs.getById("email")
                email.unindexUser(self._avatar)
                self._user.setEmail(self._value)
                email.indexUser(self._avatar)
            elif self._dataType == "secondaryEmails":
                emailList = self._buildEmailList()
                secondaryEmails = []
                # check if every secondary email is valid
                for email in emailList:
                    if email != "":
                        av = user.AvatarHolder().match({"email": email}, searchInAuthenticators=False)
                        if av and av[0] != self._avatar:
                            raise NoReportError(_("The email address %s is already used by another user.") % email)
                        else:
                            secondaryEmails.append(email)
                self._user.setSecondaryEmails(secondaryEmails)
                return ", ".join(self._user.getSecondaryEmails())
            elif self._dataType == "telephone":
                self._user.setFieldSynced('phone', False)
                self._user.setTelephone(self._value)
            elif self._dataType == "fax":
                self._user.setFieldSynced('fax', False)
                self._user.setFax(self._value)
            elif self._dataType == "address":
                self._user.setFieldSynced('address', False)
                self._user.setAddress(self._value)
            else:
                getattr(self._user, funcSet)(self._value)

            return getattr(self._user, funcGet)()
        else:
            raise ServiceError("ERR-U5", _("User id not specified"))


class UserSyncPersonalData(UserPersonalDataBase):
    _dataTypes = ["surName", "firstName", "affiliation", "phone", "fax", "address"]

    def _getAnswer(self):
        if self._dataType == 'name':
            self._dataType = 'firstName'
        self._user.setFieldSynced(self._dataType, True)
        val = self._user.getAuthenticatorPersonalData(self._dataType)
        if val:
            setter = "set%s%s" % (self._dataType[0].upper(), self._dataType[1:])
            getattr(self._user, setter)(val)
        return dict(val=val)

class UserSetPersistentSignatures(UserModifyBase):

    def _checkParams(self):
        UserModifyBase._checkParams(self)
        if self._target == None:
            raise ServiceAccessError((_("The user with does not exist")))

    def _getAnswer(self):
        ak = self._target.getAPIKey()
        ak.setPersistentAllowed(not ak.isPersistentAllowed())
        return ak.isPersistentAllowed()

class UserCreateKeyEnablePersistent(LoggedOnlyService):

    def _checkParams(self):
        LoggedOnlyService._checkParams(self)
        self._target = self._avatar = self.getAW().getUser()
        pm = ParameterManager(self._params)
        self._enablePersistent = pm.extract("enablePersistent", bool, False, False)

    def _getAnswer( self):
        minfo = info.HelperMaKaCInfo.getMaKaCInfoInstance()
        ak = APIKey(self._avatar)
        ak.create()
        if minfo.isAPIPersistentAllowed() and self._enablePersistent:
            ak.setPersistentAllowed(True)
        return True


class UserRefreshRedisLinks(AdminService):
    def _checkParams(self):
        AdminService._checkParams(self)
        self._pm = ParameterManager(self._params)
        userId = self._pm.extract("userId", pType=str, allowEmpty=True)
        if userId is not None:
            ah = user.AvatarHolder()
            self._avatar = ah.getById(userId)
        else:
            self._avatar = self._aw.getUser()

    def _getAnswer(self):
        avatar_links.delete_avatar(self._avatar)  # clean start
        avatar_links.init_links(self._avatar)


methodMap = {
    "event.list": UserListEvents,
    "favorites.addUsers": UserAddToBasket,
    "favorites.removeUser": UserRemoveFromBasket,
    "favorites.listUsers": UserListBasket,
    "data.email.get": UserGetEmail,
    "timezone.get": UserGetTimezone,
    "session.timezone.get": UserGetSessionTimezone,
    "session.language.get": UserGetSessionLanguage,
    "canBook": UserCanBook,
    "showPastEvents": UserShowPastEvents,
    "hidePastEvents": UserHidePastEvents,
    "getLanguages": UserGetLanguages,
    "setLanguage": UserSetLanguage,
    "getTimezones": UserGetTimezones,
    "setTimezone": UserSetTimezone,
    "getDisplayTimezones": UserGetDisplayTimezones,
    "setDisplayTimezone": UserSetDisplayTimezone,
    "setPersonalData": UserSetPersonalData,
    "syncPersonalData": UserSyncPersonalData,
    "togglePersistentSignatures": UserSetPersistentSignatures,
    "createKeyAndEnablePersistent": UserCreateKeyEnablePersistent,
    "refreshRedisLinks": UserRefreshRedisLinks
}
