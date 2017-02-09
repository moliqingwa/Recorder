#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

from PyQt5 import QtWidgets

from recorder.widgets.scope.scope import Scope_Widget


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent, logger, name, widget_type=0):
        super().__init__(parent)

        self.setObjectName(name)

        self.logger = logger

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.type = -1
        self.audiowidget = None
        self.widget_select(widget_type)

    # slot
    def widget_select(self, item_index):
        global WIDGET_MAPPING
        if self.audiowidget is not None:
            self.audiowidget.close()
            self.audiowidget.deleteLater()

        self.type = item_index

        self.audiowidget = Scope_Widget(self, self.logger)

        self.audiowidget.set_buffer(self.parent().parent().audiobuffer)
        self.parent().parent().audiobuffer.new_data_available.connect(self.audiowidget.handle_new_data)

        self.layout.addWidget(self.audiowidget)

    def canvasUpdate(self):
        if self.audiowidget is not None:
            self.audiowidget.canvasUpdate()

    def pause(self):
        if self.audiowidget is not None:
            try:
                self.audiowidget.pause()
            except AttributeError:
                pass

    def restart(self):
        if self.audiowidget is not None:
            try:
                self.audiowidget.restart()
            except AttributeError:
                pass

    # slot
    def settings_slot(self, checked):
        if self.audiowidget is not None:
            self.audiowidget.settings_called(checked)

    # method
    def saveState(self, settings):
        settings.setValue("type", self.type)
        if self.audiowidget is not None:
            self.audiowidget.saveState(settings)

    # method
    def restoreState(self, settings):
        widget_type = settings.value("type", 0, type=int)
        self.widget_select(widget_type)
        if self.audiowidget is not None:
            self.audiowidget.restoreState(settings)
