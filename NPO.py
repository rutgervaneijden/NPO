from PySide6.QtCore import QByteArray
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from urllib.request import urlopen

class Tray(QSystemTrayIcon):
    def __init__(self, app: QApplication, stations: list):
        super().__init__()
        self.app = app
        self.stations = stations
        self.output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.output)
        self.menu = QMenu()
        for name, logo, url in self.stations:
            pixmap = QPixmap()
            pixmap.loadFromData(urlopen(logo).read())
            action = QAction(QIcon(pixmap), name, self)
            action.triggered.connect(lambda checked=False, logo=logo, url=url: self.on_station_triggered(logo, url))
            self.menu.addAction(action)
        self.menu.addSeparator()
        bmac_action = QAction('Buy Me a Coffee', self)
        # bmac_action.triggered.connect()
        self.menu.addAction(bmac_action)
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.app.quit)
        self.menu.addAction(quit_action)
        self.activated.connect(self.on_tray_activated)
        pixmap = QPixmap()
        pixmap.loadFromData(urlopen('https://prod.cc.bijnpo.nl/assets/icons/npo-logo.svg').read())
        self.setIcon(QIcon(pixmap))

    def on_station_triggered(self, logo, url):
        pixmap = QPixmap()
        pixmap.loadFromData(urlopen(logo).read())
        self.setIcon(QIcon(pixmap))
        self.player.setSource(url)
        self.player.play()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger: # Left-click
            if self.player.source().isEmpty():
                pos = self.geometry().bottomLeft()
                self.menu.popup(pos)
            else:
                self.player.stop() if self.player.isPlaying() else self.player.play()
        elif reason == QSystemTrayIcon.ActivationReason.Context: # Right-click
            pos = self.geometry().bottomLeft()
            self.menu.popup(pos)

if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    stations = [
        ('Radio 1', 'https://www.nporadio1.nl/svg/npo_radio1_logo.svg', 'https://icecast.omroep.nl/radio1-bb-aac'),
        ('Radio 2', 'https://www.nporadio2.nl/svg/npo_radio2_logo.svg', 'https://icecast.omroep.nl/radio2-bb-aac'),
        ('3FM', 'https://www.3fm.nl/svg/npo_3fm_logo.svg', 'https://icecast.omroep.nl/3fm-bb-aac'),
        ('Klassiek', 'https://www.npoklassiek.nl/svg/npo-klassiek-logo.svg', 'https://icecast.omroep.nl/radio4-bb-aac'),
        ('Radio 5', 'https://www.nporadio5.nl/svg/npo_radio5_logo.svg', 'https://icecast.omroep.nl/radio5-bb-aac'),
        ('FunX', 'https://www.funx.nl/svg/funx_logo.svg', 'https://icecast.omroep.nl/funx-bb-aac'),
    ]
    tray = Tray(app, stations)
    tray.show()
    app.exec()