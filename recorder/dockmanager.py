#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Timothée Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from recorder.defaults import DEFAULT_DOCKS
from recorder.widgets.dock import Dock


class DockManager(QtCore.QObject):

    def __init__(self, parent, logger):
        super().__init__(parent)

        # the parent must of the QMainWindow so that docks are created as children of it
        assert isinstance(parent, QMainWindow)

        self.docks = []
        self.logger = logger

    # slot
    def new_dock(self, **kwargs):
        name = "Settings"
        new_dock = Dock(self.parent(), self.logger, name, timer=kwargs.get("timer", None))
        self.parent().addDockWidget(QtCore.Qt.TopDockWidgetArea, new_dock)

        self.docks += [new_dock]

    # slot
    def close_dock(self, dock):
        self.docks.remove(dock)

    def saveState(self, settings):
        docknames = [dock.objectName() for dock in self.docks]
        settings.setValue("dockNames", docknames)
        for dock in self.docks:
            settings.beginGroup(dock.objectName())
            dock.saveState(settings)
            settings.endGroup()

    def restoreState(self, settings):
        if settings.contains("dockNames"):
            docknames = settings.value("dockNames", [])
            # list of docks
            self.docks = [Dock(self.parent(), self.logger, name) for name in docknames]
            for dock in self.docks:
                settings.beginGroup(dock.objectName())
                dock.restoreState(settings)
                settings.endGroup()
        else:
            self.logger.push("First launch, display a default set of docks")
            self.docks = [Dock(self.parent(), self.logger, "Dock %d" % (i), widget_type=widget_type) for i, widget_type in enumerate(DEFAULT_DOCKS)]
            for dock in self.docks:
                self.parent().addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)

    def canvasUpdate(self):
        for dock in self.docks:
            dock.canvasUpdate()

    def pause(self):
        for dock in self.docks:
            try:
                dock.pause()
            except AttributeError:
                pass

    def restart(self):
        for dock in self.docks:
            try:
                dock.restart()
            except AttributeError:
                pass
