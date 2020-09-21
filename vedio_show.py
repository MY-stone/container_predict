import sys,os,time
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtCore import QUrl
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PySide2.QtWidgets import QApplication, QWidget,QMessageBox


class VedioUI(QWidget):
    def __init__(self):
        super(VedioUI, self).__init__()
        self.player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.video_widget.resize(self.width(), self.height())
        self.player.setVideoOutput(self.video_widget)

    def vedio_show(self,vedio_dir = None):
        if vedio_dir:
            self.media_content = QMediaContent(QUrl.fromLocalFile(vedio_dir))
            self.player.setMedia(self.media_content)    # 3
            self.player.setVolume(80)                   # 4
            self.player.play()                          # 5
        else: 
            QMessageBox.critical(self,'文件打开失败',\
                '1.文件扩展名与文件类型不匹配!\n2.路径中请勿含有中文字符！\n3.文件损坏!\n4.文件无法读取!')            
            exit(-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = VedioUI()
    demo.vedio_show('1.mp4')
    demo.show()
    sys.exit(app.exec_())