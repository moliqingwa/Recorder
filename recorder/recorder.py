#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017

import os
import os.path
import platform
import sys

from PyQt5 import QtCore
# specifically import from PyQt5.QtGui and QWidgets for startup time improvement :
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QApplication, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap

from recorder.exceptionhandler import errorBox, fileexcepthook
from recorder.ui_recorder import Ui_MainWindow
from recorder.widgets.centralwidget import CentralWidget
from recorder.dockmanager import DockManager
from recorder.about import About_Dialog
from recorder.audiobuffer import AudioBuffer
from recorder.audiobackend import AudioBackend

# the display timer could be made faster when the processing
# power allows it, firing down to every 10 ms
SMOOTH_DISPLAY_TIMER_PERIOD_MS = 10
SLOW_TIMER_PERIOD_MS = 1000

class Recorder(QMainWindow, ):
    def __init__(self, logger):
        QMainWindow.__init__(self)

        # exception hook that logs to console, file, and display a message box
        self.errorDialogOpened = False
        sys.excepthook = self.excepthook

        # logger
        self.logger = logger

        self.audiobuffer = AudioBuffer(self.logger)

        # Initialize the audio backend
        self.audiobackend = AudioBackend(self.logger)

        # signal containing new data from the audio callback thread, processed as numpy array
        self.audiobackend.new_data_available.connect(self.audiobuffer.handle_new_data)

        # Setup the user interface
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.about_dialog = About_Dialog(self)

        self.centralLayout = QVBoxLayout(self.ui.centralwidget)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralwidget = CentralWidget(self.ui.centralwidget, self.logger, "central_widget", 0)
        self.centralLayout.addWidget(self.centralwidget)

        # toolbar clicks
        self.ui.actionStart.triggered.connect(self.action_start_triggered)
        self.ui.actionAbout.triggered.connect(self.action_about_triggered)

        # restore the settings and widgets geometries
        self.restoreAppState()

        # this timer is used to update widgets that just need to display as fast as they can
        self.display_timer = QtCore.QTimer()
        self.display_timer.setInterval(SMOOTH_DISPLAY_TIMER_PERIOD_MS)  # constant timing

        # slow timer
        self.slow_timer = QtCore.QTimer()
        self.slow_timer.setInterval(SLOW_TIMER_PERIOD_MS)  # constant timing

        # timer ticks
        self.display_timer.timeout.connect(self.centralwidget.canvasUpdate)
        self.dockmanager = DockManager(self, self.logger)
        self.dockmanager.new_dock(timer=self.slow_timer)
        self.display_timer.timeout.connect(self.dockmanager.canvasUpdate)

        # start timers
        # self.action_start_triggered()

        self.logger.push("Init finished, entering the main loop")

    # exception hook that logs to console, file, and display a message box
    def excepthook(self, exception_type, exception_value, traceback_object):
        gui_message = fileexcepthook(exception_type, exception_value, traceback_object)

        # we do not want to flood the user with message boxes when the error happens repeatedly on each timer event
        if not self.errorDialogOpened:
            self.errorDialogOpened = True
            errorBox(gui_message)
            self.errorDialogOpened = False

    # event handler
    def closeEvent(self, event):
        self.audiobackend.close()
        self.saveAppState()
        event.accept()

    # slot
    def action_about_triggered(self):
        self.about_dialog.show()

    # slot
    def action_start_triggered(self):
        if self.display_timer.isActive():
            self.logger.push("Timer stop")
            self.display_timer.stop()
            self.slow_timer.stop()
            self.ui.actionStart.setText("Start")
            self.audiobackend.pause()
            self.centralwidget.pause()
            self.dockmanager.pause()
        else:
            # self.logger.push("check folder before Timer start")
            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Question)
            # msg.setText("The folder is not empty, are you sure to use current folder ?")
            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # ret_val = msg.exec()
            # if ret_val == QMessageBox.Ok:
            #     pass
            # else:
            #     pass
            #
            self.logger.push("Timer start")
            self.display_timer.start()
            self.slow_timer.start()
            self.ui.actionStart.setText("Stop")
            self.audiobackend.restart()
            self.centralwidget.restart()
            self.dockmanager.restart()

    # method
    def saveAppState(self):
        settings = QtCore.QSettings("Recorder", "Recorder")

    # method
    def restoreAppState(self):
        settings = QtCore.QSettings("Recorder", "Recorder")


def main():
    print("Platform is %s (%s)" % (platform.system(), sys.platform))

    if platform.system() == "Windows":
        print("Applying Windows-specific setup")
        # On Windows, redirect stderr to a file
        import imp
        import ctypes
        if (hasattr(sys, "frozen") or  # new py2exe
                hasattr(sys, "importers") or  # old py2exe
                imp.is_frozen("__main__")):  # tools/freeze
            sys.stderr = open(os.path.expanduser("~/recorder.exe.log"), "w")
        # set the App ID for Windows 7 to properly display the icon in the
        # taskbar.
        myappid = 'recorder.current'  # arbitrary string
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            print("Could not set the app model ID. If the platform is older than Windows 7, this is normal.")

    app = QApplication(sys.argv)

    if platform.system() == "Darwin":
        if hasattr(sys, "frozen"):  # py2app
            sys.stdout = open(os.path.expanduser("~/recorder.out.txt"), "w")
            sys.stderr = open(os.path.expanduser("~/recorder.err.txt"), "w")

        print("Applying Mac OS-specific setup")
        # help the py2app-packaged application find the Qt plugins (imageformats and platforms)
        pluginsPath = os.path.normpath(os.path.join(QApplication.applicationDirPath(), os.path.pardir, 'PlugIns'))
        print("Adding the following to the Library paths: " + pluginsPath)
        QApplication.addLibraryPath(pluginsPath)

    # Splash screen
    pixmap = QPixmap(":/images/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    splash.showMessage("Initializing the audio subsystem")
    app.processEvents()

    # Logger class
    from recorder import logger
    logger = logger.Logger()

    window = Recorder(logger)
    window.show()
    splash.finish(window)

    profile = "no"  # "python" or "kcachegrind" or anything else to disable

    if len(sys.argv) > 1:
        if sys.argv[1] == "--python":
            profile = "python"
        elif sys.argv[1] == "--kcachegrind":
            profile = "kcachegrind"
        elif sys.argv[1] == "--no":
            profile = "no"
        else:
            print("command-line arguments (%s) not recognized" % sys.argv[1:])

    if profile == "python":
        import cProfile
        import pstats

        cProfile.runctx('app.exec_()', globals(), locals(), filename="recorder.cprof")

        stats = pstats.Stats("recorder.cprof")
        stats.strip_dirs().sort_stats('time').print_stats(20)
        stats.strip_dirs().sort_stats('cumulative').print_stats(20)

        sys.exit(0)
    elif profile == "kcachegrind":
        import cProfile
        import lsprofcalltree

        p = cProfile.Profile()
        p.run('app.exec_()')

        k = lsprofcalltree.KCacheGrind(p)
        with open('cachegrind.out.00000', 'wb') as data:
            k.output(data)

        sys.exit(0)
    else:
        sys.exit(app.exec_())
