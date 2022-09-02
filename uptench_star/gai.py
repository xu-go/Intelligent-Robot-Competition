from fcntl import FD_CLOEXEC
import threading
from turtle import fd
from typing import Tuple

from cv2 import circle
from up_controller import UpController
import time
import cv2
import apriltag
import sys
import numpy as np
import math
import mpu6500
import uptech
import random

frame = cv2.VideoCapture(-1)
frame.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))  # 创建一个apriltag检测器

class main_demo:
    #前 右 后 左 红外定义
    FD = 490
    RD = 560
    BD = 750
    LD = 500
    # 倾斜计时
    na = 0
    # 推箱子计时
    nb = 0
    # 旋转计时
    nc = 0
    # 前搁浅计时
    nd = 0
    # 后搁浅计时
    ne = 8
    # 倾斜
    qx = 0
    #设置
    def __init__(self):
        self.version = "1.0"
        self.servo_speed = 1023
        self.controller = UpController()
        self.controller.lcd_display("MatchDemo")
        # 设置
        self.controller.set_chassis_mode(0)
        motor_ids = [1, 2]
        servo_ids = [5, 6, 7, 8]
        self.controller.set_cds_mode(motor_ids, 1)
        self.controller.set_cds_mode(servo_ids, 0)
        # self.mpu6500 = mpu6500.Read_mpu6500()
        # self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        # self.apriltag_width = 0
        # self.tag_id = -1
        # apriltag_detect = threading.Thread(target = self.apriltag_detect_thread)
        # apriltag_detect.setDaemon(True)
        # apriltag_detect.start()
        
    #视觉
    def apriltag_detect_thread(self, img):
        #尝试
        try:
            img=img[100:]  # 裁剪图像
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            tags = at_detector.detect(gray)  # 进行apriltag检测，得到检测到的apriltag的列??
            key_biggest_s = [-1, -1, -1]  # 存储画面中最大的三个面积

            for tag in tags:
                x0, y0 = tuple(tag.corners[0].astype(int))  # 获取二维码的角点
                x1, y1 = tuple(tag.corners[1].astype(int))
                x2, y2 = tuple(tag.corners[2].astype(int))
                x3, y3 = tuple(tag.corners[3].astype(int))

            
                #计算面积（该公式为已知三个点坐标求三角形面积公式??
                s_ur=(x0*y1-x0*y2+x1*y2-x1*y0+x2*y0-x1*y1)
                s_dr = (x1*y2-x1*y3+x2*y3-x2*y1+x3*y1-x2*y2)
                s_dl = (x2*y3-x2*y0+x3*y0-x3*y2+x0*y2-x3*y3)
                s_ul = (x3*y0-x3*y1+x0*y1-x0*y3+x1*y3-x0*y0)

                if (tag.tag_id) < 3:  # 将最大的面积存储到key_longest_side??
                    if s_ul >= s_ur and s_ul >= s_dr and s_ul >= s_dl:  # 获取最大面??
                        key_biggest_s[tag.tag_id] = s_ul
                    elif s_ur >= s_dr and s_ur >= s_dl and s_ur >= s_ul:
                        key_biggest_s[tag.tag_id] = s_ur
                    elif s_dr >= s_ul and s_dr >= s_ur and s_dr >= s_dl:
                        key_biggest_s[tag.tag_id] = s_dr
                    elif s_dl >= s_ul and s_dl >= s_ur and s_dl >= s_dr:
                        key_biggest_s[tag.tag_id] = s_dl
                else:
                    print("The id not in list!")

            key_index = -1
            if key_biggest_s[0] >= key_biggest_s[1] and key_biggest_s[0] >= key_biggest_s[2]:
                key_index = 0
            elif key_biggest_s[1] >= key_biggest_s[0] and key_biggest_s[1] >= key_biggest_s[2]:
                key_index = 1
            elif key_biggest_s[2] >= key_biggest_s[0] and key_biggest_s[2] >= key_biggest_s[1]:
                key_index = 2
            print(key_biggest_s)
            for tag in tags:
                if tag.tag_id == key_index:
                    print(tag.tag_id)
                    return tag.tag_id
        # #结束时通过
        # finally:
        #     pass
        except BaseException:
            pass
       
    # 默认上台动作，抬起铲子?
    def default_platform(self):
        self.controller.up.CDS_SetAngle(5, 635, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 340, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)

    # 放下前爪
    def pack_up_ahead(self):
        self.controller.up.CDS_SetAngle(5, 230, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)

    # 放下后爪
    def pack_up_behind(self):
        self.controller.up.CDS_SetAngle(6, 340, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 620, self.servo_speed)

    # 上台后爪子的状态，放下铲子
    def shovel_state(self):
        self.controller.up.CDS_SetAngle(5, 258, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 340, self.servo_speed)  #340
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)  #700
        self.controller.up.CDS_SetAngle(8, 620, self.servo_speed)  #620
    
    #只收前爪子，然后不全收完
    def front_paw_half(self):
        self.controller.up.CDS_SetAngle(5, 450, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 508, self.servo_speed)
    
    #收前爪
    def front_paw(self):
        self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)

    #收后爪
    def back_paw(self):
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)

    # 前上台动作
    def go_up_ahead_platform(self):
        # self.controller.move_cmd(0, 0)
        # time.sleep(0.1)
        # 爪子抬起
        self.default_platform()
        time.sleep(0.2)
        self.controller.move_cmd(900, 900)
        time.sleep(0.6)
        # 支前爪
        self.controller.move_cmd(0, 0)
        self.controller.up.CDS_SetAngle(5, 240, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 710, self.servo_speed)
        # self.pack_up_ahead()
        time.sleep(0.5)
        # 收起前爪
        self.controller.move_cmd(800,800)
        time.sleep(0.5)
        # self.controller.move_cmd(0,0)
        # time.sleep(0.3)
        self.controller.move_cmd(800,700)
        time.sleep(0.2)
        #self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        #self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)
        # 支后爪
        #time.sleep(0.5)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(6, 300, self.servo_speed)#320
        self.controller.up.CDS_SetAngle(8, 680, self.servo_speed)#660
        time.sleep(0.8)
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)
        # 默认上台
        #self.controller.up.CDS_SetAngle(6, 700, self.servo_speed)
        #self.controller.up.CDS_SetAngle(8, 300, self.servo_speed)
        # time.sleep(0.5)
        #self.shovel_state()
        self.controller.move_cmd(700,700)
        time.sleep(0.1)
        #self.default_platform()

    # 检测是否在台上-返回状态
    def paltform_detect(self):
        #更新传感器数值
        self.controller.edge_test_func()
        angle_sensor = self.controller.adc_data[0]
        ahead_ad = 1 if self.controller.adc_data[1] < 1000 else 0
        right_ad = 1 if self.controller.adc_data[2] < 1000 else 0
        behind_ad = 1 if self.controller.adc_data[3] < 1000 else 0
        left_ad = 1 if self.controller.adc_data[4] < 1000 else 0
        left_ahead_io = 1 if self.controller.io_data[0] == 0 else 0
        right_ahead_io = 1 if self.controller.io_data[1] == 0 else 0
        right_behind_io = 1 if self.controller.io_data[2] == 0 else 0
        left_behind_io = 1 if self.controller.io_data[3] == 0 else 0
        sum_down = ahead_ad + right_ad + behind_ad + left_ad
        sum_up = left_ahead_io + left_behind_io + right_ahead_io + right_behind_io
        # if angle_sensor >= 1600 and angle_sensor < 2100:
        if sum_up < 2:
            # 在台下
            return 0
        elif sum_down == 0 and sum_up == 0:
            return 5
        else:
            # 在台上
            return 1
        # elif angle_sensor < 1600:
        #     # 卡在擂台左侧在地面右侧在擂台
        #     return 3
        # else:
        #     # 卡在擂台右侧在地面左侧在擂台
        #     return 4

    #更新底部的光电
    def bash_fence(self):
        #更新传感器数值
        self.controller.edge_test_func()
        # 底部前方红外光电
        ad1 = self.controller.adc_data[1]
        # 底部右侧红外光电
        ad2 = self.controller.adc_data[2]
        # 底部后方红外光电
        ad3 = self.controller.adc_data[3]
        # 底部左侧红外光电
        ad4 = self.controller.adc_data[4]

        # 前红外测距传感器
        ad5 = self.controller.adc_data[5]
        # 右红外测距传感器
        ad6 = self.controller.adc_data[6]
        # 后红外测距传感器
        ad7 = self.controller.adc_data[7]
        # 左红外测距传感器
        ad8 = self.controller.adc_data[8]
        
        #前对擂台且没有障碍物
        if ad1 < 1000 and ad5 < self.FD:
            return 0
        #后对擂台或者擂台上有障碍物或者敌人
        elif ad1 < 1000 and ad5 > self.FD:
            return 1
        #其他状态
        else:
            return 2

    #上方光电检测，检测边缘
    def edge_detect(self):
        #更新传感器数值
        self.controller.edge_test_func()
        # 左前红外光电传感器
        io_0 = self.controller.io_data[0]
        # 右前红外光电传感器
        io_1 = self.controller.io_data[1]
        # 右后红外光电传感器
        io_2 = self.controller.io_data[2]
        # 左后红外光电传感器
        io_3 = self.controller.io_data[3]

        
        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #在擂台上，未检测到边缘
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #左前检测到边缘
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #右前检测到边缘
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            #右后检测到边缘
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #左后检测到边缘
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #前方检测到边缘
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            #后方检测到边缘
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #左方检测到边缘
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            #右方检测到边缘
            return 8
        else:
            return 102

    #在边缘做对应的动作
    def edge_action(self):
        #更新传感器数器
        self.controller.edge_test_func()
        # 左前红外光电传感器
        io_0 = self.controller.io_data[0]
        # 右前红外光电传感器
        io_1 = self.controller.io_data[1]
        # 右后红外光电传传感器
        io_2 = self.controller.io_data[2]
        # 左后红外光电传感器
        io_3 = self.controller.io_data[3]
        
        t = time.time()
        
        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #在擂台上，未检测到边缘
            if self.edge_detect() == 0 :
                self.controller.move_cmd(600, 600)
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #左前检测到边缘
            #未检测到边缘后退
            while((time.time()-t)<0.5 and self.edge_detect != 0):
                self.controller.move_cmd(-800, -800)
            #更新t
            t = time.time()
            #未检测到边缘旋转
            while((time.time()-t)<0.5 and self.edge_detect == 1):
                self.controller.move_cmd(800, -800)
            self.controller.move_cmd(800, 800)
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #右前检测到边缘
            #未检测到边缘后退
            while((time.time()-t)<0.5 and self.edge_detect == 2):
                self.controller.move_cmd(-800, -800)
            t = time.time()
            #未检测到边缘旋转
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(-800, 800)
            time.sleep(0.5)
            self.controller.move_cmd(800, 800)
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            #右后检测到边缘
            #未检测到边缘后退
            while((time.time()-t)<0.5 and self.edge_detect == 3):
                self.controller.move_cmd(950, 950)
            t = time.time()
            #未检测到边缘旋转
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(850, -750)
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #左后检测到边缘
            #未检测到边缘后退
            while((time.time()-t)<0.5 and self.edge_detect == 4):
                self.controller.move_cmd(950, 950)
            t = time.time()
            #未检测到边缘旋转
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(-750, 850)
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #前方检测到边缘
            while((time.time()-t)<0.5 and self.edge_detect == 5):
                self.controller.move_cmd(-800, -800)
            time.sleep(0.2)
            t = time.time()
            #随机数的种子生成
            random.seed(t)
            a = random.randint(1,2)
            if a == 1:
                #左转
                self.controller.move_cmd(-800, 800)
                time.sleep(0.2)
            else:
                #右转
                self.controller.move_cmd(800, -800)
                time.sleep(0.2)
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            #后方检测到边缘
            while((time.time()-t)<0.5 and self.edge_detect == 6):
                self.controller.move_cmd(950, 950)
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #左方检测到边缘
            self.controller.move_cmd(950, -950)
            time.sleep(0.2)
            self.controller.move_cmd(950, 950)
            time.sleep(0.2)
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            #右方检测到边缘
            self.controller.move_cmd(-950, 950)
            time.sleep(0.2)
            self.controller.move_cmd(950, 950)
            time.sleep(0.2)
            return 8
        else:
            #不知道什么情况，乱动
            self.randomm()
            return 102

    # 敌人检测
    def enemy_detect(self):
        #更新传感器数值
        self.controller.edge_test_func()
        # 底部前方红外光电传感器
        ad1 = self.controller.adc_data[1]
        # 底部右侧红外光电传感器
        ad2 = self.controller.adc_data[2]
        # 底部后方红外光电传感器
        ad3 = self.controller.adc_data[3]
        # 底部左侧红外光电传感器
        ad4 = self.controller.adc_data[4]
        # 前红外测距传感器
        ad5 = self.controller.adc_data[5]

        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:
            # 无敌人
            return 0
        #前方检测到有东西
        elif (ad1 < 100 ) :
            if (ad5 < self.FD):
                #障碍物
                return 11
            else:
                return 1
        elif ad3 < 100 :
            # 后方有敌人或棋子
            return 2
        elif (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 > 100) or (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 < 100):      
            # 右侧有敌人或棋子 or 左右两侧都有障碍
            return 3
        elif ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 < 100:
            # 左侧有敌人或棋子
            return 4
        else:
            return 103    

    #随机运动
    def randomm(self):
        t = time.time()
        #随机数的种子生成
        random.seed(t)
        #放爪子
        a = random.randint(1,2)
        #运行方向
        b = random.randint(1,4)
        if a == 1:
            #放后爪
            self.pack_up_behind()
        elif a == 2:
            #放前爪
            self.pack_up_ahead()
        if b == 1:
            #左转
            self.controller.move_cmd(-700, 700)
            time.sleep(0.6)
        elif b == 2:
            #右转
            self.controller.move_cmd(700, -700)
            time.sleep(0.6)
        elif b == 3:
            #前进
            self.controller.move_cmd(600, 600)
            time.sleep(0.6)
        elif b == 4:
            #后退
            self.controller.move_cmd(600, 600)
            time.sleep(0.6)

    def randommm(self):
        t = time.time()
        #随机数的种子生成
        random.seed(t)
        #放爪子
        a = random.randint(1,2)
        #运行方向
        b = random.randint(1,4)
        if a == 1:
            #放后爪
            self.back_paw()
        elif a == 2:
            #放前爪
            self.pack_up_ahead()
        if b == 1:
            #左转
            self.controller.move_cmd(-900, 900)
            time.sleep(0.6)
        elif b == 2:
            #右转
            self.controller.move_cmd(900, -900)
            time.sleep(0.6)
        elif b == 3:
            #前进
            self.controller.move_cmd(900, 900)
            time.sleep(0.6)
        elif b == 4:
            #后退
            self.controller.move_cmd(900, 900)
            time.sleep(0.6)

    #检测前方是否是悬崖   1是右障碍物，说明是在台上未检测到悬崖，否则检测到悬崖
    def cliff(self):
        #更新传感器数值
        self.controller.edge_test_func()
        # 铲子左
        io_l = self.controller.io_data[4]
        # 铲子右
        io_r = self.controller.io_data[5]
        if io_l == 1 and io_r == 0:
            #右前检测到悬崖
            return 1
        if io_l == 0 and io_r == 1:
            #左前检测到悬崖
            return 2
        if io_l == 0 and io_r == 0:
            #正前方检测到悬崖
            return 3
        else:
            #在台上一切正常
            return 4

    def start_match(self):
        #初始化，收起四个铲子
        self.default_platform()    
        time.sleep(1)

        ##软开关
        ad8 = self.controller.adc_data[8]
        ad6 = self.controller.adc_data[6]
        while(ad8 <= 1500 and ad6 <= 1500):
           # print("我方队伍颜色")
            ad8 = self.controller.adc_data[8]
            ad6 = self.controller.adc_data[6]
        #左边测距黄方
        if(ad8 > 1500):
            print("我方为黄方")
            our_side = 0
        #右侧测距蓝方
        if(ad6 > 1500):
            print("我方为蓝方")
            our_side = 1


        #判断是不是大量重复一个判断那极有可能是卡住了
        repeat = 0
        #状态储存
        state_storage = 0
        #台下其他状态的次数
        taixia = 0
        taixia_1 = 0
        # ##前进一段距离
        # self.controller.move_cmd(900, 900)
        # time.sleep(0.4)
        # #右转
        # self.controller.move_cmd(600, 900)
        # time.sleep(0.2)
        # ##前上台  
        #self.go_up_ahead_platform()
        # #右转抢占中间能量块
        #self.controller.move_cmd(-500,900)
        #time.sleep(0.1)

        #开始死循环，判断是不是在台下
        while 1:
            #检测是否在台上
            # 0为在台下 1为在台上 返回5 8个光电都为检测未到浮空
            stage = self.paltform_detect()
            #在台下,一级判断
            if stage == 0:
                #收爪子
                self.default_platform()
                print("stage",stage,"在台下")
                #下台了然后开始判断有没有上台来判断是不是再台上是不是
                not_on_stage = 1
                #重复值初始化
                repeat = 0
                while (not_on_stage == 1):
                    #收爪子
                    self.default_platform()
                    #更新底部的光电
                    basee = self.bash_fence()
                    print("底部的光电状态?",basee)
                    print("是否未彻底登上台,1是,0否",not_on_stage)
                    
                    #前方对擂台
                    if basee == 0:
                        #台下状态其他状态
                        taixia = 0
                        #前进以后
                        print("前方对擂台?")
                        self.controller.move_cmd(900, 900)
                        time.sleep(0.3)
                        #前上台?
                        self.go_up_ahead_platform()
                        #定时
                        t = time.time()
                        #上台了，可以更改在台下的值了，跳出循环
                        while((time.time() - t < 1.0) and (self.edge_detect() != 0)):
                            print("卡在上台这一步了")
                            #未上台随机运动
                            self.randommm()
                        #在判断有没有在台上，要四个全亮才算
                        if(self.edge_detect() == 0):
                            print("跳出上台程序")
                            #上台了可以跳出循环了给其赋一
                            not_on_stage = 0
                            

                    else:
                        print("其他状态?")
                        #后退
                        self.controller.move_cmd(-700, -700)
                        time.sleep(0.1)
                        #收爪?
                        self.default_platform() 
                        #读取时间,超时就向?
                        t = time.time()
                        #超时或前方未检测到擂台无敌人?
                        while (self.bash_fence() != 0):
                            if ((time.time()-t)<0.5):
                                #旋转
                                self.controller.move_cmd(-800, 800)
                            else :
                                self.controller.move_cmd(800, 800)
                                time.sleep(0.1)
                                #更新t?
                                t = time.time()
                            #更新在台下的状态
                            print("在台下的次数",taixia_1)
                            # if taixia == 1:
                            #     taixia_1 = taixia_1 + 1
                            # if taixia_1 >= 20:
                            #     print("其他运动太长开始随机?")
                            #     #随机运动
                            #     self.randomm()
                            #     taixia_1 = 0
                            self.paltform_detect()
                            taixia = 1

            #在台上,一级判断
            elif stage == 1:
                print("在台上")
                #一个变量
                p = 0
                #放下铲子
                self.pack_up_ahead()
                #self.pack_up_behind()
                self.back_paw()  
                #读取边缘检测
                edge = self.edge_detect()
                nnn = time.time()
                #如果在台上未检测到边缘开始死循环减少步骤时间1.5级判断
                while(edge == 0 and p == 0):
                    print("未检测到边缘")
                    #重复值为0初始0
                    repeat = 0
                    #悬崖检测
                    clif = self.cliff()
                    #更新边缘
                    edge = self.edge_detect()
                    # #放下铲子
                    # self.pack_up_ahead()
                    # self.pack_up_behind()
                    ##避障未检测到悬崖,二级判断
                    while(self.cliff() == 4):
                        #定义初始速度
                        v1 = 0
                        #定义一个初始的时间
                        t = time.time()
                        #更新边缘
                        edge = self.edge_detect()
                        #不是在台下
                        if edge != 0:
                            p = 1
                            break

                        #在台上    
                        else:
                            #更新底层的光电判断是否有障碍物
                            enemy = self.enemy_detect()

                            #未检测到障碍物三级判断
                            if enemy == 0:
                                #计算开启的时间
                                now_time = time.time() - t
                                # #如果超过0.06秒内满足线性关系
                                # if now_time < 0.06:
                                #     v = 900 - 5000 * now_time * now_time
                                #     if v > 790 :
                                #         v = 790
                                #     print("满足线性关系v = ",int(v))
                                #     self.controller.move_cmd(int(v), int(v))
                                #如果时间差在0.02s内快速
                                if now_time < 0.02:
                                    #前进
                                    #print("快前进")
                                    self.controller.move_cmd(630, 630)
                                #如果时间差在0.05内可以稍微慢速
                                elif now_time >= 0.02 and now_time < 0.05:
                                    #慢前进
                                    #print("慢前进")
                                    self.controller.move_cmd(530, 530)
                                #超时了近乎停止
                                else:
                                    #倒退
                                    self.controller.move_cmd(400, 400)
                                    #print("前进超时!!!")
                                    time.sleep(0.03)
                                #更新t
                                t = time.time()
                            
                            

                            #前方有敌人、能量块或者炸弹三级判断
                            elif enemy == 1:
                                #测试用的比赛注释
                                # self.controller.move_cmd(750, 750)
                                # print("#前方有敌人、能量块或者炸弹id = ")
                                #开启摄像头
                                ret,img = frame.read()
                                print(ret)
                                #给id设个值防止其报错
                                id = -1
                                id = self.apriltag_detect_thread(img)
                                #判断不同id的状态
                                print("#前方有敌人、能量块或者炸弹id = ",id)
                                #能量块时四级判断
                                #蓝方能量块为1，黄方能量块为2”，中立能量块为0,别推自己的能量块
                                #our_side = 0黄方
                                #our_side = 1蓝方
                                #决赛视频时能量块为1,炸弹为0
                                if id == 1:
                                    print("决赛能量块")
                                    #把铲子稍微抬起一点可以确保把3KG的能量块推下台
                                    #前进,可能会掉下去,注意
                                    self.controller.move_cmd(660, 660)
                                
                                if id == 0:
                                    print("决赛炸弹")
                                    #后退但是要检测是否到边缘
                                    t = time.time()
                                    #未超时和未检测到边缘
                                    while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                        #后退
                                        self.controller.move_cmd(-750, -750)
                                    #转弯
                                    #边缘更新
                                    n = self.edge_detect()
                                    #不在边缘转弯五级判断
                                    if(n == 0):
                                        self.controller.move_cmd(750, -750)
                                        time.sleep(0.8)
                                    #其他情况交给你了五级判断
                                    else:
                                        #边缘动作
                                        self.edge_action()

                                # #蓝方能量1
                                # if id == 1 :
                                #     print("蓝方能量块")
                                #     #把铲子稍微抬起一点可以确保把3KG的能量块推下台
                                #     #前进,可能会掉下去,注意
                                #     #判断是否是黄色
                                #     if our_side == 0:
                                #         self.controller.move_cmd(600, 600)
                                #     #炸弹
                                #     else:
                                #         print("蓝方炸弹")
                                #         #后退但是要检测是否到边缘
                                #         t = time.time()
                                #         #未超时和未检测到边缘
                                #         while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                #             #后退
                                #             self.controller.move_cmd(-750, -750)
                                #         #转弯
                                #         #边缘更新
                                #         n = self.edge_detect()
                                #         #不在边缘转弯五级判断
                                #         if(n == 0):
                                #             self.controller.move_cmd(750, -750)
                                #             time.sleep(0.8)
                                #         #其他情况交给你了五级判断
                                #         else:
                                #             #边缘动作
                                #             self.edge_action()
                                # #炸弹时四级判断
                                # #中立能量块0，决赛的炸弹
                                # elif id == 0 :
                                #     print("中立能量块")
                                #     #把铲子稍微抬起一点可以确保把2.5KG的能量块推下台
                                #     #前进,可能会掉下去,注意
                                #     self.controller.move_cmd(800, 800)
                                # #黄方能量块2
                                # elif id == 2 :
                                #     print("黄方能量块")
                                #     #判断是否是蓝方
                                #     if our_side == 1:
                                #         self.controller.move_cmd(600, 600)
                                #     #炸弹
                                #     else:
                                #         print("黄方炸弹")
                                #         #后退但是要检测是否到边缘
                                #         t = time.time()
                                #         #未超时和未检测到边缘
                                #         while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                #             #后退
                                #             self.controller.move_cmd(-850, -850)
                                #         #转弯
                                #         #边缘更新
                                #         n = self.edge_detect()
                                #         #不在边缘转弯五级判断
                                #         if(n == 0):
                                #             self.controller.move_cmd(750, -750)
                                #             time.sleep(0.8)
                                #         #其他情况交给你了五级判断
                                #         else:
                                #             #边缘动作
                                #             self.edge_action()
                                    
                                #当id识别不到东西的时,可能时敌方机器人，不排除视觉寄了的情况四级判断
                                elif id == None:
                                    print("不知道是什么东西,可能是敌人或大障碍物")
                                    #前进
                                    self.controller.move_cmd(650, 650)
                                    #当红外测距检测到比较高的值时把前铲稍微抬起来点可以一定程度上把敌人铲起来
                                    #读取前方红外的值
                                    FD_red = self.controller.adc_data[5]
                                    print("前方红外值为 ",FD_red)
                                    # #当红外值足够小时铲子要放下
                                    # if FD_red < 1100 :
                                    #     self.controller.up.CDS_SetAngle(5, 250, self.servo_speed)
                                    #     self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)
                                    # #当红外值相对大时可以适当抬起其爪子
                                    # else :
                                    #     self.controller.up.CDS_SetAngle(5, 270, self.servo_speed)
                                    #     self.controller.up.CDS_SetAngle(7, 680, self.servo_speed)
                                #我也不知道什么情况,乱动吧四级判断
                                else:
                                    print("我也不知道什么情况,乱动")
                                    self.randomm()
                            
                            #前方小障碍物,同未检测到一样操作,三级判断
                            elif enemy == 11:
                                #计算开启的时间t
                                now_time = time.time() - t
                                #如果时间差在0.02s内快速
                                if now_time < 0.02:
                                    #前进
                                    #print("快前进")
                                    self.controller.move_cmd(610, 610)
                                #如果时间差在0.05内可以稍微慢速
                                elif now_time >= 0.02 and now_time < 0.06:
                                    #慢前进
                                    #print("慢前进")
                                    self.controller.move_cmd(520, 520)
                                #超时了倒退一小会
                                else:
                                    #倒退
                                    self.controller.move_cmd(300, 300)
                                    #print("前进超时!!!")
                                    time.sleep(0.05)
                                #更新t
                                t = time.time()
                            
                            #后侧有敌人有俩种应对方法三级判断
                            elif enemy == 2:
                                print("enemy",enemy,"后方有敌人")
                                #开始时间检测
                                t = time.time()
                                #未超时和未检查测到边缘四级判断
                                while (((time.time()-t)<0.1) and self.edge_detect() == 0):
                                    #前进
                                    self.controller.move_cmd(600, 600)
                                #更新时间
                                t = time.time()
                                #随机转弯
                                a = random.randint(1,2)
                                #开前光电四级判断
                                while (((time.time()-t)<1.2) and self.controller.adc_data[1] > 100 and self.edge_detect() == 0):
                                    #左转
                                    if a == 1:
                                        self.controller.move_cmd(-700, 700)
                                    #右转
                                    else:
                                        self.controller.move_cmd(700, -700)
                                
                                n = self.edge_detect()
                                #未检测到边缘
                                if n == 0:
                                    self.controller.move_cmd(600, 600)
                                #其他情况
                                else:
                                    self.edge_action()

                            #右侧有敌人三级判断
                            elif enemy == 3:
                                print("enemy",enemy,"右侧有敌人")
                                #开启时间检测
                                t = time.time()
                                #未超时未检测到边缘先后退
                                while (((time.time()-t)<0.6) and self.edge_detect() == 0):
                                    self.controller.move_cmd(-700, -700)
                                #更新t
                                t = time.time()
                                #未超时未检测到边缘转弯
                                while(((time.time()-t)<0.7) and self.controller.adc_data[1] > 1000):
                                    self.controller.move_cmd(-700, 700)
                                #暂停一下
                                self.controller.move_cmd(0,0)
                                time.sleep(0.1)

                            #左侧有敌人三级判断
                            elif enemy == 4:
                                print("enemy",enemy,"左侧有敌人")
                                #开启时间检测
                                t = time.time()
                                #未超时未检测到边缘先后退
                                while (((time.time()-t)<0.6) and self.edge_detect() == 0):
                                    self.controller.move_cmd(-700, -700)
                                #更新t
                                t = time.time()
                                #未超时未检测到边缘转弯  本来0.7
                                while(((time.time()-t)<0.7) and self.controller.adc_data[1] > 1000):
                                    self.controller.move_cmd(700, -700)
                                #暂停一下
                                self.controller.move_cmd(0,0)
                                time.sleep(0.1)

                            #不知道什么情况
                            else:
                                print("光电检测到了不知道什么东西")
                                #更新t
                                t = time.time()
                                #未超时
                                while  ((time.time() - t) and self.edge_detect() == 0):
                                    #随机转弯
                                    a = random.randint(1,2)
                                    #左转
                                    if a == 1:
                                        self.controller.move_cmd(-800, 800)
                                    #右转
                                    else:
                                        self.controller.move_cmd(-800, 800)

                    #右前方检测到悬崖
                    if clif == 1:
                        print("右前方检测到悬崖")
                        #更新t
                        t = time.time()
                        #未超时未检测到边缘
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #后退
                            self.controller.move_cmd(-700, -700)
                        #更新
                        t = time.time()
                        while  (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #右转
                            self.controller.move_cmd(800, -750)
                        #状态储态
                        if state_storage == 1:
                            #重复值加一
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #更新状态
                        state_storage = 1
                        
                        
                    #左前方检测到悬崖
                    elif clif == 2:
                        print("左前方检测到悬崖")
                        #更新t
                        t = time.time()
                        #未超时未检测到边缘
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #后退
                            self.controller.move_cmd(-700, -700)
                        #更新
                        t = time.time()
                        while  (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #左转
                            self.controller.move_cmd(-750, 850)
                        #状态储态
                        if state_storage == 2:
                            #重复值加一
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #更新状态
                        state_storage = 2
                        
                    #正前方检测到悬崖
                    elif clif == 3:
                        print("正前方检测到悬崖")
                        #更新t
                        t = time.time()
                        #未超时未检测到边缘
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #后退
                            self.controller.move_cmd(-700, -700)
                        #更新
                        t = time.time()
                        while  (((time.time()-t)<1.0) and self.edge_detect() == 0):
                            #随机数的种子生成
                            random.seed(t)
                            #随机转向
                            a = random.randint(1,2)
                            if a == 1:
                                #左转
                                self.controller.move_cmd(-750, 850)
                            else:
                                #右转
                                self.controller.move_cmd(-750, 850)
                        #状态储台
                        if state_storage == 3:
                            #重复值加一
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #更新状态
                        state_storage = 3
                       
                #其他的检测
                #左前检测到边缘
                if edge == 1:
                    print("左前检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 1):
                        self.controller.move_cmd(-800, -800)
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(-750, 800)
                    #状态储态
                    if state_storage == 4:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 4

                #右前检测到边缘
                elif edge == 2:
                    print("右前检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 2):
                        self.controller.move_cmd(-800, -800)
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(800, -750)
                    #状态储态
                    if state_storage == 5:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 5

                #右后检测到边缘
                elif edge == 4:
                    print("右后检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 4):
                        self.controller.move_cmd(800, 800)
                    #状态储态
                    if state_storage == 6:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 6
                
                #左后检测到边缘
                elif edge == 3:
                    print("左后检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 3):
                        self.controller.move_cmd(900, 900)
                    #状态储态
                    if state_storage == 7:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 7
                    
                #前检测到边缘
                elif edge == 5:
                    print("前检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 5):
                        self.controller.move_cmd(-900, -900)
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(750, -800)
                    #状态储态
                    if state_storage == 8:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 8
                    
                #后测到边缘
                elif edge == 6:
                    print("后检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 6):
                        self.controller.move_cmd(900, 900)
                    #状态储态
                    if state_storage == 9:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 9
                    
                #左侧检测到边缘
                elif edge == 7:
                    print("左侧检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 7):
                        self.controller.move_cmd(-750, 800)
                    #状态储态
                    if state_storage == 10:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 10

                #右侧检测到边缘
                elif edge == 8:
                    print("右侧检测到边缘")
                    #更新t
                    t = time.time()
                    #未超时未检测到边缘
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 8):
                        self.controller.move_cmd(800, -750)
                    #状态储态
                    if state_storage == 11:
                        #重复值加一
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #更新状态
                    state_storage = 11

                #不知道什么情况乱动                             
                else:
                    self.randomm()
                
                #重复值超过20就乱动
                print("重复值 = ",repeat)
                if repeat >= 30:
                    self.randomm()
                    #repeat = 0

            #浮空
            elif stage == 5:
                print("已浮空")
                #停下
                self.randomm()
                self.controller.move_cmd(0,0)
                time.sleep(0.8)
                #收起铲子
                self.default_platform()
                
            # 搁浅   
            else:
                self.randomm()

if __name__ == '__main__':
    Main_demo = main_demo()
    Main_demo.start_match()


                                




                        
                        



                        

