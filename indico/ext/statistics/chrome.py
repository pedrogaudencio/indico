# -*- coding: utf-8 -*-
##
##
## This file is part of CDS Indico.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
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

import os
import zope.interface

import indico.ext.statistics

from indico.core.extpoint import Component
from indico.core.extpoint.events import INavigationContributor, IEventDisplayContributor
from indico.core.extpoint.plugins import IPluginSettingsContributor
from indico.ext.statistics.register import StatisticsRegister
from indico.web.rh import RHHtdocs

from MaKaC.i18n import _
from MaKaC.errors import PluginError
from MaKaC.plugins import PluginsHolder
from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from MaKaC.webinterface.pages.conferences import WPConferenceModifBase
from MaKaC.webinterface.urlHandlers import URLHandler
from MaKaC.webinterface import wcomponents


class StatisticsSMContributor(Component):

    zope.interface.implements(INavigationContributor)

    @classmethod
    def fillManagementSideMenu(cls, obj, params={}):
        if obj._conf.canModify(obj._rh._aw):

            if StatisticsRegister().hasActivePlugins():
                params['Statistics'] = wcomponents.SideMenuItem(_('Statistics'),
                    UHConfModifStatistics.getURL(obj._conf))


class StatisticsEFContributor(Component):

    zope.interface.implements(IEventDisplayContributor)

    @classmethod
    def eventDetailFooter(cls, obj, vars):
        """
        Add the footer extension for the statistics tracking.
        """
        stats = PluginsHolder().getPluginType('statistics')
        register = StatisticsRegister()

        if not stats.isActive() or not register.hasActivePlugins():
            return False

        key = 'extraFooterContent'
        extension = {}
        tracking = {}

        tracking['trackingActive'] = True
        tracking['trackingHooks'] = register.getAllPluginJSHooks(obj)

        # Build the extension object to be passed to the footer.
        extension['path'] = register.getJSInjectionPath()
        extension['args'] = tracking

        if key not in vars:
            vars[key] = [extension]
        else:
            vars[key].append(extension)


class UHConfModifStatistics(URLHandler):

    _relativeURL = "statistics"


class RHStatisticsView(RHConferenceModifBase):

    _url = r"^/statistics/?$"
    _register = StatisticsRegister()

    def _checkProtection(self):
        if not PluginsHolder().hasPluginType("statistics"):
            raise PluginError(_("Statistics plugin is not active."))

        self._checkSessionUser()

        RHConferenceModifBase._checkProtection(self)

    def _checkParams(self, params):
        RHConferenceModifBase._checkParams(self, params)
        self._activeTab = params.pop("tab", 'Piwik')
        self._params = params

    def _process(self):
        return WPStatisticsView(self, WStatisticsView, self._activeTab, self._params).display()


class RHStatisticsHtdocs(RHHtdocs):

    _url = r"^/statistics/(?P<filepath>.*)$"
    _local_path = os.path.join(indico.ext.statistics.__path__[0], 'htdocs')


class WStatisticsView(wcomponents.WTemplated):

    def __init__(self, register, activeTab, params):
        self._register = register
        self._confId = params.get('confId')
        self._contribId = params.get('contribId')
        self._startDate = params.get('startDate')
        self._endDate = params.get('endDate')
        self._activeTab = activeTab

    def getVars(self):
        """
        In this method it is expected that any implementations of statistics
        have both a getContributionReport and getConferenceReport method
        defined, the results of which are the data for the view.
        """
        vars = wcomponents.WTemplated.getVars(self)
        plugin = self._register.getPluginByName(self._activeTab, instantiate=False)

        if self._contribId is not None:
            vars["report"] = plugin.getContributionReport(self._startDate, self._endDate,
                                                          self._confId, self._contribId)
        elif self._confId is not None:
            vars["report"] = plugin.getConferenceReport(self._startDate, self._endDate,
                                                        self._confId)
        else:
            raise Exception(_('Cannot instantiate reports view without ID.'))

        return vars


class PluginSettingsContributor(Component):

    zope.interface.implements(IPluginSettingsContributor)

    def hasPluginSettings(self, obj, ptype, plugin):
        return (ptype == 'statistics' and plugin == None)

    def getPluginSettingsHTML(self, obj, ptype, plugin):
        if ptype == 'statistics' and plugin == None:
            return WPluginSettings.forModule(indico.ext.statistics).getHTML()


class WPluginSettings(wcomponents.WTemplated):

    def getVars(self):
        """
        Extend here to add more information to the plugin settings page, hence
        allowing admin only view.
        """
        return wcomponents.WTemplated.getVars(self)


class WPStatisticsView(WPConferenceModifBase):

    def __init__(self, rh, templateClass, activeTab, params):
        WPConferenceModifBase.__init__(self, rh, rh._conf)
        self._rh = rh
        self._conf = self._rh._conf
        self._register = StatisticsRegister()
        self._plugins = self._register.getAllPlugins(activeOnly=True)
        self._templateClass = templateClass
        self._extraJS = []
        self._activeTabName = activeTab
        self._params = params
        self._tabs = []
        self._tabCtrl = wcomponents.TabControl()

    def _createTabCtrl(self):
        for plugin in self._plugins:
            self._tabs.append(self._tabCtrl.newTab(plugin.getName(),
                plugin.getName(), UHConfModifStatistics.getURL(self._conf,
                                                               tab=plugin.getName())))

    def _getTitle(self):
        return WPConferenceModifBase._getTitle(self) + " - " + _("Statistics")

    def _getPageContent(self, params):
        self._createTabCtrl()
        plugin = self._register.getPluginByName(self._activeTabName)

        if not plugin:
            raise Exception(_('There is no tab called %s available.') % \
                            self._activeTabName)

        return wcomponents.WTabControl(self._tabCtrl, self._getAW()).getHTML(
            self._templateClass.forModule(plugin.getImplementationPackage(),
                                          self._register, self._activeTabName, self._params).getHTML(params))

    def getCSSFiles(self):
        return WPConferenceModifBase.getCSSFiles(self) + \
                ['statistics/css/main.css']

    def getJSFiles(self):
        return WPConferenceModifBase.getJSFiles(self) + \
                ['statistics/js/statistics.js']

    def _setActiveSideMenuItem(self):
        if 'Statistics' in self._pluginsDictMenuItem:
            self._pluginsDictMenuItem['Statistics'].setActive(True)