import sys,os,time
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import QVideoWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    vw=QVideoWidget()                       # 定义视频显示的widget
    vw.show()
    player.setVideoOutput(vw)                 # 视频播放输出的widget，就是上面定义的
    player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
    player.play()                               # 播放视频
    sys.exit(app.exec_())