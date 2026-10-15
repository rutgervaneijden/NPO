import PySide6.QtGui, PySide6.QtMultimedia, PySide6.QtWidgets, requests

app = PySide6.QtWidgets.QApplication([])

player = PySide6.QtMultimedia.QMediaPlayer()
output = PySide6.QtMultimedia.QAudioOutput()
player.setAudioOutput(output)
player.setSource('https://icecast.omroep.nl/3fm-bb-aac')

tray = PySide6.QtWidgets.QSystemTrayIcon()
icon = PySide6.QtGui.QPixmap()
icon.loadFromData(requests.get('https://www.3fm.nl/svg/npo_3fm_logo.svg').content)
tray.setIcon(PySide6.QtGui.QIcon(icon))
tray.setVisible(True)
tray.activated.connect(lambda: player.stop() if player.isPlaying() else player.play())

app.setQuitOnLastWindowClosed(False)
app.exec()