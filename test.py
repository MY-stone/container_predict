import sys,os,time
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtCore import QUrl
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PySide2.QtWidgets import QApplication, QWidget


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.player = QMediaPlayer(self)            # 1
        self.video_widget = QVideoWidget(self)
        self.video_widget.resize(self.width(), self.height())
        self.player.setVideoOutput(self.video_widget)
        self.media_content = QMediaContent(QUrl.fromLocalFile('1.mp4'))  # 2
        self.player.setMedia(self.media_content)    # 3
        self.player.setVolume(80)                   # 4
        self.player.play()                          # 5


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())