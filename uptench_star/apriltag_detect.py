##apriltag 识别，返回apriltag 二维码的内容
import cv2
import apriltag
import sys
import numpy as np
from up_controller import UpController
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

class ApriltagDetect:
##初始化
    def __init__(self):
        self.target_id = 0
        self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))  #apriltag信息
        BaseManager.register('UpController', UpController)
        manager = BaseManager()
        manager.start()
        self.up = manager.UpController()
        controller_up = Process(name="controller_up", target=self.controller_init)
        controller_up.start()
##舵机初始化
    def controller_init(self):
        print("process start")
        self.up.lcd_display("ApriltagDetect")
        motor_ids = [1,2,3,4]              #舵机id
        self.up.set_cds_mode(motor_ids,1)  #电机模式
        self.up.move_up()
 ##图像处理
    def update_frame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #灰度图像
        tags = self.at_detector.detect(gray)
        for tag in tags:
            print(tag.tag_id)
            cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
            cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
            cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
            cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom

            apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2
            target_x = apriltag_width / 2

           # if target_x < 300:
                #self.up.move_left()
            #elif target_x > 340:
                #self.up.move_right()
            #else:
                #self.up.move_up()

##作为模块时不会执行，直接编译时执行(__name__==__main__为条件)
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    ad = ApriltagDetect()
    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180) #图像反转180
        ad.update_frame(frame)
        cv2.imshow("img", frame)
        if cv2.waitKey(100) & 0xff == ord('q'):   #按'q'退出
            break
    cap.release()
    cv2.destroyAllWindows()

