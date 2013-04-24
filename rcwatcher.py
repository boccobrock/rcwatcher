#!/usr/bin/env python -*- coding: utf-8 -*-

import gtk
import webkit
import requests
import xml.etree.ElementTree as ET
import Queue
import os
import pango

class Page(object):
    diff = ""
    title = ""
    timestamp = ""

    def __init__(self, _diff, _title, _timestamp):
        self.diff = _diff
        self.title = _title
        self.timestamp = _timestamp

    def getDiff(self):
        return self.diff

    def getTitle(self):
        return self.title

    def getTimestamp(self):
        return self.timestamp

class Rcwatcher:
    diffs = []
    current = 0
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.connect('delete_event', self.close)
        self.window.connect('key_press_event', self.keyPressed)
        self.window.set_default_size(800, 600)

        vbox = gtk.VBox(spacing=5)
        vbox.set_border_width(5)

        self.title = gtk.Label()

        self.scrolled_window = gtk.ScrolledWindow()
        self.webview = webkit.WebView()
        self.scrolled_window.add(self.webview)

        vbox.pack_start(self.title, fill=False, expand=False)
        vbox.pack_start(self.scrolled_window, fill=True, expand=True)
        self.window.add(vbox)
        self.window.maximize()

    def next(self):
        if self.current+1 >= len(self.diffs):
            self.getRecent()
        self.current += 1
        self.getcurrent()

    def prev(self):
        if self.current > 0:
            self.current -= 1
        self.getcurrent()

    def getcurrent(self):
        diff = open('diff/diff.html', 'w')
        page = self.diffs[self.current]
        diff.write("<meta charset='utf-8'><link rel='stylesheet' type='text/css' href='"+os.getcwd()+"/diff/stylediff.css' />\n<table>"+str(page.getDiff())+"</table>")
        self.title.set_text(page.getTitle() + " - " + page.getTimestamp())
        self.window.set_title('RCWatcher')
        self.webview.open(os.getcwd()+"/diff/diff.html")

    def show(self):
        self.window.show_all()

    def close(self, widget, event, data=None):
        gtk.main_quit()

    def getDiff(self, pageid, rev, oldrev):
        diffurl = 'http://en.wikipedia.org/w/api.php?action=compare&fromrev='+rev+'&torev='+oldrev+'&format=xml'
        r = requests.get(diffurl)
        diff = ET.fromstring(r.content)
        return diff[0].text

    def getRecent(self):
        r = requests.get('http://en.wikipedia.org/w/api.php?action=query&list=recentchanges&format=xml')
        response = ET.fromstring(r.content)

        for recent in response.iter("rc"):
            content = self.getDiff(recent.attrib.get('pageid'), recent.attrib.get('revid'), recent.attrib.get('old_revid'))
            if(content is not None):
                page = Page(content, recent.attrib.get('title'), recent.attrib.get('timestamp'))
                self.diffs.append(page)

    def keyPressed(self, contentbuffer, event):
        if(event.keyval == 106):
            self.next()
        elif(event.keyval == 107):
            self.prev()
        elif(event.keyval == 114):
            print "r!"
        elif(event.keyval == 100):
            print "d!"
        elif(event.keyval == 65362):
            print "up!"
        elif(event.keyval == 65364):
            print "down!"
        elif(event.keyval == 113):
            gtk.main_quit()

if __name__ == '__main__':
    gtk.gdk.threads_init()
    watcher = Rcwatcher()
    watcher.next()
    watcher.show()
    gtk.main()

