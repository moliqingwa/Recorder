#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

import os, time

import numpy as np
from PyQt5 import QtCore, QtWidgets

from recorder.utilities.audioFeatureExtraction import stEnergy
from recorder.widgets.audio_recorder import AudioRecorder

no_input_device_title = "No audio input device found"

no_input_device_message = """No audio input device has been found.

Please check your audio configuration.

Recorder will now exit.
"""

from recorder.audiobackend import SAMPLING_RATE


class Settings_Widget(QtWidgets.QWidget):
    def __init__(self, parent, logger, audiobackend, timer):
        super().__init__(parent)

        self.audiobackend = audiobackend
        self.timer = timer
        self.logger = logger
        self.start_time = None
        self.data = None
        self.timer.timeout.connect(self.timeout_update)

        self.setObjectName("Settings_Widget")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_inputType_2 = QtWidgets.QLabel(self)
        self.label_inputType_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_inputType_2.setObjectName("label_inputType_2")
        self.verticalLayout_5.addWidget(self.label_inputType_2)
        self.comboBox_inputDevice = QtWidgets.QComboBox(self)
        self.comboBox_inputDevice.setObjectName("comboBox_inputDevice")
        self.verticalLayout_5.addWidget(self.comboBox_inputDevice)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_inputType = QtWidgets.QLabel(self)
        self.label_inputType.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_inputType.setObjectName("label_inputType")
        self.verticalLayout_3.addWidget(self.label_inputType)
        self.radioButton_single = QtWidgets.QRadioButton(self)
        self.radioButton_single.setChecked(True)
        self.radioButton_single.setObjectName("radioButton_single")
        self.inputTypeButtonGroup = QtWidgets.QButtonGroup(self)
        self.inputTypeButtonGroup.setObjectName("inputTypeButtonGroup")
        self.inputTypeButtonGroup.addButton(self.radioButton_single)
        self.verticalLayout_3.addWidget(self.radioButton_single)
        self.radioButton_double = QtWidgets.QRadioButton(self)
        self.radioButton_double.setObjectName("radioButton_double")
        self.inputTypeButtonGroup.addButton(self.radioButton_double)
        self.verticalLayout_3.addWidget(self.radioButton_double)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_first = QtWidgets.QGroupBox(self)
        self.groupBox_first.setObjectName("groupBox_first")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_first)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_firstChannel = QtWidgets.QComboBox(self.groupBox_first)
        self.comboBox_firstChannel.setObjectName("comboBox_firstChannel")
        self.verticalLayout.addWidget(self.comboBox_firstChannel)
        self.verticalLayout_4.addWidget(self.groupBox_first)
        self.groupBox_second = QtWidgets.QGroupBox(self)
        self.groupBox_second.setEnabled(False)
        self.groupBox_second.setObjectName("groupBox_second")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_second)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox_secondChannel = QtWidgets.QComboBox(self.groupBox_second)
        self.comboBox_secondChannel.setObjectName("comboBox_secondChannel")
        self.verticalLayout_2.addWidget(self.comboBox_secondChannel)
        self.verticalLayout_4.addWidget(self.groupBox_second)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBoxEnableFilter = QtWidgets.QCheckBox(self)
        self.checkBoxEnableFilter.setObjectName("checkBoxEnableFilter")
        self.verticalLayout_6.addWidget(self.checkBoxEnableFilter)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.lineEdit_energy = QtWidgets.QLineEdit(self)
        self.lineEdit_energy.setObjectName("lineEdit_energy")
        self.horizontalLayout_4.addWidget(self.lineEdit_energy)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.lineEdit_zcr = QtWidgets.QLineEdit(self)
        self.lineEdit_zcr.setObjectName("lineEdit_zcr")
        self.horizontalLayout_5.addWidget(self.lineEdit_zcr)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_entropy = QtWidgets.QLineEdit(self)
        self.lineEdit_entropy.setObjectName("lineEdit_entropy")
        self.horizontalLayout_6.addWidget(self.lineEdit_entropy)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.button_selectFile = QtWidgets.QPushButton(self)
        self.button_selectFile.setObjectName("button_selectFile")
        self.horizontalLayout_2.addWidget(self.button_selectFile)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.label_inputType_2.setText("Select the input device :")
        self.label_inputType.setText("Select the type of input :")
        self.radioButton_single.setText("Single channel")
        self.radioButton_double.setText("Two channels")
        self.groupBox_first.setTitle("First channel")
        self.groupBox_second.setTitle("Second channel")
        self.label.setText("Select the output file or folder :")
        self.lineEdit.setText(os.path.join(os.getcwd(), "data"))
        self.button_selectFile.setText("...")
        self.checkBoxEnableFilter.setText("Enable Filter")
        self.label_2.setText("Max Energy : ")
        self.label_3.setText("Max ZCR :")
        self.label_4.setText("Max Entropy :")

        self.setLayout(self.verticalLayout_5)

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
        self.button_selectFile.clicked.connect(self.select_file)

        self.audiorecorder = AudioRecorder()
        self.audiowriter = None

    # method
    def canvasUpdate(self):
        pass

    def widget_select(self):
        pass

    def pause(self):
        self.comboBox_inputDevice.setDisabled(False)
        self.radioButton_single.setDisabled(False)
        self.radioButton_double.setDisabled(False)
        self.comboBox_firstChannel.setDisabled(False)
        self.comboBox_secondChannel.setDisabled(False)
        self.lineEdit.setDisabled(False)
        self.button_selectFile.setDisabled(False)
        self.checkBoxEnableFilter.setDisabled(False)
        self.lineEdit_energy.setDisabled(False)
        self.lineEdit_zcr.setDisabled(False)
        self.lineEdit_entropy.setDisabled(False)

        if self.audiowriter:
            self.audiowriter.stop()

    def restart(self):
        self.comboBox_inputDevice.setDisabled(True)
        self.radioButton_single.setDisabled(True)
        self.radioButton_double.setDisabled(True)
        self.comboBox_firstChannel.setDisabled(True)
        self.comboBox_secondChannel.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.button_selectFile.setDisabled(True)
        self.checkBoxEnableFilter.setDisabled(True)
        self.lineEdit_energy.setDisabled(True)
        self.lineEdit_entropy.setDisabled(True)
        self.lineEdit_zcr.setDisabled(True)

        self._new_writer()

        if self.checkBoxEnableFilter.isChecked():
            try:
                szZCR = self.lineEdit_zcr.text()
                szEnergy = self.lineEdit_energy.text()
                szEntropy = self.lineEdit_entropy.text()
                zcr = float(szZCR) if szZCR.isdigit() else None
                energy = float(szEnergy) if szEnergy.isdigit() else None
                entropy = float(szEntropy) if szEntropy.isdigit() else None
                self.audiowriter.set_filter(zcr=zcr, energy=energy, entropy=entropy)
            except Exception as e:
                print(e)
        else:
            self.audiowriter.disable_filter()

    # method
    def saveState(self, settings):
        self.self.saveState(settings)

    # method
    def restoreState(self, settings):
        self.self.restoreState(settings)

    # slot
    def input_device_changed(self, index):
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

    # slot
    def first_channel_changed(self, index):
        success, index = self.audiobackend.select_first_channel(index)

        self.comboBox_firstChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage(
                "Impossible to use the selected channel as the first channel, reverting to the previous one")

    # slot
    def second_channel_changed(self, index):
        success, index = self.audiobackend.select_second_channel(index)

        self.comboBox_secondChannel.setCurrentIndex(index)

        if not success:
            # Note: the error message is a child of the settings dialog, so that
            # that dialog remains on top when the error message is closed
            error_message = QtWidgets.QErrorMessage(self)
            error_message.setWindowTitle("Input device error")
            error_message.showMessage(
                "Impossible to use the selected channel as the second channel, reverting to the previous one")

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

    # slot
    def select_file(self, clicked):
        current_directory = self.lineEdit.text()
        directory = QtWidgets.QFileDialog.getExistingDirectory(parent=None,
                                                               caption="Choose folder to save",
                                                               directory=current_directory)
        self.lineEdit.setText(directory)

    def handle_new_data(self, floatdata):
        self.data = np.zeros((1, floatdata.shape[1]))
        self.data[:] = floatdata[0, :]
        if self.audiowriter:
            self.audiowriter.write(floatdata)

    def timeout_update(self):
        # TESTING ONLY
        self.lineEdit_energy.setText("{}".format(stEnergy(self.data)))

        DELTA_TIME = 60 * 10 # 60 seconds * 10 = 10 min
        if time.time() - self.start_time > DELTA_TIME:
            self._new_writer()

    def _new_writer(self):
        self.start_time = time.time()
        name = "rec_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".wav"
        path = os.path.join(self.lineEdit.text(), name)
        self.audiowriter = self.audiorecorder.start(path,
                                 channels=1 if self.radioButton_single.isChecked() else 2,
                                 rate=SAMPLING_RATE,
                                 sampwidth=2,
                                 ratio=self.audiobackend.norm_coeff)