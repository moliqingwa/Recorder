#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

from PyQt5 import QtCore, QtWidgets

from recorder.widgets.ui_settings import Ui_Settings_Dialog

no_input_device_title = "No audio input device found"

no_input_device_message = """No audio input device has been found.

Please check your audio configuration.

Friture will now exit.
"""


class Settings_Dialog(QtWidgets.QDialog, Ui_Settings_Dialog):

    def __init__(self, parent, logger, audiobackend):
        QtWidgets.QDialog.__init__(self, parent)
        Ui_Settings_Dialog.__init__(self)

        # Setup the user interface
        self.setupUi(self)

        self.audiobackend = audiobackend
        self.logger = logger

        devices = self.audiobackend.get_readable_devices_list()

        if devices == []:
            # no audio input device: display a message and exit
            QtWidgets.QMessageBox.critical(self, no_input_device_title, no_input_device_message)
            QtCore.QTimer.singleShot(0, self.exitOnInit)
            return

        for device in devices:
            self.comboBox_inputDevice.addItem(device)

        channels = self.audiobackend.get_readable_current_channels()
        for channel in channels:
            self.comboBox_firstChannel.addItem(channel)
            self.comboBox_secondChannel.addItem(channel)

        current_device = self.audiobackend.get_readable_current_device()
        self.comboBox_inputDevice.setCurrentIndex(current_device)

        first_channel = self.audiobackend.get_current_first_channel()
        self.comboBox_firstChannel.setCurrentIndex(first_channel)
        second_channel = self.audiobackend.get_current_second_channel()
        self.comboBox_secondChannel.setCurrentIndex(second_channel)

        # signals
        self.comboBox_inputDevice.currentIndexChanged.connect(self.input_device_changed)
        self.comboBox_firstChannel.activated.connect(self.first_channel_changed)
        self.comboBox_secondChannel.activated.connect(self.second_channel_changed)
        self.radioButton_single.toggled.connect(self.single_input_type_selected)
        self.radioButton_double.toggled.connect(self.double_input_type_selected)

    # slot
    # used when no audio input device has been found, to exit immediately
    def exitOnInit(self):
        QtWidgets.QApplication.instance().quit()

    # slot
    def input_device_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = self.audiobackend.select_input_device(index)

        self.comboBox_inputDevice.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected input device, reverting to the previous one")

        # reset the channels
        channels = self.audiobackend.get_readable_current_channels()

        self.comboBox_firstChannel.clear()
        self.comboBox_secondChannel.clear()

        for channel in channels:
            self.comboBox_firstChannel.addItem(channel)
            self.comboBox_secondChannel.addItem(channel)

        first_channel = self.audiobackend.get_current_first_channel()
        self.comboBox_firstChannel.setCurrentIndex(first_channel)
        second_channel = self.audiobackend.get_current_second_channel()
        self.comboBox_secondChannel.setCurrentIndex(second_channel)

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def first_channel_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = self.audiobackend.select_first_channel(index)

        self.comboBox_firstChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected channel as the first channel, reverting to the previous one")

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def second_channel_changed(self, index):
        self.parent().ui.actionStart.setChecked(False)

        success, index = self.audiobackend.select_second_channel(index)

        self.comboBox_secondChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage("Impossible to use the selected channel as the second channel, reverting to the previous one")

        self.parent().ui.actionStart.setChecked(True)

    # slot
    def single_input_type_selected(self, checked):
        if checked:
            self.groupBox_second.setEnabled(False)
            self.audiobackend.set_single_input()
            self.logger.push("Switching to single input")

    # slot
    def double_input_type_selected(self, checked):
        if checked:
            self.groupBox_second.setEnabled(True)
            self.audiobackend.set_double_input()
            self.logger.push("Switching to difference between two inputs")

    # method
    def saveState(self, settings):
        # for the input device, we search by name instead of index, since
        # we do not know if the device order stays the same between sessions
        settings.setValue("deviceName", self.comboBox_inputDevice.currentText())
        settings.setValue("firstChannel", self.comboBox_firstChannel.currentIndex())
        settings.setValue("secondChannel", self.comboBox_secondChannel.currentIndex())
        settings.setValue("doubleInput", self.inputTypeButtonGroup.checkedId())

    # method
    def restoreState(self, settings):
        device_name = settings.value("deviceName", "")
        device_index = self.comboBox_inputDevice.findText(device_name)
        # change the device only if it exists in the device list
        if device_index >= 0:
            self.comboBox_inputDevice.setCurrentIndex(device_index)
            channel = settings.value("firstChannel", 0, type=int)
            self.comboBox_firstChannel.setCurrentIndex(channel)
            channel = settings.value("secondChannel", 0, type=int)
            self.comboBox_secondChannel.setCurrentIndex(channel)
            double_input_id = settings.value("doubleInput", 0, type=int)
            self.inputTypeButtonGroup.button(double_input_id).setChecked(True)
