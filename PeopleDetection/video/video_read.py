import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class VideoPlayer:
    def __init__(self, label):
        self.label = label  # 设置播放区
        self.init_video_reader()    # 初始化视频读取器
        self.init_timer()   # 初始化定时器

    def init_video_reader(self):
        self.cap = None

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

    def start(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.timer.start(30)  # 30ms刷新一次

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()  # 关闭计时器，停止更新视频画面
        if self.cap is not None:
            self.cap.release()
        self.cap = None
        self.label.clear()

    def next_frame(self):
        if self.cap is not None:
            flag, frame = self.cap.read()
            if flag:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w

                qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_img)
                self.label.setPixmap(pixmap.scaled(self.label.size()))
            else:
                self.stop()  # 播放结束自动停止

