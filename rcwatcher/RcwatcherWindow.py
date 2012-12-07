# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Jeff Brock boccobrock@gmail.com
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('rcwatcher')

import requests
import xml.etree.ElementTree as ET

from rcwatcher_lib import Window
from rcwatcher.AboutRcwatcherDialog import AboutRcwatcherDialog
from rcwatcher.PreferencesRcwatcherDialog import PreferencesRcwatcherDialog

# See rcwatcher_lib.Window.py for more details about how this class works
class RcwatcherWindow(Window):
    __gtype_name__ = "RcwatcherWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(RcwatcherWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutRcwatcherDialog
        self.PreferencesDialog = PreferencesRcwatcherDialog

        # Code for other initialization actions should be added here.

    def rcwatcher_window_key_press_event_cb(window, contentbuffer, event):
        if(event.keyval == 106):
            contentbuffer.set_text("Rev: "+getRecent());
        elif(event.keyval == 107):
            print "k!"
        elif(event.keyval == 114):
            print "r!"
        elif(event.keyval == 100):
            print "d!"
        elif(event.keyval == 65362):
            print "up!"
        elif(event.keyval == 65364):
            print "down!"
        elif(event.keyval == 113):
            window.destroy()

def getDiff(pageid, rev, oldrev):
    diffurl = 'http://en.wikipedia.org/w/api.php?action=compare&fromrev='+rev+'&torev='+oldrev+'&format=xml'
    print diffurl
    r = requests.get(diffurl)
    diff = ET.fromstring(r.content);
    return diff[0].text

def getRecent():
    r = requests.get('http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&format=xml')
    response = ET.fromstring(r.content);

    for recent in response[0][0]:
        return getDiff(recent.attrib.get('pageid'), recent.attrib.get('revid'), recent.attrib.get('old_revid'))
