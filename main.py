# Written by Kelvin Addy

# Imports the required modules
import sys, os, time
from ctypes import windll

from PyQt6.QtWidgets import (QApplication, QWidget, QGroupBox, QSpinBox, QLCDNumber, QLabel,
                              QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSplashScreen)
from PyQt6.QtCore import QTimer, QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon

MODES = ("Study", "Break")
BASEDIR = os.path.dirname(__file__)

STUDY_TIME = 1500000
BREAK_TIME = 300000

 
myappid = "PomodoroTimer200207"
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Pomodoro(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        """Sets up the pomodoro window"""
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(700, 350)
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Creates and arranges widgets in the pomdoro widget"""
        self.study_time = STUDY_TIME
        self.break_time = BREAK_TIME

        self.currrent_time = self.study_time
        remaining_time = self.convertTotalTime(self.currrent_time)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

        self.lcd_widget = QLCDNumber()
        self.lcd_widget.setFixedSize(450,250)
        self.lcd_widget.display(remaining_time)
        self.lcd_widget.setStyleSheet("color: red")

        self.current_mode = QLabel("Current Mode: Study")
        pomodoro_label = QLabel()
        pomodoro_label.setPixmap(QPixmap(os.path.join(BASEDIR, "images/IMG_0816.PNG")))
        pomodoro_label.setStyleSheet("color: red; font: bold italic 20px;")

        lcd_layout = QVBoxLayout()
        lcd_layout.addWidget(pomodoro_label, alignment=Qt.AlignmentFlag.AlignCenter)
        lcd_layout.addWidget(self.lcd_widget)
        lcd_layout.addWidget(self.current_mode)

        # Home tab of the pomodro timer
        home_tab = QWidget()
        self.start_button = QPushButton()
        self.start_button.setToolTip("Start Countdown")
        self.start_button.setIcon(QIcon(os.path.join(BASEDIR, "images/play.png")))
        self.start_button.setIconSize(QSize(50,50))
        self.start_button.clicked.connect(self.startCountDown)

        self.pause_button = QPushButton()
        self.pause_button.setToolTip("Pause Countdown")
        self.pause_button.setIcon(QIcon(os.path.join(BASEDIR, "images/pause-button.png")))
        self.pause_button.setIconSize(QSize(50,50))
        self.pause_button.clicked.connect(self.stopCountDown)
        
        self.reset_button = QPushButton()
        self.reset_button.setToolTip("Reset Countdown")
        self.reset_button.setIcon(QIcon(os.path.join(BASEDIR, "images/undo.png")))
        self.reset_button.setIconSize(QSize(50,50))
        self.reset_button.clicked.connect(self.resetCountDown)

        mode_groupbox = QGroupBox("Mode")
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(MODES)
        self.mode_combobox.currentTextChanged.connect(self.changeMode)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.mode_combobox)
        mode_groupbox.setLayout(mode_layout)

        home_layout = QVBoxLayout()
        home_layout.addWidget(self.start_button)
        home_layout.addWidget(self.pause_button)
        home_layout.addWidget(self.reset_button)
        home_layout.addWidget(mode_groupbox)
        home_tab.setLayout(home_layout)

        # Settings tab of the pomodor timer
        settings_tab = QWidget()
        self.break_settings = QSpinBox()
        self.break_settings.setValue(5)
        self.break_settings.setSuffix(" minutes")
        self.break_settings.setRange(5, 10)


        self.study_settings = QSpinBox()
        self.study_settings.setValue(25)
        self.study_settings.setRange(25,59)
        self.study_settings.setSuffix(" minutes")

        self.study_time_settings = self.study_settings.value() * 60 * 1000
        self.break_time_settings = self.break_settings.value() * 60 * 1000

        self.apply_settings = QPushButton("Apply")
        self.apply_settings.clicked.connect(self.applySettings)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel("Study Time"))
        settings_layout.addWidget(self.study_settings)
        settings_layout.addWidget(QLabel("Break Time"))
        settings_layout.addWidget(self.break_settings)
        settings_layout.addWidget(self.apply_settings)
        settings_tab.setLayout(settings_layout)

        tab_widget = QTabWidget()
        tab_widget.addTab(home_tab, "Home")
        tab_widget.addTab(settings_tab, "Settings")

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(lcd_layout)
        self.main_layout.addWidget(tab_widget)
        self.setLayout(self.main_layout)

    def startCountDown(self):
        """Starts the countdown"""
        self.start_button.setDisabled(True)
        self.mode_combobox.setDisabled(True)
        remaining_time = self.convertTotalTime(self.currrent_time)
        if remaining_time == "00:00":
            self.resetCountDown()
        else:
            self.timer.start(1000)
    
    def stopCountDown(self):
        """Stops the countdown"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.mode_combobox.setEnabled(True)
    
    def resetCountDown(self):
        """Resets the countdown"""
        self.checkMode()   
        self.stopCountDown()

    def updateTimer(self):
        """Updates the timer"""
        remaining_time = self.convertTotalTime(self.currrent_time)

        if remaining_time == "00:00":
            self.resetCountDown()
        else:
            self.lcd_widget.display(remaining_time)
            self.currrent_time -= 1000

    def changeMode(self, text):
        """Changes the current mode and displays the time for that mode"""
        if text == "Study":
            self.currrent_time = self.study_time
            remaining_time = self.convertTotalTime(self.currrent_time)

        elif text == "Break":
            self.currrent_time = self.break_time
            remaining_time = self.convertTotalTime(self.currrent_time)
        
        self.lcd_widget.display(remaining_time)

        self.current_mode.setText(f"Current Mode: {text}")

    def applySettings(self):
        """Applies the time settings to the countdown"""
        self.study_time_settings = self.study_settings.value() * 60 * 1000
        self.break_time_settings = self.break_settings.value() * 60 * 1000
        self.checkMode()
                

    def convertTotalTime(self, time_in_milli):
        """Calculate the time that should be displayed in the QLCDNumber widget."""
        minutes = int((time_in_milli / (1000 * 60)) % 60)
        seconds = int((time_in_milli / 1000) % 60)
        amount_of_time = "{:02d}:{:02d}".format(minutes, seconds)
        return amount_of_time
    
    def checkMode(self):
        """Checks the mode and changes the time accordinly"""
        if self.mode_combobox.currentText() == "Study":
            self.currrent_time = self.study_time_settings
            remaining_time = self.convertTotalTime(self.currrent_time)
    
        elif self.mode_combobox.currentText() == "Break":
            self.currrent_time = self.break_time_settings
            remaining_time = self.convertTotalTime(self.currrent_time)
        self.lcd_widget.display(remaining_time)

if __name__ == "__main__":
    window = QApplication(sys.argv)
    window.setWindowIcon(QIcon(os.path.join(BASEDIR, "images/pomodoro 2.png")))
    window.setStyle("Fusion")
    splash = QSplashScreen(QPixmap(os.path.join(BASEDIR, "images/pomodoro 2.png")))
    splash.show()
    time.sleep(1)
    app = Pomodoro()
    splash.finish(app)
    sys.exit(window.exec())





