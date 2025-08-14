import cv2
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from detect.my_detector import Detector as my_Detector

class Camera(QObject):
    # 定义信号
    frame_ready = pyqtSignal(object)  # 原始帧信号
    detected_frame_ready = pyqtSignal(object, int)  # 检测后的帧和人数信号
    
    def __init__(self):
        super().__init__()

        self.init_camera()  # 初始化摄像头
        self.init_timer()   # 初始化定时器
        self.init_detector()    # 初始化检测器

    def init_camera(self):
        self.cap = None

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def init_detector(self):
        self.detector = my_Detector()

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)  # 打开设备默认摄像头
        self.timer.start(30)  # 30ms刷新一次

    def close_camera(self):
        if self.cap is not None:
            self.timer.stop()   # 关闭计时器，停止更新摄像头画面
            self.cap.release()
            self.cap = None

    # 更新帧并发送信号
    def update_frame(self):
        if self.cap is not None:
            flag, frame = self.cap.read()    # 读取一帧图像
            if flag:
                # 进行检测
                result_frame, people_count = self.detector.detect_frame(frame)
                # 发送原始帧
                self.frame_ready.emit(frame)
                # 发送检测帧,实施人数
                if result_frame is not None:
                    self.detected_frame_ready.emit(result_frame, people_count)
