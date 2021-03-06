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


from MaKaC.webinterface.rh import conferenceModif

def index( req, **params ):
    return conferenceModif.RHConfModifDisplayCustomization( req ).process( params )

def custom( req, **params ):
    return conferenceModif.RHConfModifDisplayCustomization( req ).process( params )

def menu( req, **params ):
    return conferenceModif.RHConfModifDisplayMenu( req ).process( params )

def resources( req, **params ):
    return conferenceModif.RHConfModifDisplayResources( req ).process( params )

def confHeader( req, **params ):
    return conferenceModif.RHConfModifDisplayConfHeader( req ).process( params )

def modifyData( req, **params ):
    return conferenceModif.RHConfModifDisplayModifyData( req ).process( params )

def addLink( req, **params ):
    return conferenceModif.RHConfModifDisplayAddLink( req ).process( params )

def addPage( req, **params ):
    return conferenceModif.RHConfModifDisplayAddPage( req ).process( params )

def addSpacer( req, **params ):
    return conferenceModif.RHConfModifDisplayAddSpacer( req ).process( params )


def removeLink( req, **params ):
    return conferenceModif.RHConfModifDisplayRemoveLink( req ).process( params )


def toggleLinkStatus( req, **params ):
    return conferenceModif.RHConfModifDisplayToggleLinkStatus( req ).process( params )

def toggleHomePage( req, **params ):
    return conferenceModif.RHConfModifDisplayToggleHomePage( req ).process( params )

def upLink( req, **params ):
    return conferenceModif.RHConfModifDisplayUpLink( req ).process( params )


def downLink( req, **params ):
    return conferenceModif.RHConfModifDisplayDownLink( req ).process( params )

def formatTitleBgColor(req, **params):
    return conferenceModif.RHConfModifFormatTitleBgColor( req ).process( params )

def formatTitleTextColor(req, **params):
    return conferenceModif.RHConfModifFormatTitleTextColor( req ).process( params )

def saveLogo( req, **params ):
    return conferenceModif.RHConfSaveLogo( req ).process( params )

def removeLogo( req, **params ):
    return conferenceModif.RHConfRemoveLogo( req ).process( params )

def saveCSS( req, **params ):
    return conferenceModif.RHConfSaveCSS( req ).process( params )

def removeCSS( req, **params ):
    return conferenceModif.RHConfRemoveCSS( req ).process( params )

def savePic( req, **params ):
    return conferenceModif.RHConfSavePic( req ).process( params )

def modifySystemData(req, **params ):
    return conferenceModif.RHConfModifDisplayModifySystemData( req ).process( params )

def tickerTapeAction(req, **params ):
    return conferenceModif.RHConfModifTickerTapeAction( req ).process( params )

def toggleSearch(req, **params ):
    return conferenceModif.RHConfModifToggleSearch( req ).process( params )

def toggleNavigationBar(req, **params ):
    return conferenceModif.RHConfModifToggleNavigationBar( req ).process( params )

def previewCSS(req, **params):
    return conferenceModif.RHConfModifPreviewCSS(req).process(params)

def useCSS(req, **params):
    return conferenceModif.RHConfUseCSS(req).process(params)
