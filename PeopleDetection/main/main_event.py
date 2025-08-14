import sys
import cv2
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from ui_mainwindow import Ui_MainWindow
from video.camera_read import Camera
from video.video_read import VideoPlayer
from detect.my_detector import Detector as my_Detector


class MainEvent(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_detectors()  # 初始化检测器
        self.init_camera()  # 初始化摄像头
        self.init_video_players()   # 初始化视频播放器
        self.connect_actions()  # 连接菜单动作信号

    def init_detectors(self):
        self.detector = my_Detector()  # 本地检测器

    def init_camera(self):
        # 初始化摄像头
        self.camera = Camera()

        # 连接摄像头信号
        self.camera.frame_ready.connect(self.update_original_frame)
        self.camera.detected_frame_ready.connect(self.update_detected_frame)    

    def init_video_players(self):
        self.video_player1 = VideoPlayer(self.img1)
        self.video_player2 = VideoPlayer(self.img2)

    def connect_actions(self):
        self.action_1.triggered.connect(self.handle_image_detection)    # 图片检测
        self.action_2.triggered.connect(self.handle_video_detection)    # 视频检测
        self.action_3.triggered.connect(self.handle_camera_start)   # 开启摄像头
        self.action_4.triggered.connect(self.handle_camera_stop)    # 关闭摄像头

    def handle_image_detection(self):
        self.clear_tools()
        self.clear_displays()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)"
        )
        
        if not file_path:
            return
            
        # 显示原始图片
        self.display_image(self.img1, file_path)
        
        # 执行检测并显示结果
        result_path, people_count = self.detector.detect_image(file_path)
        if result_path:
            self.display_image(self.img2, result_path)
            self.lcdPeople.display(people_count)
        else:
            print("检测失败：无法生成结果图片")
    
    def handle_video_detection(self):
        self.clear_tools()
        self.clear_displays()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv *.flv *.wmv);;所有文件 (*)"
        )
        
        if not file_path:
            return

        # 执行视频检测
        result_path = self.detector.detect_video(file_path)
        
        # 播放原始视频和检测结果视频
        self.video_player1.start(file_path)
        if result_path:
            self.video_player2.start(result_path)
        else:
            print("检测失败：无法生成结果视频")
    
    def handle_camera_start(self):
        self.clear_tools()
        self.clear_displays()

        self.camera.open_camera()
    
    def handle_camera_stop(self):
        self.camera.close_camera()
        self.clear_displays()

    # 在指定标签上显示图片
    def display_image(self, label, image_path):
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap.scaled(label.size()))

    # 清空显示区域
    def clear_displays(self):
        self.img1.clear()
        self.img2.clear()
        self.lcdPeople.display(0)

    # 重置读取设备
    def clear_tools(self):
        self.video_player1.stop()
        self.video_player2.stop()
        self.handle_camera_stop()

    # 更新摄像头画面
    def update_original_frame(self, frame):
        if frame is not None:
            self.display_cv_frame(self.img1, frame)

    # 更新检测结果画面
    def update_detected_frame(self, result_frame, people_count):
        if result_frame is not None:
            self.display_cv_frame(self.img2, result_frame)
            self.lcdPeople.display(people_count)

    # 将OpenCV帧转换为Qt图片，并在指定标签显示
    def display_cv_frame(self, label, frame):
        # BGR转RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        
        # 转换为Qt图片格式
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        label.setPixmap(pixmap.scaled(label.size()))


def main():
    app = QApplication(sys.argv)
    window = MainEvent()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()