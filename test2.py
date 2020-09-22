import sys
from PyQt5.Qt import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QLabel, QSlider, QPushButton, QHBoxLayout, \
    QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()

        self.time_label = QLabel(self)
        self.volume_slider = QSlider(self)
        self.progress_slider = QSlider(self)
        self.sound_btn = QPushButton(self)
        self.previous_btn = QPushButton(self)
        self.play_pause_btn = QPushButton(self)
        self.next_btn = QPushButton(self)
        self.mode_btn = QPushButton(self)
        self.list_btn = QPushButton(self)
        self.list_widget = QListWidget(self)

        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.playlist = QMediaPlaylist(self)        
        self.player = QMediaPlayer(self)

        self.widget_init()
        self.layout_init()
        self.signal_init()

    def widget_init(self):
        self.time_label.setText('--/--')
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.progress_slider.setEnabled(False)
        self.progress_slider.setOrientation(Qt.Horizontal)
        self.sound_btn.setIcon(QIcon('images/sound_on.png'))
        self.previous_btn.setIcon(QIcon('images/previous.png'))
        self.play_pause_btn.setIcon(QIcon('images/play.png'))
        self.next_btn.setIcon(QIcon('images/next.png'))
        self.mode_btn.setIcon(QIcon('images/list_loop.png'))
        self.list_btn.setIcon(QIcon('images/show.png'))

        self.player.setPlaylist(self.playlist)
        self.media_list = ['/Users/louis/Downloads/music1.mp3',
                           '/Users/louis/Downloads/music2.mp4',
                           '/Users/louis/Downloads/music3.mp3']
        for m in self.media_list:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(m)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

        self.list_widget.addItems([m.split('/')[-1] for m in self.media_list])

    def layout_init(self):
        self.h1_layout.addWidget(self.progress_slider)
        self.h1_layout.addWidget(self.time_label)
        self.h2_layout.addWidget(self.volume_slider)
        self.h2_layout.addWidget(self.sound_btn)
        self.h2_layout.addWidget(self.previous_btn)
        self.h2_layout.addWidget(self.play_pause_btn)
        self.h2_layout.addWidget(self.next_btn)
        self.h2_layout.addWidget(self.mode_btn)
        self.h2_layout.addWidget(self.list_btn)

        self.all_v_layout.addLayout(self.h1_layout)
        self.all_v_layout.addLayout(self.h2_layout)
        self.all_v_layout.addWidget(self.list_widget)
        self.all_v_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        self.setLayout(self.all_v_layout)

    def signal_init(self):
        self.sound_btn.clicked.connect(lambda: self.btn_func(self.sound_btn))
        self.previous_btn.clicked.connect(lambda: self.btn_func(self.previous_btn))
        self.play_pause_btn.clicked.connect(lambda: self.btn_func(self.play_pause_btn))
        self.next_btn.clicked.connect(lambda: self.btn_func(self.next_btn))
        self.mode_btn.clicked.connect(lambda: self.btn_func(self.mode_btn))
        self.list_btn.clicked.connect(lambda: self.btn_func(self.list_btn))
        self.volume_slider.valueChanged.connect(self.volume_slider_func)
        self.list_widget.doubleClicked.connect(self.list_play_func)
        self.player.durationChanged.connect(self.get_duration_func)
        self.player.positionChanged.connect(self.get_position_func)
        self.progress_slider.sliderMoved.connect(self.update_position_func)

    def btn_func(self, btn):
        if btn == self.sound_btn:              
            if self.player.isMuted():
                self.player.setMuted(False)
                self.sound_btn.setIcon(QIcon('images/sound_on'))
            else:
                self.player.setMuted(True)
                self.sound_btn.setIcon(QIcon('images/sound_off'))

        elif btn == self.previous_btn:          
            if self.playlist.currentIndex() == 0:
                self.playlist.setCurrentIndex(self.playlist.mediaCount() - 1)
            else:
                self.playlist.previous()

        elif btn == self.play_pause_btn:      
            if self.player.state() == 1:
                self.player.pause()
                self.play_pause_btn.setIcon(QIcon('images/play.png'))
            else:
                self.player.play()
                self.play_pause_btn.setIcon(QIcon('images/pause.png'))

        elif btn == self.next_btn:              
            if self.playlist.currentIndex() == self.playlist.mediaCount() - 1:
                self.playlist.setCurrentIndex(0)
            else:
                self.playlist.next()

        elif btn == self.mode_btn:             
            if self.playlist.playbackMode() == 2:
                self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
                self.mode_btn.setIcon(QIcon('images/item_loop.png'))

            elif self.playlist.playbackMode() == 3:
                self.playlist.setPlaybackMode(QMediaPlaylist.Random)
                self.mode_btn.setIcon(QIcon('images/random.png'))

            elif self.playlist.playbackMode() == 4:
                self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
                self.mode_btn.setIcon(QIcon('images/list_loop.png'))

        elif btn == self.list_btn:             
            if self.list_widget.isHidden():
                self.list_widget.show()
                self.list_btn.setIcon(QIcon('images/show.png'))
            else:
                self.list_widget.hide()
                self.list_btn.setIcon(QIcon('images/hide.png'))

    def volume_slider_func(self, value):
        self.player.setVolume(value)
        if value == 0:
            self.sound_btn.setIcon(QIcon('images/sound_off.png'))
        else:
            self.sound_btn.setIcon(QIcon('images/sound_on.png'))

    def list_play_func(self):
        self.playlist.setCurrentIndex(self.list_widget.currentRow())
        self.player.play()
        self.play_pause_btn.setIcon(QIcon('images/pause.png'))

    def get_duration_func(self, d):
        self.progress_slider.setRange(0, d)
        self.progress_slider.setEnabled(True)
        self.get_time_func(d)

    def get_time_func(self, d):
        seconds = int(d / 1000)
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        if minutes == 0 and seconds == 0:
            self.time_label.setText('--/--')
            self.play_pause_btn.setIcon(QIcon('images/play.png'))
        else:
            self.time_label.setText('{}:{}'.format(minutes, seconds))

    def get_position_func(self, p):
        self.progress_slider.setValue(p)

    def update_position_func(self, v):
        self.player.setPosition(v)
        d = self.progress_slider.maximum() - v
        self.get_time_func(d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())