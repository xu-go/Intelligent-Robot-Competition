##颜色检测、跟踪
import cv2
import numpy as np
import utils
from up_controller import UpController
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

font = cv2.FONT_HERSHEY_SIMPLEX

class ColorDetect:
##初始化
    def __init__(self):
        self.target_H = 0
        self.target_S = 0
        self.target_V = 0
        self.gray_frame = None
        self.hsv_frame = None
        self.target_x = None
        self.target_y = None
        self.is_detect = False

        BaseManager.register('UpController', UpController)
        manager = BaseManager()
        manager.start()
        self.up = manager.UpController()
        controller_up = Process(name="controller_up", target=self.controller_init)
        controller_up.start()
##舵机控制
    def controller_init(self):
        print("process start")
        self.up.lcd_display("ball_pick")
        motor_ids = [1,2,3,4]
        servo_ids = [5,6,7,8]
        self.up.set_cds_mode(motor_ids,1) #电机模式
        self.up.set_cds_mode(servo_ids,0) #舵机模式
 ##hsv颜色设置
    def mouse_click(self, event, x, y, flags, para):
        if event == cv2.EVENT_LBUTTONDOWN:
            print ('PIX: ', x, y)
            print ('GRAY: ', self.gray_frame[y, x])
            print ('HSV: ', self.hsv_frame[y, x])

    def btn_click(self):
        print("ha")

 ##图像处理
    def update_frame(self, img, h_min, h_max, s_min, s_max, v_min, v_max):
        src_frame = img
        result = src_frame
        self.gray_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2GRAY)
        self.hsv_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2HSV)
        low_color = np.array([h_min, s_min, v_min])
        high_color = np.array([h_max, s_max, v_max])
        mask_color = cv2.inRange(self.hsv_frame, low_color, high_color)
        mask_color = cv2.medianBlur(mask_color, 7)
        cv2.imshow("mask", mask_color)
        cnts, hierarchy = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in cnts:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)  
            cv2.putText(result, 'target', (x, y - 5), font, 0.7, (0, 0, 255), 2)
        if len(cnts) == 1 and self.is_detect:
            (x, y, w, h) = cv2.boundingRect(cnt)
            self.target_x = x+w/2
            self.target_y = y+h/2
            # print("target_x = {}, target_y = {}".format(self.target_x, self.target_y))
            # if w > 100:

           #运动控制
            if self.target_x < 360:
                self.up.set_controller_cmd(UpController.MOVE_LEFT)
            elif self.target_x >370:
                self.up.set_controller_cmd(UpController.MOVE_RIGHT)
            else:
                self.up.set_controller_cmd(UpController.PICK_UP_BALL)

            
     
def nothing(x):
    pass


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cd = ColorDetect()
    cv2.namedWindow('img')
    cv2.createTrackbar("H_MIN","img",35,180,nothing)
    cv2.createTrackbar("H_MAX","img",40,180,nothing)
    cv2.createTrackbar("S_MIN","img",100,255,nothing)
    cv2.createTrackbar("S_MAX","img",115,255,nothing)
    cv2.createTrackbar("V_MIN","img",180,255,nothing)
    cv2.createTrackbar("V_MAX","img",190,255,nothing)
    cv2.setMouseCallback("img", cd.mouse_click)

    while True:
        ret, frame = cap.read()
        r_Img = cv2.rotate(frame, cv2.ROTATE_180)#图像反转180
        h_min = cv2.getTrackbarPos("H_MIN","img")
        h_max = cv2.getTrackbarPos("H_MAX","img")
        s_min = cv2.getTrackbarPos("S_MIN","img")
        s_max = cv2.getTrackbarPos("S_MAX","img") 
        v_min = cv2.getTrackbarPos("V_MIN","img")
        v_max = cv2.getTrackbarPos("V_MAX","img")
        cd.update_frame(r_Img, h_min, h_max, s_min, s_max, v_min, v_max)
        cv2.imshow("img", r_Img)
        if cv2.waitKey(30) & 0xff == ord('q'): #按‘q‘退出
            break
        if cv2.waitKey(30) & 0xff == ord('s'): #按‘s’设置检测颜色
            cd.is_detect = True
    cap.release()
    cv2.destroyAllWindows()