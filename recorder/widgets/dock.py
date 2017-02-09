#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timoth?Lecomte

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

from PyQt5 import Qt, QtWidgets
from recorder.widgets.setting import Settings_Widget


class Dock(QtWidgets.QDockWidget):
    def __init__(self, parent, logger, name, widget_type=0, timer=None):
        super().__init__(name, parent)

        self.setObjectName(name)

        self.logger = logger
        self.dockwidget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.dockwidget)
        # self.layout.addWidget(self.control_bar)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.dockwidget.setLayout(self.layout)

        self.setWidget(self.dockwidget)

        self.settings_widget = Settings_Widget(self, self.logger, self.parent().audiobackend, timer)

        self.widget_select(widget_type)

    # note that by default the closeEvent is accepted, no need to do it explicitely
    def closeEvent(self, event):
        event.ignore()
        # self.parent().dockmanager.close_dock(self)

    def canvasUpdate(self):
        pass

    def pause(self):
        self.settings_widget.pause()

    def restart(self):
        self.settings_widget.restart()

    # slot
    def settings_slot(self, checked):
        pass

    # slot
    def widget_select(self, item):
        self.layout.addWidget(self.settings_widget)

        self.parent().audiobuffer.new_data_available.connect(self.settings_widget.handle_new_data)

    # method
    def saveState(self, settings):
        settings.setValue("type", self.type)

    # method
    def restoreState(self, settings):
        widget_type = settings.value("type", 0, type=int)
        self.widget_select(widget_type)
