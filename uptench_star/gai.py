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
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))  # ����һ��apriltag�����

class main_demo:
    #ǰ �� �� �� ���ⶨ��
    FD = 490
    RD = 560
    BD = 750
    LD = 500
    # ��б��ʱ
    na = 0
    # �����Ӽ�ʱ
    nb = 0
    # ��ת��ʱ
    nc = 0
    # ǰ��ǳ��ʱ
    nd = 0
    # ���ǳ��ʱ
    ne = 8
    # ��б
    qx = 0
    #����
    def __init__(self):
        self.version = "1.0"
        self.servo_speed = 1023
        self.controller = UpController()
        self.controller.lcd_display("MatchDemo")
        # ����
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
        
    #�Ӿ�
    def apriltag_detect_thread(self, img):
        #����
        try:
            img=img[100:]  # �ü�ͼ��
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            tags = at_detector.detect(gray)  # ����apriltag��⣬�õ���⵽��apriltag����??
            key_biggest_s = [-1, -1, -1]  # �洢�����������������

            for tag in tags:
                x0, y0 = tuple(tag.corners[0].astype(int))  # ��ȡ��ά��Ľǵ�
                x1, y1 = tuple(tag.corners[1].astype(int))
                x2, y2 = tuple(tag.corners[2].astype(int))
                x3, y3 = tuple(tag.corners[3].astype(int))

            
                #����������ù�ʽΪ��֪�����������������������ʽ??
                s_ur=(x0*y1-x0*y2+x1*y2-x1*y0+x2*y0-x1*y1)
                s_dr = (x1*y2-x1*y3+x2*y3-x2*y1+x3*y1-x2*y2)
                s_dl = (x2*y3-x2*y0+x3*y0-x3*y2+x0*y2-x3*y3)
                s_ul = (x3*y0-x3*y1+x0*y1-x0*y3+x1*y3-x0*y0)

                if (tag.tag_id) < 3:  # ����������洢��key_longest_side??
                    if s_ul >= s_ur and s_ul >= s_dr and s_ul >= s_dl:  # ��ȡ�����??
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
        # #����ʱͨ��
        # finally:
        #     pass
        except BaseException:
            pass
       
    # Ĭ����̨������̧�����?
    def default_platform(self):
        self.controller.up.CDS_SetAngle(5, 635, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 340, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)

    # ����ǰצ
    def pack_up_ahead(self):
        self.controller.up.CDS_SetAngle(5, 230, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)

    # ���º�צ
    def pack_up_behind(self):
        self.controller.up.CDS_SetAngle(6, 340, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 620, self.servo_speed)

    # ��̨��צ�ӵ�״̬�����²���
    def shovel_state(self):
        self.controller.up.CDS_SetAngle(5, 258, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 340, self.servo_speed)  #340
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)  #700
        self.controller.up.CDS_SetAngle(8, 620, self.servo_speed)  #620
    
    #ֻ��ǰצ�ӣ�Ȼ��ȫ����
    def front_paw_half(self):
        self.controller.up.CDS_SetAngle(5, 450, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 508, self.servo_speed)
    
    #��ǰצ
    def front_paw(self):
        self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)

    #�պ�צ
    def back_paw(self):
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)

    # ǰ��̨����
    def go_up_ahead_platform(self):
        # self.controller.move_cmd(0, 0)
        # time.sleep(0.1)
        # צ��̧��
        self.default_platform()
        time.sleep(0.2)
        self.controller.move_cmd(900, 900)
        time.sleep(0.6)
        # ֧ǰצ
        self.controller.move_cmd(0, 0)
        self.controller.up.CDS_SetAngle(5, 240, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 710, self.servo_speed)
        # self.pack_up_ahead()
        time.sleep(0.5)
        # ����ǰצ
        self.controller.move_cmd(800,800)
        time.sleep(0.5)
        # self.controller.move_cmd(0,0)
        # time.sleep(0.3)
        self.controller.move_cmd(800,700)
        time.sleep(0.2)
        #self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        #self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)
        # ֧��צ
        #time.sleep(0.5)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(6, 300, self.servo_speed)#320
        self.controller.up.CDS_SetAngle(8, 680, self.servo_speed)#660
        time.sleep(0.8)
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)
        # Ĭ����̨
        #self.controller.up.CDS_SetAngle(6, 700, self.servo_speed)
        #self.controller.up.CDS_SetAngle(8, 300, self.servo_speed)
        # time.sleep(0.5)
        #self.shovel_state()
        self.controller.move_cmd(700,700)
        time.sleep(0.1)
        #self.default_platform()

    # ����Ƿ���̨��-����״̬
    def paltform_detect(self):
        #���´�������ֵ
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
            # ��̨��
            return 0
        elif sum_down == 0 and sum_up == 0:
            return 5
        else:
            # ��̨��
            return 1
        # elif angle_sensor < 1600:
        #     # ������̨����ڵ����Ҳ�����̨
        #     return 3
        # else:
        #     # ������̨�Ҳ��ڵ����������̨
        #     return 4

    #���µײ��Ĺ��
    def bash_fence(self):
        #���´�������ֵ
        self.controller.edge_test_func()
        # �ײ�ǰ��������
        ad1 = self.controller.adc_data[1]
        # �ײ��Ҳ������
        ad2 = self.controller.adc_data[2]
        # �ײ��󷽺�����
        ad3 = self.controller.adc_data[3]
        # �ײ���������
        ad4 = self.controller.adc_data[4]

        # ǰ�����ഫ����
        ad5 = self.controller.adc_data[5]
        # �Һ����ഫ����
        ad6 = self.controller.adc_data[6]
        # ������ഫ����
        ad7 = self.controller.adc_data[7]
        # ������ഫ����
        ad8 = self.controller.adc_data[8]
        
        #ǰ����̨��û���ϰ���
        if ad1 < 1000 and ad5 < self.FD:
            return 0
        #�����̨������̨�����ϰ�����ߵ���
        elif ad1 < 1000 and ad5 > self.FD:
            return 1
        #����״̬
        else:
            return 2

    #�Ϸ�����⣬����Ե
    def edge_detect(self):
        #���´�������ֵ
        self.controller.edge_test_func()
        # ��ǰ�����紫����
        io_0 = self.controller.io_data[0]
        # ��ǰ�����紫����
        io_1 = self.controller.io_data[1]
        # �Һ�����紫����
        io_2 = self.controller.io_data[2]
        # �������紫����
        io_3 = self.controller.io_data[3]

        
        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #����̨�ϣ�δ��⵽��Ե
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #��ǰ��⵽��Ե
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #��ǰ��⵽��Ե
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            #�Һ��⵽��Ե
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #����⵽��Ե
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #ǰ����⵽��Ե
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            #�󷽼�⵽��Ե
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #�󷽼�⵽��Ե
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            #�ҷ���⵽��Ե
            return 8
        else:
            return 102

    #�ڱ�Ե����Ӧ�Ķ���
    def edge_action(self):
        #���´���������
        self.controller.edge_test_func()
        # ��ǰ�����紫����
        io_0 = self.controller.io_data[0]
        # ��ǰ�����紫����
        io_1 = self.controller.io_data[1]
        # �Һ�����紫������
        io_2 = self.controller.io_data[2]
        # �������紫����
        io_3 = self.controller.io_data[3]
        
        t = time.time()
        
        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #����̨�ϣ�δ��⵽��Ե
            if self.edge_detect() == 0 :
                self.controller.move_cmd(600, 600)
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            #��ǰ��⵽��Ե
            #δ��⵽��Ե����
            while((time.time()-t)<0.5 and self.edge_detect != 0):
                self.controller.move_cmd(-800, -800)
            #����t
            t = time.time()
            #δ��⵽��Ե��ת
            while((time.time()-t)<0.5 and self.edge_detect == 1):
                self.controller.move_cmd(800, -800)
            self.controller.move_cmd(800, 800)
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #��ǰ��⵽��Ե
            #δ��⵽��Ե����
            while((time.time()-t)<0.5 and self.edge_detect == 2):
                self.controller.move_cmd(-800, -800)
            t = time.time()
            #δ��⵽��Ե��ת
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(-800, 800)
            time.sleep(0.5)
            self.controller.move_cmd(800, 800)
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            #�Һ��⵽��Ե
            #δ��⵽��Ե����
            while((time.time()-t)<0.5 and self.edge_detect == 3):
                self.controller.move_cmd(950, 950)
            t = time.time()
            #δ��⵽��Ե��ת
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(850, -750)
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #����⵽��Ե
            #δ��⵽��Ե����
            while((time.time()-t)<0.5 and self.edge_detect == 4):
                self.controller.move_cmd(950, 950)
            t = time.time()
            #δ��⵽��Ե��ת
            while((time.time()-t)<0.5 and self.edge_detect == 0):
                self.controller.move_cmd(-750, 850)
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            #ǰ����⵽��Ե
            while((time.time()-t)<0.5 and self.edge_detect == 5):
                self.controller.move_cmd(-800, -800)
            time.sleep(0.2)
            t = time.time()
            #���������������
            random.seed(t)
            a = random.randint(1,2)
            if a == 1:
                #��ת
                self.controller.move_cmd(-800, 800)
                time.sleep(0.2)
            else:
                #��ת
                self.controller.move_cmd(800, -800)
                time.sleep(0.2)
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            #�󷽼�⵽��Ե
            while((time.time()-t)<0.5 and self.edge_detect == 6):
                self.controller.move_cmd(950, 950)
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            #�󷽼�⵽��Ե
            self.controller.move_cmd(950, -950)
            time.sleep(0.2)
            self.controller.move_cmd(950, 950)
            time.sleep(0.2)
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            #�ҷ���⵽��Ե
            self.controller.move_cmd(-950, 950)
            time.sleep(0.2)
            self.controller.move_cmd(950, 950)
            time.sleep(0.2)
            return 8
        else:
            #��֪��ʲô������Ҷ�
            self.randomm()
            return 102

    # ���˼��
    def enemy_detect(self):
        #���´�������ֵ
        self.controller.edge_test_func()
        # �ײ�ǰ�������紫����
        ad1 = self.controller.adc_data[1]
        # �ײ��Ҳ�����紫����
        ad2 = self.controller.adc_data[2]
        # �ײ��󷽺����紫����
        ad3 = self.controller.adc_data[3]
        # �ײ��������紫����
        ad4 = self.controller.adc_data[4]
        # ǰ�����ഫ����
        ad5 = self.controller.adc_data[5]

        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:
            # �޵���
            return 0
        #ǰ����⵽�ж���
        elif (ad1 < 100 ) :
            if (ad5 < self.FD):
                #�ϰ���
                return 11
            else:
                return 1
        elif ad3 < 100 :
            # ���е��˻�����
            return 2
        elif (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 > 100) or (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 < 100):      
            # �Ҳ��е��˻����� or �������඼���ϰ�
            return 3
        elif ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 < 100:
            # ����е��˻�����
            return 4
        else:
            return 103    

    #����˶�
    def randomm(self):
        t = time.time()
        #���������������
        random.seed(t)
        #��צ��
        a = random.randint(1,2)
        #���з���
        b = random.randint(1,4)
        if a == 1:
            #�ź�צ
            self.pack_up_behind()
        elif a == 2:
            #��ǰצ
            self.pack_up_ahead()
        if b == 1:
            #��ת
            self.controller.move_cmd(-700, 700)
            time.sleep(0.6)
        elif b == 2:
            #��ת
            self.controller.move_cmd(700, -700)
            time.sleep(0.6)
        elif b == 3:
            #ǰ��
            self.controller.move_cmd(600, 600)
            time.sleep(0.6)
        elif b == 4:
            #����
            self.controller.move_cmd(600, 600)
            time.sleep(0.6)

    def randommm(self):
        t = time.time()
        #���������������
        random.seed(t)
        #��צ��
        a = random.randint(1,2)
        #���з���
        b = random.randint(1,4)
        if a == 1:
            #�ź�צ
            self.back_paw()
        elif a == 2:
            #��ǰצ
            self.pack_up_ahead()
        if b == 1:
            #��ת
            self.controller.move_cmd(-900, 900)
            time.sleep(0.6)
        elif b == 2:
            #��ת
            self.controller.move_cmd(900, -900)
            time.sleep(0.6)
        elif b == 3:
            #ǰ��
            self.controller.move_cmd(900, 900)
            time.sleep(0.6)
        elif b == 4:
            #����
            self.controller.move_cmd(900, 900)
            time.sleep(0.6)

    #���ǰ���Ƿ�������   1�����ϰ��˵������̨��δ��⵽���£������⵽����
    def cliff(self):
        #���´�������ֵ
        self.controller.edge_test_func()
        # ������
        io_l = self.controller.io_data[4]
        # ������
        io_r = self.controller.io_data[5]
        if io_l == 1 and io_r == 0:
            #��ǰ��⵽����
            return 1
        if io_l == 0 and io_r == 1:
            #��ǰ��⵽����
            return 2
        if io_l == 0 and io_r == 0:
            #��ǰ����⵽����
            return 3
        else:
            #��̨��һ������
            return 4

    def start_match(self):
        #��ʼ���������ĸ�����
        self.default_platform()    
        time.sleep(1)

        ##����
        ad8 = self.controller.adc_data[8]
        ad6 = self.controller.adc_data[6]
        while(ad8 <= 1500 and ad6 <= 1500):
           # print("�ҷ�������ɫ")
            ad8 = self.controller.adc_data[8]
            ad6 = self.controller.adc_data[6]
        #��߲��Ʒ�
        if(ad8 > 1500):
            print("�ҷ�Ϊ�Ʒ�")
            our_side = 0
        #�Ҳ�������
        if(ad6 > 1500):
            print("�ҷ�Ϊ����")
            our_side = 1


        #�ж��ǲ��Ǵ����ظ�һ���ж��Ǽ��п����ǿ�ס��
        repeat = 0
        #״̬����
        state_storage = 0
        #̨������״̬�Ĵ���
        taixia = 0
        taixia_1 = 0
        # ##ǰ��һ�ξ���
        # self.controller.move_cmd(900, 900)
        # time.sleep(0.4)
        # #��ת
        # self.controller.move_cmd(600, 900)
        # time.sleep(0.2)
        # ##ǰ��̨  
        #self.go_up_ahead_platform()
        # #��ת��ռ�м�������
        #self.controller.move_cmd(-500,900)
        #time.sleep(0.1)

        #��ʼ��ѭ�����ж��ǲ�����̨��
        while 1:
            #����Ƿ���̨��
            # 0Ϊ��̨�� 1Ϊ��̨�� ����5 8����綼Ϊ���δ������
            stage = self.paltform_detect()
            #��̨��,һ���ж�
            if stage == 0:
                #��צ��
                self.default_platform()
                print("stage",stage,"��̨��")
                #��̨��Ȼ��ʼ�ж���û����̨���ж��ǲ�����̨���ǲ���
                not_on_stage = 1
                #�ظ�ֵ��ʼ��
                repeat = 0
                while (not_on_stage == 1):
                    #��צ��
                    self.default_platform()
                    #���µײ��Ĺ��
                    basee = self.bash_fence()
                    print("�ײ��Ĺ��״̬?",basee)
                    print("�Ƿ�δ���׵���̨,1��,0��",not_on_stage)
                    
                    #ǰ������̨
                    if basee == 0:
                        #̨��״̬����״̬
                        taixia = 0
                        #ǰ���Ժ�
                        print("ǰ������̨?")
                        self.controller.move_cmd(900, 900)
                        time.sleep(0.3)
                        #ǰ��̨?
                        self.go_up_ahead_platform()
                        #��ʱ
                        t = time.time()
                        #��̨�ˣ����Ը�����̨�µ�ֵ�ˣ�����ѭ��
                        while((time.time() - t < 1.0) and (self.edge_detect() != 0)):
                            print("������̨��һ����")
                            #δ��̨����˶�
                            self.randommm()
                        #���ж���û����̨�ϣ�Ҫ�ĸ�ȫ������
                        if(self.edge_detect() == 0):
                            print("������̨����")
                            #��̨�˿�������ѭ���˸��丳һ
                            not_on_stage = 0
                            

                    else:
                        print("����״̬?")
                        #����
                        self.controller.move_cmd(-700, -700)
                        time.sleep(0.1)
                        #��צ?
                        self.default_platform() 
                        #��ȡʱ��,��ʱ����?
                        t = time.time()
                        #��ʱ��ǰ��δ��⵽��̨�޵���?
                        while (self.bash_fence() != 0):
                            if ((time.time()-t)<0.5):
                                #��ת
                                self.controller.move_cmd(-800, 800)
                            else :
                                self.controller.move_cmd(800, 800)
                                time.sleep(0.1)
                                #����t?
                                t = time.time()
                            #������̨�µ�״̬
                            print("��̨�µĴ���",taixia_1)
                            # if taixia == 1:
                            #     taixia_1 = taixia_1 + 1
                            # if taixia_1 >= 20:
                            #     print("�����˶�̫����ʼ���?")
                            #     #����˶�
                            #     self.randomm()
                            #     taixia_1 = 0
                            self.paltform_detect()
                            taixia = 1

            #��̨��,һ���ж�
            elif stage == 1:
                print("��̨��")
                #һ������
                p = 0
                #���²���
                self.pack_up_ahead()
                #self.pack_up_behind()
                self.back_paw()  
                #��ȡ��Ե���
                edge = self.edge_detect()
                nnn = time.time()
                #�����̨��δ��⵽��Ե��ʼ��ѭ�����ٲ���ʱ��1.5���ж�
                while(edge == 0 and p == 0):
                    print("δ��⵽��Ե")
                    #�ظ�ֵΪ0��ʼ0
                    repeat = 0
                    #���¼��
                    clif = self.cliff()
                    #���±�Ե
                    edge = self.edge_detect()
                    # #���²���
                    # self.pack_up_ahead()
                    # self.pack_up_behind()
                    ##����δ��⵽����,�����ж�
                    while(self.cliff() == 4):
                        #�����ʼ�ٶ�
                        v1 = 0
                        #����һ����ʼ��ʱ��
                        t = time.time()
                        #���±�Ե
                        edge = self.edge_detect()
                        #������̨��
                        if edge != 0:
                            p = 1
                            break

                        #��̨��    
                        else:
                            #���µײ�Ĺ���ж��Ƿ����ϰ���
                            enemy = self.enemy_detect()

                            #δ��⵽�ϰ��������ж�
                            if enemy == 0:
                                #���㿪����ʱ��
                                now_time = time.time() - t
                                # #�������0.06�����������Թ�ϵ
                                # if now_time < 0.06:
                                #     v = 900 - 5000 * now_time * now_time
                                #     if v > 790 :
                                #         v = 790
                                #     print("�������Թ�ϵv = ",int(v))
                                #     self.controller.move_cmd(int(v), int(v))
                                #���ʱ�����0.02s�ڿ���
                                if now_time < 0.02:
                                    #ǰ��
                                    #print("��ǰ��")
                                    self.controller.move_cmd(630, 630)
                                #���ʱ�����0.05�ڿ�����΢����
                                elif now_time >= 0.02 and now_time < 0.05:
                                    #��ǰ��
                                    #print("��ǰ��")
                                    self.controller.move_cmd(530, 530)
                                #��ʱ�˽���ֹͣ
                                else:
                                    #����
                                    self.controller.move_cmd(400, 400)
                                    #print("ǰ����ʱ!!!")
                                    time.sleep(0.03)
                                #����t
                                t = time.time()
                            
                            

                            #ǰ���е��ˡ����������ը�������ж�
                            elif enemy == 1:
                                #�����õı���ע��
                                # self.controller.move_cmd(750, 750)
                                # print("#ǰ���е��ˡ����������ը��id = ")
                                #��������ͷ
                                ret,img = frame.read()
                                print(ret)
                                #��id���ֵ��ֹ�䱨��
                                id = -1
                                id = self.apriltag_detect_thread(img)
                                #�жϲ�ͬid��״̬
                                print("#ǰ���е��ˡ����������ը��id = ",id)
                                #������ʱ�ļ��ж�
                                #����������Ϊ1���Ʒ�������Ϊ2��������������Ϊ0,�����Լ���������
                                #our_side = 0�Ʒ�
                                #our_side = 1����
                                #������Ƶʱ������Ϊ1,ը��Ϊ0
                                if id == 1:
                                    print("����������")
                                    #�Ѳ�����΢̧��һ�����ȷ����3KG������������̨
                                    #ǰ��,���ܻ����ȥ,ע��
                                    self.controller.move_cmd(660, 660)
                                
                                if id == 0:
                                    print("����ը��")
                                    #���˵���Ҫ����Ƿ񵽱�Ե
                                    t = time.time()
                                    #δ��ʱ��δ��⵽��Ե
                                    while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                        #����
                                        self.controller.move_cmd(-750, -750)
                                    #ת��
                                    #��Ե����
                                    n = self.edge_detect()
                                    #���ڱ�Եת���弶�ж�
                                    if(n == 0):
                                        self.controller.move_cmd(750, -750)
                                        time.sleep(0.8)
                                    #����������������弶�ж�
                                    else:
                                        #��Ե����
                                        self.edge_action()

                                # #��������1
                                # if id == 1 :
                                #     print("����������")
                                #     #�Ѳ�����΢̧��һ�����ȷ����3KG������������̨
                                #     #ǰ��,���ܻ����ȥ,ע��
                                #     #�ж��Ƿ��ǻ�ɫ
                                #     if our_side == 0:
                                #         self.controller.move_cmd(600, 600)
                                #     #ը��
                                #     else:
                                #         print("����ը��")
                                #         #���˵���Ҫ����Ƿ񵽱�Ե
                                #         t = time.time()
                                #         #δ��ʱ��δ��⵽��Ե
                                #         while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                #             #����
                                #             self.controller.move_cmd(-750, -750)
                                #         #ת��
                                #         #��Ե����
                                #         n = self.edge_detect()
                                #         #���ڱ�Եת���弶�ж�
                                #         if(n == 0):
                                #             self.controller.move_cmd(750, -750)
                                #             time.sleep(0.8)
                                #         #����������������弶�ж�
                                #         else:
                                #             #��Ե����
                                #             self.edge_action()
                                # #ը��ʱ�ļ��ж�
                                # #����������0��������ը��
                                # elif id == 0 :
                                #     print("����������")
                                #     #�Ѳ�����΢̧��һ�����ȷ����2.5KG������������̨
                                #     #ǰ��,���ܻ����ȥ,ע��
                                #     self.controller.move_cmd(800, 800)
                                # #�Ʒ�������2
                                # elif id == 2 :
                                #     print("�Ʒ�������")
                                #     #�ж��Ƿ�������
                                #     if our_side == 1:
                                #         self.controller.move_cmd(600, 600)
                                #     #ը��
                                #     else:
                                #         print("�Ʒ�ը��")
                                #         #���˵���Ҫ����Ƿ񵽱�Ե
                                #         t = time.time()
                                #         #δ��ʱ��δ��⵽��Ե
                                #         while(((time.time()-t)<0.6) and  self.edge_detect()== 0):
                                #             #����
                                #             self.controller.move_cmd(-850, -850)
                                #         #ת��
                                #         #��Ե����
                                #         n = self.edge_detect()
                                #         #���ڱ�Եת���弶�ж�
                                #         if(n == 0):
                                #             self.controller.move_cmd(750, -750)
                                #             time.sleep(0.8)
                                #         #����������������弶�ж�
                                #         else:
                                #             #��Ե����
                                #             self.edge_action()
                                    
                                #��idʶ�𲻵�������ʱ,����ʱ�з������ˣ����ų��Ӿ����˵�����ļ��ж�
                                elif id == None:
                                    print("��֪����ʲô����,�����ǵ��˻���ϰ���")
                                    #ǰ��
                                    self.controller.move_cmd(650, 650)
                                    #���������⵽�Ƚϸߵ�ֵʱ��ǰ����΢̧���������һ���̶��ϰѵ��˲�����
                                    #��ȡǰ�������ֵ
                                    FD_red = self.controller.adc_data[5]
                                    print("ǰ������ֵΪ ",FD_red)
                                    # #������ֵ�㹻Сʱ����Ҫ����
                                    # if FD_red < 1100 :
                                    #     self.controller.up.CDS_SetAngle(5, 250, self.servo_speed)
                                    #     self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)
                                    # #������ֵ��Դ�ʱ�����ʵ�̧����צ��
                                    # else :
                                    #     self.controller.up.CDS_SetAngle(5, 270, self.servo_speed)
                                    #     self.controller.up.CDS_SetAngle(7, 680, self.servo_speed)
                                #��Ҳ��֪��ʲô���,�Ҷ����ļ��ж�
                                else:
                                    print("��Ҳ��֪��ʲô���,�Ҷ�")
                                    self.randomm()
                            
                            #ǰ��С�ϰ���,ͬδ��⵽һ������,�����ж�
                            elif enemy == 11:
                                #���㿪����ʱ��t
                                now_time = time.time() - t
                                #���ʱ�����0.02s�ڿ���
                                if now_time < 0.02:
                                    #ǰ��
                                    #print("��ǰ��")
                                    self.controller.move_cmd(610, 610)
                                #���ʱ�����0.05�ڿ�����΢����
                                elif now_time >= 0.02 and now_time < 0.06:
                                    #��ǰ��
                                    #print("��ǰ��")
                                    self.controller.move_cmd(520, 520)
                                #��ʱ�˵���һС��
                                else:
                                    #����
                                    self.controller.move_cmd(300, 300)
                                    #print("ǰ����ʱ!!!")
                                    time.sleep(0.05)
                                #����t
                                t = time.time()
                            
                            #����е���������Ӧ�Է��������ж�
                            elif enemy == 2:
                                print("enemy",enemy,"���е���")
                                #��ʼʱ����
                                t = time.time()
                                #δ��ʱ��δ���⵽��Ե�ļ��ж�
                                while (((time.time()-t)<0.1) and self.edge_detect() == 0):
                                    #ǰ��
                                    self.controller.move_cmd(600, 600)
                                #����ʱ��
                                t = time.time()
                                #���ת��
                                a = random.randint(1,2)
                                #��ǰ����ļ��ж�
                                while (((time.time()-t)<1.2) and self.controller.adc_data[1] > 100 and self.edge_detect() == 0):
                                    #��ת
                                    if a == 1:
                                        self.controller.move_cmd(-700, 700)
                                    #��ת
                                    else:
                                        self.controller.move_cmd(700, -700)
                                
                                n = self.edge_detect()
                                #δ��⵽��Ե
                                if n == 0:
                                    self.controller.move_cmd(600, 600)
                                #�������
                                else:
                                    self.edge_action()

                            #�Ҳ��е��������ж�
                            elif enemy == 3:
                                print("enemy",enemy,"�Ҳ��е���")
                                #����ʱ����
                                t = time.time()
                                #δ��ʱδ��⵽��Ե�Ⱥ���
                                while (((time.time()-t)<0.6) and self.edge_detect() == 0):
                                    self.controller.move_cmd(-700, -700)
                                #����t
                                t = time.time()
                                #δ��ʱδ��⵽��Եת��
                                while(((time.time()-t)<0.7) and self.controller.adc_data[1] > 1000):
                                    self.controller.move_cmd(-700, 700)
                                #��ͣһ��
                                self.controller.move_cmd(0,0)
                                time.sleep(0.1)

                            #����е��������ж�
                            elif enemy == 4:
                                print("enemy",enemy,"����е���")
                                #����ʱ����
                                t = time.time()
                                #δ��ʱδ��⵽��Ե�Ⱥ���
                                while (((time.time()-t)<0.6) and self.edge_detect() == 0):
                                    self.controller.move_cmd(-700, -700)
                                #����t
                                t = time.time()
                                #δ��ʱδ��⵽��Եת��  ����0.7
                                while(((time.time()-t)<0.7) and self.controller.adc_data[1] > 1000):
                                    self.controller.move_cmd(700, -700)
                                #��ͣһ��
                                self.controller.move_cmd(0,0)
                                time.sleep(0.1)

                            #��֪��ʲô���
                            else:
                                print("����⵽�˲�֪��ʲô����")
                                #����t
                                t = time.time()
                                #δ��ʱ
                                while  ((time.time() - t) and self.edge_detect() == 0):
                                    #���ת��
                                    a = random.randint(1,2)
                                    #��ת
                                    if a == 1:
                                        self.controller.move_cmd(-800, 800)
                                    #��ת
                                    else:
                                        self.controller.move_cmd(-800, 800)

                    #��ǰ����⵽����
                    if clif == 1:
                        print("��ǰ����⵽����")
                        #����t
                        t = time.time()
                        #δ��ʱδ��⵽��Ե
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #����
                            self.controller.move_cmd(-700, -700)
                        #����
                        t = time.time()
                        while  (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #��ת
                            self.controller.move_cmd(800, -750)
                        #״̬��̬
                        if state_storage == 1:
                            #�ظ�ֵ��һ
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #����״̬
                        state_storage = 1
                        
                        
                    #��ǰ����⵽����
                    elif clif == 2:
                        print("��ǰ����⵽����")
                        #����t
                        t = time.time()
                        #δ��ʱδ��⵽��Ե
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #����
                            self.controller.move_cmd(-700, -700)
                        #����
                        t = time.time()
                        while  (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #��ת
                            self.controller.move_cmd(-750, 850)
                        #״̬��̬
                        if state_storage == 2:
                            #�ظ�ֵ��һ
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #����״̬
                        state_storage = 2
                        
                    #��ǰ����⵽����
                    elif clif == 3:
                        print("��ǰ����⵽����")
                        #����t
                        t = time.time()
                        #δ��ʱδ��⵽��Ե
                        while (((time.time()-t)<0.5) and self.edge_detect() == 0):
                            #����
                            self.controller.move_cmd(-700, -700)
                        #����
                        t = time.time()
                        while  (((time.time()-t)<1.0) and self.edge_detect() == 0):
                            #���������������
                            random.seed(t)
                            #���ת��
                            a = random.randint(1,2)
                            if a == 1:
                                #��ת
                                self.controller.move_cmd(-750, 850)
                            else:
                                #��ת
                                self.controller.move_cmd(-750, 850)
                        #״̬��̨
                        if state_storage == 3:
                            #�ظ�ֵ��һ
                            repeat = repeat + 1
                        else:
                            repeat = 0
                        #����״̬
                        state_storage = 3
                       
                #�����ļ��
                #��ǰ��⵽��Ե
                if edge == 1:
                    print("��ǰ��⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 1):
                        self.controller.move_cmd(-800, -800)
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(-750, 800)
                    #״̬��̬
                    if state_storage == 4:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 4

                #��ǰ��⵽��Ե
                elif edge == 2:
                    print("��ǰ��⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 2):
                        self.controller.move_cmd(-800, -800)
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(800, -750)
                    #״̬��̬
                    if state_storage == 5:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 5

                #�Һ��⵽��Ե
                elif edge == 4:
                    print("�Һ��⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 4):
                        self.controller.move_cmd(800, 800)
                    #״̬��̬
                    if state_storage == 6:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 6
                
                #����⵽��Ե
                elif edge == 3:
                    print("����⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 3):
                        self.controller.move_cmd(900, 900)
                    #״̬��̬
                    if state_storage == 7:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 7
                    
                #ǰ��⵽��Ե
                elif edge == 5:
                    print("ǰ��⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 5):
                        self.controller.move_cmd(-900, -900)
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 0):
                        self.controller.move_cmd(750, -800)
                    #״̬��̬
                    if state_storage == 8:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 8
                    
                #��⵽��Ե
                elif edge == 6:
                    print("���⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 6):
                        self.controller.move_cmd(900, 900)
                    #״̬��̬
                    if state_storage == 9:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 9
                    
                #����⵽��Ե
                elif edge == 7:
                    print("����⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 7):
                        self.controller.move_cmd(-750, 800)
                    #״̬��̬
                    if state_storage == 10:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 10

                #�Ҳ��⵽��Ե
                elif edge == 8:
                    print("�Ҳ��⵽��Ե")
                    #����t
                    t = time.time()
                    #δ��ʱδ��⵽��Ե
                    while (((time.time()-t)<0.3) and  self.edge_detect()== 8):
                        self.controller.move_cmd(800, -750)
                    #״̬��̬
                    if state_storage == 11:
                        #�ظ�ֵ��һ
                        repeat = repeat + 1
                    else:
                        repeat = 0
                    #����״̬
                    state_storage = 11

                #��֪��ʲô����Ҷ�                             
                else:
                    self.randomm()
                
                #�ظ�ֵ����20���Ҷ�
                print("�ظ�ֵ = ",repeat)
                if repeat >= 30:
                    self.randomm()
                    #repeat = 0

            #����
            elif stage == 5:
                print("�Ѹ���")
                #ͣ��
                self.randomm()
                self.controller.move_cmd(0,0)
                time.sleep(0.8)
                #�������
                self.default_platform()
                
            # ��ǳ   
            else:
                self.randomm()

if __name__ == '__main__':
    Main_demo = main_demo()
    Main_demo.start_match()


                                




                        
                        



                        

