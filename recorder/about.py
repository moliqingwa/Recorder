#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timoth�e Lecomte

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

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import sounddevice
import numpy
import OpenGL
import recorder.recorder_rc
import recorder
# from recorder.logwidget import LogWidget
# from recorder.statisticswidget import StatisticsWidget

aboutText = """
<p> <b>Recorder %s</b> (dated %s)</p>
<p> Recorder is an application to record real-time audio signals to local file.</p>
""" % (recorder.__version__,
       recorder.__releasedate__)


class About_Dialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("About_Dialog")
        self.resize(400, 300)
        self.setWindowTitle("About Recorder")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images-src/window-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.aboutWidget = QtWidgets.QWidget()
        self.aboutWidget.setObjectName("aboutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.aboutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.aboutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(128, 128))
        self.label_2.setMaximumSize(QtCore.QSize(128, 128))
        self.label_2.setPixmap(QtGui.QPixmap(":/images-src/window-icon.svg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.aboutWidget)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.label.setText(aboutText)

        self.horizontalLayout.addWidget(self.label)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")

        self.verticalLayout.addWidget(self.aboutWidget)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
