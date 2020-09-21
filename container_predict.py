import sys,os,time
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QMessageBox,\
                              QFileDialog,QGraphicsView,QGraphicsScene,QGraphicsPixmapItem,QTreeWidgetItem,\
                              QGraphicsRectItem,QLabel,QWidget,QRubberBand
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QDir, QTimer,QFileInfo,Qt,QRect,QSize
from PySide2.QtGui import QIcon,QPixmap,QImage,QImageReader,QPainter,QPen,QGuiApplication,QPalette
from text_recognition import predict
import cv2
from vedio_show import VedioUI


#重写GraphicsView类
class myGraphicsView(QGraphicsView):
    def __init__(self):
        super(myGraphicsView,self).__init__()
        self.scene = QGraphicsScene()
        self.setObjectName("picture_view")
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
            self.rubberband.hide()
            
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.select_flag :  
            self.cut_window(self.x0,self.y0,abs(self.x1-self.x0),abs(self.y1-self.y0))
            
    def cut_window(self,x0,y0,wide,high):
        pqscreen  = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), x0, y0, wide, high)
        pixmap2.save('pridict.png')

   
class ContainerUI():
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./container.ui')
        self.pictureFile_dir = './container_picture'
        self.ui.picture_view = myGraphicsView()
        self.ui.H2.addWidget(self.ui.picture_view)
        self.ui.H2.setStretch(0, 2)
        self.ui.H2.setStretch(1, 8)
        self.ui.video_lode.clicked.connect(self.video_lode)
        self.ui.selected.clicked.connect(self.selected)
        self.ui.predict.clicked.connect(self.predict)
        self.ui.clear.clicked.connect(self.clear)
        self.ui.tree.clicked.connect(self.onTreeClicked)
        self.preloadPicture(self.pictureFile_dir)
    
    #图片加载
    def video_lode(self):
        #图片选择
        file_dir = QFileDialog.getOpenFileName(self.ui, "打开视频",\
             QDir.currentPath(),"图片文件(*.mp4 *avi *.wmv *.flv);;所有文件(*)")[0]

        print(file_dir)
        # 判断是否正确打开文件
        if file_dir:
        # 新建窗口播放视频
            self.ui.childWindow = VedioUI()
            self.ui.childWindow.vedio_show(file_dir)
            self.ui.childWindow.show()

        else:
            QMessageBox.critical(self.ui, "错误", "文件错误或打开文件失败！")
            return
        # 在QGraphicsView上显示图像
        #下面要播放视频


    

    #区域选定
    def selected(self):
        print("集装箱区域选定被点击了")
        QMessageBox.information(self.ui,"提示",'请框取集装箱编号区域') 
        #鼠标修改       
        self.ui.picture_view.setCursor(Qt.CrossCursor)  
        self.ui.picture_view.select_on()
    #预测
    def predict(self):        
        if (self.ui.tree.currentItem()):  
            picture_dir = self.ui.tree.currentItem().text(1)
            res_txt = predict.txt_predicte('pridict.png')
            self.ui.predict_txt.clear()
            self.ui.predict_txt.append(res_txt)
            if not predict.container_check(res_txt):
                QMessageBox.information(self.ui,"提示",\
                '识别可能出现误判，请手动修改')

    #清除
    def clear(self):
        print("清除被点击了")
        self.ui.picture_view.setCursor(Qt.ArrowCursor)
        self.ui.picture_view.select_off()
        self.ui.predict_txt.clear()
    #剔除文件拓展名
    def dropExtension(self,file_name):
        return '.'.join(file_name.split('.')[:-1])
    
    def preloadPicture(self,file_dir):
        #打开文件夹并把文件信息存入列表
        file_dir = QDir(file_dir)
        file_dir.setFilter(QDir.Files)
        #以名称进行排序
        file_dir.setSorting(QDir.Name)
        file_list = file_dir.entryInfoList()
        for i in file_list:
            child = QTreeWidgetItem(self.ui.tree)
            child.setIcon(0,QIcon('./ico/picture.png'))
            child.setText(0,i.fileName())
            child.setText(1,i.absoluteFilePath())

    def onTreeClicked(self,index):
        item = self.ui.tree.currentItem()        
        file_dir = item.text(1)
        print(file_dir)
        # 判断是否正确打开文件
        if not file_dir:
            QMessageBox.critical(self.ui, "错误", "文件错误或打开文件失败！")
            return
        # 在QGraphicsView上显示图像
        self.GraphicsViewShow(file_dir)
    
    def GraphicsViewShow(self,file_dir):
        
        image = cv2.imread(file_dir)
        
        if image is None:
            QMessageBox.critical(self.ui,'文件打开失败',\
                '1.文件扩展名与文件类型不匹配!\n2.路径中请勿含有中文字符！\n3.文件损坏!\n4.文件无法读取!')
            QMessageBox.information(self.ui,"解决方法",\
                '1.尝试将导入图片路径修改为英文\n2.使用画图工具将图片格式修改\n3.尝试联系管理员')
            return

        height, width, bytesPerComponent = image.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
        QImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)

        if pixmap:
            #清除场景
            self.ui.picture_view.scene.clear()
            item = QGraphicsPixmapItem(pixmap)
            self.ui.picture_view.scene.addItem(item)
            self.ui.picture_view.setScene(self.ui.picture_view.scene)
            QMessageBox.information(self.ui,'操作成功','请继续下一步操作')
        else:
            QMessageBox.critical(self.ui,'文件打开失败',\
                '1.文件扩展名与文件类型不匹配!\n2.路径中请勿含有中文字符！\n3.文件损坏!\n4.文件无法读取!')
            QMessageBox.information(self.ui,"解决方法",\
                '1.尝试将导入图片路径修改为英文\n2.使用画图工具将图片格式修改\n3.尝试联系管理员')    


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon('./ico/logo.png'))
    ContainerUI = ContainerUI()
    ContainerUI.ui.show()
    sys.exit(app.exec_())

