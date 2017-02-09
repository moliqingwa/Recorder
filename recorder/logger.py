#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

from PyQt5 import QtCore


class Logger(QtCore.QObject):

    logChanged = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.count = 0
        self.log = ""

    # push some text to the log
    def push(self, text):
        if len(self.log) == 0:
            self.log = "[0] %s" % text
        else:
            self.log = "%s\n[%d] %s" % (self.log, self.count, text)
        self.count += 1
        self.logChanged.emit()

        # also print to the console
        print(text)

    # return the current log
    def text(self):
        return self.log


# simple logger that prints to the console
class PrintLogger:
    # push some text to the log

    def push(self, text):
        print(text)

    # return the current log
    def text(self):
        return ""
