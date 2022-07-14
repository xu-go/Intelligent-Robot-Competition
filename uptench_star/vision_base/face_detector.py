# -*- coding: utf-8 -*-

import cv2
import time
import numpy as np


cap = cv2.VideoCapture(0)
ret = cap.set(3, 640)  # 设置帧宽
ret = cap.set(4, 480)  # 设置帧高
font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
kernel = np.ones((5, 5), np.uint8)  # 卷积
face_cascade = cv2.CascadeClassifier('/home/pi/uptench_star/cascades/haarcascade_frontalface_default.xml')

class FaceDetector():
    def __init__(self):
        self.start_video()

    def api_init(self):
        print("process start")

    def start_video(self):
        while cap.isOpened():
            ret, frame = cap.read()
            src = frame.copy()
            result = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                result = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if faces is not None:
                if len(faces) == 1:
                    (fx, fy, fw, fh) = faces[0]
                    target_face_x = fx + fw / 2
                    offset_x = target_face_x - 640 / 2
                    offset_x = -offset_x

            cv2.imshow("result", result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    face_detector = FaceDetector()
