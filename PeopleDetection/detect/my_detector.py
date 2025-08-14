import os
import cv2
from ultralytics import YOLO

class Detector:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.init_model()   # 初始化模型

    def init_model(self):
        self.model_path = os.path.join(self.base_dir, 'best.onnx')
        self.model = YOLO(self.model_path)
        self.conf = 0.25

    def detect_frame(self, frame):
        results = self.model(frame, conf=self.conf)
        boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes is not None else []
        people_count = len(boxes)

        # 绘制框图
        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        return frame, people_count

    def detect_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            return None, 0

        result_img, people_count = self.detect_frame(img)
        save_path = os.path.join(self.base_dir, "result.jpg")
        cv2.imwrite(save_path, result_img)

        return save_path, people_count

    def detect_video(self, video_path):
        cap = cv2.VideoCapture(video_path)  # 视频读取器
        if not cap.isOpened():
            return None

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        save_path = os.path.join(self.base_dir, "result_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))  # 视频写入器

        while True:
            flag, frame = cap.read()
            if not flag:
                break
            result_img, _ = self.detect_frame(frame)
            out.write(result_img)

        cap.release()
        out.release()
        print(f"视频检测完成，保存至: {save_path}")

        return save_path
