##擂台边缘检测，当识别到apriltag 二维码位置，将二维码推下擂台
import cv2
import apriltag
import sys
import numpy as np
from up_controller import UpController
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

class ArenaContest:
##初始化
    def __init__(self):
        self.target_id = 0
        self.detect_flag = False    #检测标志位
        self.up_flag = False        #前进标志位
        self.tag_one_flag = False
        self.tag_two_flag = True
        self.stop_count = 0         #停止计数
        self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9')) #apriltag信息
        BaseManager.register('UpController', UpController)
        manager = BaseManager()
        manager.start()
        self.up = manager.UpController()
        controller_up = Process(name="controller_up", target=self.controller_init)
        controller_up.start()
        self.apriltag_width = 0
        
#舵机初始化
    def controller_init(self):
        print("process start")
        self.up.lcd_display("ArenaContest")
        self.up.set_chassis_mode(2)        #开环控制
        motor_ids = [1,2]                  #电机id
        servo_ids = [5,6,7,8]              #舵机id
        self.up.set_cds_mode(motor_ids, 1) #电机模式
        self.up.set_cds_mode(servo_ids, 0) #舵机模式
        self.up.open_edge_detect()         #边缘检测
        
        #self.up.go_up_platform()
        
#图像处理
    def update_frame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   #灰度图像
        tags = self.at_detector.detect(gray)
        for tag in tags:
            cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
            cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
            cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
            cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
            self.apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2 + tag.corners[0][0] + self.apriltag_width
        #apriltag_width = abs(tag.corners[0][0] - tag.corners[1][0]) / 2
        
        if len(tags) > 0 and self.detect_flag is not True:
            target_x = self.apriltag_width / len(tags)
            self.apriltag_width = 0
            print(target_x)
            self.stop_count += 1
            if self.stop_count == 3:
                self.up.set_controller_cmd(6)    #停止
                self.stop_count = 0
            if target_x < 280:
                # print("move_left")
                self.up.set_controller_cmd(4)    #左转
            elif target_x > 300:
                # print("move_right")
                self.up.set_controller_cmd(5)    #右转
            else:
                self.up.set_controller_cmd(6)    #停止
                #self.detect_flag = True
                self.apriltag_width = 0
##前进撞击物块
        elif self.detect_flag and self.up_flag is not True:
            print("move_up")
            self.up.set_controller_cmd(1)
            #self.up_flag = True
##旋转寻找物块S
        elif self.up_flag is not True:
            self.up.set_controller_cmd(4)

        


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    ac = ArenaContest()
    while True:
        ret, frame = cap.read()
        ac.update_frame(frame)
        cv2.imshow("img", frame)
        if cv2.waitKey(100) & 0xff == ord('q'):  #按‘q’退出
            break
    cap.release()
    cv2.destroyAllWindows()

