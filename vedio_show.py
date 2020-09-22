import sys,os,time
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtCore import QDir,QTimer,QFileInfo,Qt,QRect,QSize,QUrl
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PySide2.QtWidgets import QApplication, QWidget,QMessageBox,QPushButton,QHBoxLayout,QVBoxLayout,\
    QDesktopWidget,QSlider,QLabel,QRubberBand
from PySide2.QtGui import QIcon,QGuiApplication

#重定义QVideoWidget，实现鼠标截图
class myQVideoWidget(QVideoWidget):
    def __init__(self):
        super(myQVideoWidget,self).__init__()
        self.select_flag = False
        self.rubberband = QRubberBand(QRubberBand.Line,self)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
    
    def select_on(self):    
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.select_flag = True
    def select_off(self):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.rubberband.hide()
        self.select_flag = False

    def mousePressEvent(self,event):
        if self.select_flag :
            self.origin = event.pos()
            self.x0 = event.x()
            self.y0 = event.y()
            self.rubberband.setGeometry(QRect(self.origin,QSize()))
            self.rubberband.show()

    def mouseMoveEvent(self, event):
        if self.select_flag :
            self.rubberband.setGeometry(QRect(self.origin,event.pos()))
    def mouseReleaseEvent(self, event):
        if self.select_flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.cut_window(self.x0,self.y0,abs(self.x1-self.x0),abs(self.y1-self.y0))           
            #self.rubberband.hide()

    def cut_window(self,x0,y0,wide,high):
        pqscreen  = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), x0, y0, wide, high)
        pixmap2.save('pridict.png')

#UI播放及功能
class VedioUI(QWidget):
    def __init__(self):
        super(VedioUI, self).__init__()
        #定义视频总时长(分钟/秒钟)，当前播放到的时间(单位ms)
        self.vedio_duration_total = '00:00'
        self.vedio_duration_now = 0
        #定义窗口和播放器
        self.player = QMediaPlayer(self)
        self.video_widget = myQVideoWidget()
        self.video_widget.resize(self.width(),self.height())
        self.player.setVideoOutput(self.video_widget)

        #设置按钮
        self.start_pause_btn = QPushButton(self)
        self.stop_btn = QPushButton(self)
        self.fast_btn = QPushButton(self)
        self.back_btn = QPushButton(self)
        self.screenshot_btn = QPushButton(self)

        #设定时间块
        self.time_label = QLabel(self)
        self.time_label.setText('--/--')
        self.progress_slider = QSlider(self)
        self.progress_slider.setEnabled(False)#没有视频播放时，进度条不可使用 
        self.progress_slider.setOrientation(Qt.Horizontal)
        #进度条移动事件
        self.progress_slider.sliderMoved.connect(self.move_position)
        #设定图标
        self.start_pause_btn.setIcon(QIcon('ico/pause.png'))
        self.stop_btn.setIcon(QIcon('ico/stop.png'))
        self.fast_btn.setIcon(QIcon('ico/fast_forward.png'))
        self.back_btn.setIcon(QIcon('ico/back_forward.png'))
        self.screenshot_btn.setIcon(QIcon('ico/screenshot.png'))

        #点击链接
        self.start_pause_btn.clicked.connect(lambda: self.btn_func(self.start_pause_btn))
        self.stop_btn.clicked.connect(lambda: self.btn_func(self.stop_btn))
        self.fast_btn.clicked.connect(lambda: self.btn_func(self.fast_btn))
        self.back_btn.clicked.connect(lambda: self.btn_func(self.back_btn))
        self.screenshot_btn.clicked.connect(lambda: self.btn_func(self.screenshot_btn))
        #获取视频时间
        self.player.durationChanged.connect(self.get_duration)
        #更新进度条
        self.player.positionChanged.connect(self.update_position)

        #界面布局
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h1_layout.addWidget(self.progress_slider)
        self.h1_layout.addWidget(self.time_label)

        self.h2_layout.addWidget(self.back_btn)
        self.h2_layout.addWidget(self.start_pause_btn)
        self.h2_layout.addWidget(self.stop_btn)
        self.h2_layout.addWidget(self.fast_btn)
        self.h2_layout.addWidget(self.screenshot_btn)
        self.v_layout.addWidget(self.video_widget)
        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)
        self.v_layout.setStretch(0,1)
        self.setLayout(self.v_layout)
        #设定窗口名称及大小
        self.setWindowTitle("视频播放")
        self.resize(1024,768)
        #居中显示
        self.center()

    #文件加载与播放
    def vedio_show(self,vedio_dir = None):
        if vedio_dir:
            #添加播放文件
            self.media_content = QMediaContent(QUrl.fromLocalFile(vedio_dir))
            self.player.setMedia(self.media_content)
            #声音
            self.player.setVolume(50)
            #开始播放
            self.player.play()
        else: 
            QMessageBox.critical(self,'文件打开失败',\
                '1.文件扩展名与文件类型不匹配!\n2.路径中请勿含有中文字符！\n3.文件损坏!\n4.文件无法读取!')            
            exit(-1)
    
    #按键链接
    def btn_func(self, btn):
        pass
        if btn == self.start_pause_btn:
            # 0停止状态 1正在播放 2暂停状态
            if self.player.state() == 1:
                self.player.pause()
                self.start_pause_btn.setIcon(QIcon('ico/start.png'))
            else:
                self.player.play()
                self.start_pause_btn.setIcon(QIcon('ico/pause.png'))

        # elif btn == self.stop_btn:

        # elif btn == self.fast_btn:

        # elif btn == self.back_btn:

        elif btn == self.screenshot_btn:
            self.player.pause()
            self.start_pause_btn.setIcon(QIcon('ico/start.png'))
            QMessageBox.information(self,"提示",'请框取集装箱编号区域') 
            #鼠标修改
            self.video_widget.setCursor(Qt.CrossCursor)
            self.video_widget.select_on()
    
    #让屏幕居中
    def center(self):
        #获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        #获取窗口坐标系
        size = self.geometry()

        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft,newTop)
    
    

#将ms转化成 分钟:秒钟
    def time_conversion(self, d):
        seconds = int(d / 1000)
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        return '{}:{}'.format(minutes, seconds)

#设置QLable的时间
    def time_set(self,d_now = '00:00',d_total = '00:00'):
        if d_now == '00:00':
            self.time_label.setText('--/--')
            self.start_pause_btn.setIcon(QIcon('ico/start.png'))
        else:
            self.time_label.setText(d_now + '/' + d_total)

#获取视频总时长，并设定进度条可用
    def get_duration(self, p):
        self.progress_slider.setRange(0, p)
        self.vedio_duration_total = self.time_conversion(p)
        self.progress_slider.setEnabled(True)

#更新进度条和时间
    def update_position(self, p):
        self.progress_slider.setValue(p)
        self.vedio_duration_now = p
        self.time_set(self.time_conversion(self.vedio_duration_now),self.vedio_duration_total)

#移动滑块后更新视频，更新时间显示
    def move_position(self, p):
        self.player.setPosition(p)
        self.vedio_duration_now = p
        self.time_set(self.time_conversion(self.vedio_duration_now),self.vedio_duration_total)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = VedioUI()
    demo.vedio_show('1.mp4')
    demo.show()
    sys.exit(app.exec_())