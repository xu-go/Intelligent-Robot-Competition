import threading
from typing import Tuple
from up_controller import UpController
import time
import cv2
import apriltag
import sys
import numpy as np
import math
import mpu6500
import uptech

frame = cv2.VideoCapture(-1)
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))  # ����һ��apriltag�����



class MatchDemo:

    

    FD = 700
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
        

    def apriltag_detect_thread(self, img):
        img=img[100:]  # �ü�ͼ��
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(gray)  # ����apriltag��⣬�õ���⵽��apriltag���б�
        key_biggest_s = [-1, -1, -1]  # �洢�����������������

        for tag in tags:
            x0, y0 = tuple(tag.corners[0].astype(int))  # ��ȡ��ά��Ľǵ�
            x1, y1 = tuple(tag.corners[1].astype(int))
            x2, y2 = tuple(tag.corners[2].astype(int))
            x3, y3 = tuple(tag.corners[3].astype(int))

        
            #����������ù�ʽΪ��֪�����������������������ʽ��
            s_ur=(x0*y1-x0*y2+x1*y2-x1*y0+x2*y0-x1*y1)
            s_dr = (x1*y2-x1*y3+x2*y3-x2*y1+x3*y1-x2*y2)
            s_dl = (x2*y3-x2*y0+x3*y0-x3*y2+x0*y2-x3*y3)
            s_ul = (x3*y0-x3*y1+x0*y1-x0*y3+x1*y3-x0*y0)

            if (tag.tag_id) < 3:  # ����������洢��key_longest_side��
                if s_ul >= s_ur and s_ul >= s_dr and s_ul >= s_dl:  # ��ȡ������
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


        # print("detect start")
        # cap = cv2.VideoCapture(2)

        # w = 640
        # h = 480
        # weight = 320
        # cap.set(3,w)
        # cap.set(4,h)

        # cup_w = (int)((w - weight) / 2)
        # cup_h = (int)((h - weight) / 2) + 50

        # while True:
        #     ret, frame = cap.read()
        #     #frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
        #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     tags = self.at_detector.detect(gray)
        #     for tag in tags:
        #         self.tag_id = tag.tag_id
        #         print("tag_id = {}".format(tag.tag_id))
        #         cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
        #         cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
        #         cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
        #         cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
        #     cv2.imshow("img", frame)
        #     if cv2.waitKey(100) & 0xff == ord('q'):
        #        break
        # cap.release()
        # cv2.destroyAllWindows()

    # Ĭ����̨����
    def default_platform(self):
        self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 685, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 295, self.servo_speed)

    def default_platform2(self):
        self.controller.up.CDS_SetAngle(5, 455, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 380, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 50, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 600, self.servo_speed)


    # ����ǰצ
    def pack_up_ahead(self):
        self.controller.up.CDS_SetAngle(5, 258, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)
        # self.controller.up.CDS_SetAngle(5, 360, self.servo_speed)     #����
        # self.controller.up.CDS_SetAngle(7, 630, self.servo_speed)

    # ���º�צ
    def pack_up_behind(self):
        self.controller.up.CDS_SetAngle(6, 360, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 600, self.servo_speed)
        # self.controller.up.CDS_SetAngle(6, 300, self.servo_speed)
        # self.controller.up.CDS_SetAngle(8, 668, self.servo_speed)


    # ��̨��צ�ӵ�״̬
    def shovel_state(self):
        self.controller.up.CDS_SetAngle(5, 258, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 380, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 700, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 600, self.servo_speed)
    
    #ֻ��ǰצ�ӣ�Ȼ��ȫ����
    def front_paw_half(self):
        self.controller.up.CDS_SetAngle(5, 450, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 508, self.servo_speed)
    
    def front_paw(self):
        self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)

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
        time.sleep(0.8)
        # ֧ǰצ
        self.controller.move_cmd(0, 0)
        self.controller.up.CDS_SetAngle(5, 240, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 710, self.servo_speed)
        # self.pack_up_ahead()
        time.sleep(0.5)
        # ����ǰצ
        self.controller.move_cmd(800,800)
        time.sleep(0.5)
        self.controller.move_cmd(0,0)
        time.sleep(0.3)
        self.controller.move_cmd(900,700)
        time.sleep(0.2)
        self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)
        # ֧��צ
        #time.sleep(0.5)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(6, 320, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 660, self.servo_speed)
        time.sleep(1.0)
        # Ĭ����̨
        # self.controller.up.CDS_SetAngle(6, 700, self.servo_speed)
        # self.controller.up.CDS_SetAngle(8, 300, self.servo_speed)
        # time.sleep(0.5)
        self.shovel_state()
        self.controller.move_cmd(0,0)
        time.sleep(0.3)
        # self.default_platform()

    # ����̨
    def go_up_behind_platform(self):
        self.controller.move_cmd(0, 0)
        time.sleep(0.1)
        # צ��̧��
        self.default_platform()
        time.sleep(0.4)
        self.controller.move_cmd(-800, -800)
        time.sleep(1)
        # ֧ǰצ
        self.controller.move_cmd(0,0)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(5, 790, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 190, self.servo_speed)
        time.sleep(0.5)
        # ����ǰצ
        self.controller.move_cmd(-1023,-1023)
        time.sleep(0.5)
        self.controller.move_cmd(0,0)
        time.sleep(0.3)
        self.controller.move_cmd(-1023,-1023)
        time.sleep(0.3)
        self.controller.up.CDS_SetAngle(5, 305, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 710, self.servo_speed)
        # ֧��צ
        #time.sleep(0.5)
        # self.pack_up_ahead()
        self.controller.up.CDS_SetAngle(6, 700, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 170, self.servo_speed)
        time.sleep(1)
        # Ĭ����̨
        # self.controller.up.CDS_SetAngle(5,700,self.servo_speed)
        # self.controller.up.CDS_SetAngle(7,310,self.servo_speed)
        self.default_platform()
        #time.sleep(0.5)
        # self.controller.move_cmd(700, 900)
        # time.sleep(0.7)

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

    def fence_detect(self):
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

        # # ��ǰ�����紫����
        # io_0 = self.controller.io_data[0]
        # # ��ǰ�����紫����
        # io_1 = self.controller.io_data[1]
        # # �Һ�����紫����
        # io_2 = self.controller.io_data[2]
        # # �������紫����
        # io_3 = self.controller.io_data[3]

        # ----------------------����̨��һ������⵽--------------------
        if  ad2 > 1000 and ad4 > 1000 and ad3 < 1000 and ad1 < 1000 and ad5 > self.FD-130 and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£��󷽶���̨ad3 < 1000 and
            return 1
        if  ad2 > 1000 and ad4 > 1000 and ad3 < 1000 and ad1 > 1000 and ad5 > self.FD-130 and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£��󷽶���̨ad3 < 1000 and
            return 1
        if ad4 > 1000 and ad1 > 1000 and ad3 > 1000 and ad2 < 1000 and ad5 < self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:        #��
            # ��̨�£��Ҳ�1����̨
            return 2
        if ad4 < 1000 and ad1 > 1000 and ad3 > 1000 and ad2 < 1000 and ad5 < self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:        #��
            # ��̨�£��Ҳ�2����̨
            return 2
        if ad1 < 1000 and ad2 > 1000 and ad4 > 1000 and ad5 < self.FD+300 and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£�ǰ������̨
            return 3
        if ad1 > 1000 and ad2 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£�ǰ��2����̨
            return 3
        if ad1 > 1000 and ad2 > 1000 and ad3 > 1000 and ad4 < 1000 and ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£�������̨ad2 > 1000and
            return 4
        if ad1 > 1000 and ad2 < 1000 and ad3 > 1000 and ad4 < 1000 and ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:        #��
            # ��̨�£�������̨2
            return 4
        # ------------------------��Χ�����������ڲ���⵽-------------
        if ad1 < 13 and ad2 > 1000 and ad3 > 1000 and ad4 < 1000 and ad5 > self.FD and ad6 < self.RD-100  and ad7 < self.BD and ad8 > self.LD:       #��
            # ��̨�£�ǰ���⵽Χ��
            return 5

        if ad1 < 1000 and ad2 < 1000 and ad3 > 1000 and ad4 > 1000 and ad5 > self.FD and ad6 > self.RD-100 and ad7 < self.BD and ad8 < self.LD:       #��
            # ��̨�£�ǰ�Ҽ�⵽Χ��
            return 6
        if ad1 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:       #��
            # ��̨�£����Ҽ�⵽Χ��
            return 7
        if ad1 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:       #��
            # ��̨�£����Ҽ�⵽Χ��
            return 7
        if ad1 > 1000 and ad2 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:       #��
            # ��̨�£������⵽Χ��
            return 8
        if ad1 > 1000 and ad2 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:       #��
            # ��̨�£������⵽Χ��
            return 8
        # --------------------------̨���е��ˣ�������Բ���⵽-----------
        if ad1 < 1000 and ad5 > self.FD+200 and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:         
            # ��̨�£�ǰ�������̨�ϵ���
            return 9
        if ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # ��̨�£������Ҳ���̨�ϵ���
            return 10
        # -------------------------�������ϰ�����������⵽---------------
        if ad5 > self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # ��̨�£�ǰ���������Ҳ��⵽Χ��
            return 11
        if ad5 > self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:
            # ��̨�£�ǰ�����Ҳ�ͺ󷽼�⵽Χ��
            return 12
        if ad5 > self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:
            # ��̨�£�ǰ�������ͺ󷽼�⵽Χ��
            return 13
        if ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 > self.LD:
            # ��̨�£��Ҳࡢ���ͺ󷽼�⵽Χ��
            return 14
        # -----------------------б����̨�������������⵽----------------
        if ad1 < 1000 and ad2 < 1000 and ad5 < self.FD and ad6 < self.RD:
            # ��̨�£�ǰ�����Ҳ����̨����������û��⵽
            return 15
        if ad1 < 1000 and ad4 < 1000 and ad5 < self.FD and ad8 < self.LD:
            # ��̨�£���̨�£�ǰ����������̨����������û��⵽
            return 16
        if ad2 < 1000 and ad3 < 1000 and ad6 < self.FD and ad7 < self.RD:
            # ��̨�£��󷽺��Ҳ����̨����������û��⵽
            return 17
        if ad3 < 1000 and ad4 < 1000 and ad7 < self.FD and ad8 < self.LD:
            # ��̨�£��󷽺�������̨����������û��⵽
            return 18
        else:
            # print("else")
            return 101


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
        # ������
        #io_l = self.controller.io_data[4]
        # ������
        #io_r = self.controller.io_data[5]
        #print(io_l,io_r)

        # if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_r == 1 and io_l == 1:
        #     # û�м�⵽��Ե
        #     return 0
        # elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 1:
        #     # ��ǰ��⵽��Ե
        #     return 1
        # elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 0:
        #     # ��ǰ��⵽��Ե
        #     return 1
        # elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 1:
        #     # ��ǰ��⵽��Ե
        #     return 1
        # elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 0:
        #     # ��ǰ��⵽��Ե
        #     return 2
        # elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 0:
        #     # ��ǰ��⵽��Ե
        #     return 2
        # elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 0:
        #     # ��ǰ��⵽��Ե
        #     return 2
        # elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 0:
        #     # ��ǰ��⵽��Ե
        #     return 2
        if io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            # �Һ��⵽��Ե
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # ����⵽��Ե
            return 4
        # elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_r == 0 and io_l == 0:
        #     # ǰ��������⵽��Ե
        #     return 5
        # elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_r == 0 and io_l == 0:
        #     # ǰ��������⵽��Ե
        #     return 5
        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # δ��⵽��Ե
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # ��ǰ��⵽��Ե
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            # ��ǰ��⵽��Ե
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            # ��������⵽��Ե
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # ���������⵽��Ե
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            # �Ҳ�������⵽��Ե
            return 8
        else:
            return 102

    # ���˼��
    def enemy_detect(self):
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

        #print("ad1 = {} , ad2 = {} , ad3 = {}, ad4 = {} , ad5 = {}".format(ad1,ad2,ad3,ad4,ad5))

        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:
            # �޵���
            return 0
        elif (ad1 < 100 ) :
            return 1
            # if ad5 > 1000:
            #     # ǰ��������
            #     return 11
            # else:
            #     # ǰ���е���
            #     if self.tag_id != 2 or self.tag_id == -1:
            #         # ǰ���ǵ���
            #         return 1
            #     else:
            #         return 5
        elif ad3 < 100 :
            # ���е��˻�����
            return 3
        elif (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 > 100) or (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 < 100):      
            # �Ҳ��е��˻����� or �������඼���ϰ�
            return 2
        elif ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 < 100:
            # //����е��˻�����
            return 4
        else:
            return 103

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
        self.default_platform()    #�����ĸ�����
        time.sleep(1)
        #����

        #ad4 = self.controller.adc_data[8]
        #while(ad4 <= 1000):
        #    # print("1")
        #    ad4 = self.controller.adc_data[8]


        #ǰ��һ�ξ���

        #self.controller.move_cmd(800, 800)
        #time.sleep(0.5)  
        #self.go_up_ahead_platform()    #ǰ��̨      #4.1s


        # self.controller.move_cmd(900, 500)  
        # time.sleep(0.2)  
        while 1:
            stage = self.paltform_detect()    #����Ƿ���̨��
            #ret,img = frame.read()
            # self.default_platform()
            # time.sleep(0.01)                                            #0.01s
            # ��̨��
            if stage == 0:
                print("stage",stage,"��̨��")
                self.default_platform()         #������
                not_on_stage = 0                #��̨��Ȼ��ʼ�ж���û����̨���ж��ǲ�����̨���ǲ���
                while(not_on_stage == 0):
                    fence = self.fence_detect()     #��ȡ�ײ���缰�����ഫ��������
                    print("fence",fence)
                    not_on_stage = 1
                    
                    # ��̨�º󷽶���̨
                    if fence == 1:
                        print("��̨�º󷽶���̨")
                        t = time.time()
                        ad1 = self.controller.adc_data[1]
                        ad2 = self.controller.adc_data[2]
                        ad3 = self.controller.adc_data[3]
                        ad4 = self.controller.adc_data[4]
                        ad7 = self.controller.adc_data[7]
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad2 = self.controller.adc_data[2]
                            ad3 = self.controller.adc_data[3]
                            ad4 = self.controller.adc_data[4]
                            #ad7 = self.controller.adc_data[7]
                            if ad1 < 1000 and ad4 > 1000 and ad2 > 1000  or (time.time() - t) >= 4:     #�ѵ�����������̨
                                # time.sleep(0.2)     ad5 < 700 and                and ad4 > 1000        #0.2s
                                self.controller.move_cmd(600, 600)
                                time.sleep(0.6) 
                                # print("��������")                           #0.3s
                                break
                            else:       #Ϊ���������̨��������������
                                # print(ad5,ad7)
                                # print("2")
                                self.controller.move_cmd(-600, 600)
                                time.sleep(0.02)
                        #   self.controller.move_cmd(-600,-600)
                        #   time.sleep(0.5)                                     #0.3s
                        #   print("fence",fence,"��̨�º󷽶���̨")
                        #  self.go_up_ahead_platform()    #����̨             #4.1s
                    
                    # �Ҳ����̨
                    if fence == 2:
                        print("fence",fence,"��̨���Ҳ����̨")
                        self.controller.move_cmd(-800, 800)
                        time.sleep(0.2)                                     #0.2s
                        t = time.time()
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or (time.time() - t) >= 4:     #�ѵ�����������̨
                                # time.sleep(0.2)                             #0.2s
                                self.controller.move_cmd(600, 600)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:       #Ϊ���������̨��������������
                                self.controller.move_cmd(-600, 600)
                                time.sleep(0.002)                           #0.002s
                    
                    # ǰ������̨
                    if fence == 3:
                            print("fence",fence,"��̨��ǰ������̨")
                            self.controller.move_cmd(800,800)
                            time.sleep(0.2)                                     #0.2s
                            self.go_up_ahead_platform()                         #4.1s
                            edgee = self.edge_detect()
                            eng = 0                                             #�ж���̨�Ĵ���
                            # while edgee != 0 or eng < 3:                                           #���û��̨�ͼ���
                            #     self.go_up_ahead_platform()
                            #     edgee = self.edge_detect()
                            #     eng = eng + 1
                            edgee = 0 
                            not_on_stage = 1       
                    
                    # ������̨
                    if fence == 4:
                        print("fence",fence,"��̨��������̨")
                        self.controller.move_cmd(-800, 800)
                        time.sleep(0.2)                                     #0.2s
                        t = time.time()
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or (time.time() - t) >= 4:     #�롯������̨��������������
                                # time.sleep(0.2)                             #0.2s
                                self.controller.move_cmd(600, 600)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:
                                self.controller.move_cmd(600, -600)
                                time.sleep(0.002)                           #0.002
                    
                    # ǰ���⵽Χ��
                    if fence == 5:      #������̨�����������˵��������·���ͬ
                        print("fence",fence,"��̨�£�ǰ���⵽Χ��")
                        self.controller.move_cmd(-600, -600)
                        time.sleep(0.4)                                     #0.4s
                    # ǰ�Ҽ�⵽Χ��
                    if fence == 6:
                        print("fence",fence,"��̨�£�ǰ�Ҽ�⵽Χ��")
                        self.controller.move_cmd(-600, -600)
                        time.sleep(0.4)                                     #0.4s
                    # ���Ҽ�⵽Χ��
                    if fence == 7:      #��Ȼ�ǹ�������������ǰ������
                        print("fence",fence,"��̨�£����Ҽ�⵽Χ��")
                        self.controller.move_cmd(600, 600)
                        time.sleep(1)                                     #0.4s
                    # �����⵽Χ��
                    if fence == 8:
                        print("fence",fence,"��̨�£������⵽Χ��")
                        self.controller.move_cmd(600, 600)
                        time.sleep(1)                                     #0.4s
                    
                    # ǰ�������̨�ϵ���
                    if fence == 9:      #����ת����ǰ�����ܿ����ˣ�����λ����̨
                        print("fence",fence,"��̨�£�ǰ�������̨�ϵ���")
                        self.controller.move_cmd(-800, -800)
                        time.sleep(0.2)
                        self.controller.move_cmd(800, -800)
                        time.sleep(0.4)                                     #0.3s
                        self.controller.move_cmd(800, 800)
                        time.sleep(0.4)                                      #0.4s
                    # �����Ҳ���̨�ϵ���
                    if fence == 10:     #ֱ��ǰ��������λ����̨
                        print("fence",fence,"��̨�£������Ҳ���̨�ϵ���")
                        self.controller.move_cmd(600, 600)
                        time.sleep(0.4)                                     #0.4s
                    
                    # ǰ���������Ҳ��⵽Χ��
                    if fence == 11:         #�˴����������֪�����˴���ʲô״̬
                        print("fence",fence,"��̨�£�ǰ���������Ҳ��⵽Χ��")
                        self.controller.move_cmd(600, 500)
                        time.sleep(0.5)                                     #0.5s
                        self.controller.move_cmd(-600, 600)
                        time.sleep(0.8)                                     #0.3s
                    # ǰ�Һ��⵽Χ��
                    if fence == 12:
                        print("fence",fence,"��̨�£�ǰ�Һ��⵽Χ��")
                        self.controller.move_cmd(500, 800)
                        time.sleep(0.8)                                     #0.4s
                    # ǰ����⵽Χ��
                    if fence == 13:
                        print("fence",fence,"��̨�£�ǰ����⵽Χ��")
                        self.controller.move_cmd(800, 500)
                        time.sleep(0.8)                                     #0.4s
                    # ������⵽Χ��
                    if fence == 14:
                        print("fence",fence,"��̨�£�������⵽Χ��")
                        self.controller.move_cmd(-600, 600)
                        time.sleep(0.2)                                     #0.2s
                        self.controller.move_cmd(600, 600)
                        time.sleep(0.3)                                     #0.3s
                    
                    # ǰ�Ҽ�⵽��̨
                    if fence == 15:     #�롮�Ҳ����̨�����������ͬ
                        print("fence",fence,"��̨�£�ǰ�Ҽ�⵽��̨")
                        self.controller.move_cmd(-600, -600)
                        time.sleep(0.5)                                     #0.5s
                        self.controller.move_cmd(800, 600)
                        time.sleep(0.5)                                     #0.5s
                        t = time.time()
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or ((time.time() - t)) >= 2:
                                #time.sleep(0.2)
                                self.controller.move_cmd(800, 800)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:
                                if (time.time() - t == 2) :
                                    break
                                self.controller.move_cmd(1000, 0)
                                time.sleep(0.5)                             #0.5s
                    #  ǰ���⵽��̨
                    if fence == 16:     #�롮������̨�����������ͬ
                        print("fence",fence,"��̨�£�ǰ���⵽��̨")
                        self.controller.move_cmd(-600, -600)
                        time.sleep(0.5)                                     #0.5s
                        self.controller.move_cmd(600, 800)
                        time.sleep(0.5)                                     #0.5s
                        t = time.time()
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or ((time.time() - t)) >= 2:
                                # time.sleep(0.2)
                                self.controller.move_cmd(800, 800)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:
                                if (time.time() - t == 2) :
                                    break
                                self.controller.move_cmd(0, 1000)
                                time.sleep(0.5)    
                                                            #0.5s
                    # ��̨�£��󷽺��Ҳ����̨����������û��⵽
                    if fence == 17:         #��֪����ʲô״̬������������롮�Ҳ����̨�����ƣ���ת�ٶȲ�ͬ��
                        print("fence",fence,"��̨�£��󷽺��Ҳ����̨����������û��⵽")
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.2)                                     #0.2s
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                                # time.sleep(0.2)                             #0.2s
                                self.controller.move_cmd(800, 800)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:
                                self.controller.move_cmd(600, -700)
                                time.sleep(0.002)                           #0.002s
                    # ��̨��,�󷽺�������̨����������û��⵽
                    if fence == 18:         #ͬ��
                        print("fence",fence,"��̨�£��󷽺�������̨����������û��⵽")
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.2)                                     #0.2s
                        while 1:
                            ad1 = self.controller.adc_data[1]
                            ad4 = self.controller.adc_data[4]
                            ad6 = self.controller.adc_data[6]
                            if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                                # time.sleep(0.2)                             #0.2s
                                self.controller.move_cmd(600, 600)
                                time.sleep(0.3)                             #0.3s
                                break
                            else:
                                self.controller.move_cmd(-620, 550)
                                time.sleep(0.002)                           #0.002s
                    # elif fence == 19:
                    #     print("���ǰ��")
                    #     self.go_up_behind_platform()
                    # elif fence == 20:
                    #     print("ǰ�ߺ��")
                    #     self.go_up_ahead_platform()
                    if fence == 101:
                        # print("ɶҲ���ǣ�")
                        self.controller.move_cmd(600,600)
                        time.sleep(0.01)
                

            #����̨��
            elif stage == 1:
                
                # print("stage",stage,"��̨��")
                # self.na = 0
                # self.nb = 0
                edge = self.edge_detect()
                nnn = time.time()
                # print("edge = ",edge)
                if edge == 0:
                    
                    # print("edge",edge,"δ��⵽��Ե")
                    self.pack_up_ahead()
                    
                    self.pack_up_behind()
                    #self.controller.move_cmd(0, 0)
                    # time.sleep(0.1)
                    enemy = self.enemy_detect()
                    # print("enemy",enemy)
                    # �޵���
                    clif = self.cliff()
                    vvv = time.time()-nnn
                    print("�򿪹�粢����",vvv)
                    
                    if clif == 4:       #δ��⵽����
                        # ret,img = frame.read()
                        while(1):
                            abcd = time.time()
                            while(self.cliff() == 4 and self.edge_detect() == 0):     #
                                t = time.time()                          
                                enemy = self.enemy_detect()
                                if enemy == 0:      #�޵��������ӣ�����ǰ��  !!!ע��400���ٶ��Ʋ���2.5KG��������Ҫ�Ķ�ץ��ʱ���������Ӧ�ӳٵ�����
                                    #print("enemy",enemy,"�޵���������")
                                    # self.pack_up_ahead()
                                    cha = time.time()
                                    if((cha-t)>0.03):
                                        self.controller.move_cmd(600, 600)
                                    elif((cha-t)>0.05):
                                        self.controller.move_cmd(-400, -400)
                                    else:
                                        self.controller.move_cmd(800, 800)
                                    #print("ǰ��ʱ���",cha-t)
                                    # self.shovel_state()
                                    #time.sleep(0.1)
                                    
                                # ǰ��qizi
                                elif enemy == 1:      #ǰ�����ˣ�����ǰ��
                                    ret,img = frame.read()
                                    # print("enemy",enemy,"ǰ���и�����")
                                    id = -1
                                    id = self.apriltag_detect_thread(img)
                                    # self.controller.move_cmd(0,0)
                                    # time.sleep(1)                                             #1s
                                    print("id =", id)
                                    if (id == 1):                          #�����2�����ƿ�
                                        #print("enemy",enemy,"ǰ����������")
                                        self.controller.up.CDS_SetAngle(5, 268, self.servo_speed)
                                        self.controller.up.CDS_SetAngle(7, 690, self.servo_speed)
                                        # edge = self.edge_detect()
                                        # id = self.apriltag_detect_thread(img)
                                        # while(edge == 0):                             #��������ײ����Ե��ͣ��
                                        self.controller.move_cmd(950, 950)#400�ǿ��Ե�
                                        
                                        #time.sleep(0.15)

                                        # edge = self.edge_detect()
                                        # self.pack_up_ahead
                                        # time.sleep(0.5)                                     #0.5s
                                        # self.default_platform()
                                        # time.sleep(1)                                       #1s
                                    elif (id == 0  or id == 2) :
                                        #print("enemy",enemy,"ǰ����ը��")
                                        t = time.time()
                                        n = self.edge_detect()
                                        #����Ե��
                                        while (((time.time()-t)<0.6) and n == 0):
                                            self.controller.move_cmd(-800, -800)                                         #0.5s
                                        self.controller.move_cmd(750,-750)
                                        time.sleep(1)                                         #1s
                                        self.controller.move_cmd(800,800)
                                        time.sleep(0.2)                                       #0.5s
                                    elif(id == None) :
                                        #print("enemy",enemy,"ǰ������ͨ�ϰ����з�С��")
                                        # edge = self.edge_detect()
                                        self.controller.move_cmd(750, 750)
                                        time.sleep(0.1)
                        

                                # �Ҳ��е���
                                elif enemy == 2:      #�Ҳ��е��ˣ����˺�(�˴����˺�Ŀ����ɲ������Ϊִ��ʱ��ֻ��0.1s)��ԭ����ת
                                    print("enemy",enemy,"�Ҳ��е���")
                                    t = time.time()
                                    n = self.edge_detect()
                                    #����Ե��
                                    while (((time.time()-t)<0.6) and n == 0):
                                        self.controller.move_cmd(-800, -800)                                             #0.3s
                                    #print("ad1","                                                     ",ad1)
                                    if n == 0:    
                                        ad1 = self.controller.adc_data[1]
                                        t = time.time()
                                        while(ad1 > 100):
                                            ad1 = self.controller.adc_data[1]
                                            #print("ad1","                                                     ",ad1)
                                            self.controller.move_cmd(-700, 700)
                                            # self.default_platform()
                                            if time.time() - t >= 1.10:    #timeout
                                                break
                                        self.controller.move_cmd(0,0)
                                        time.sleep(0.1)
                                    else:
                                        self.controller.move_cmd(900, 900)
                                        time.sleep(0.2) 
                                    #time.sleep(0.5)
                                # ���е��ˣ�����������ģʽ���Ժ���������֣�1��ֱ�ӵ�ͷ��ȥײ2��ֱ�ӵ���ײ�����ǲ���ʶ��
                                elif enemy == 3:      #ֱ��ԭ�ص�ͷ
                                    print("enemy",enemy,"���е���")
                                    t = time.time()
                                    n = self.edge_detect()
                                    #����Ե��
                                    while (((time.time()-t)<0.5) and n == 0):
                                        self.controller.move_cmd(700, 700)                                            #0.3s
                                    ad1 = self.controller.adc_data[1]
                                    t = time.time()
                                    while(ad1 > 100):
                                        ad1 = self.controller.adc_data[1]
                                        #print("ad1","                                                     ",ad1)
                                        self.controller.move_cmd(700, -700)
                                        # self.default_platform()
                                        if time.time() - t >= 1.5:    #timeout
                                            break
                                    self.controller.move_cmd(0,0)
                                    time.sleep(0.1)                                             #0.1s
                                    #time.sleep(1.0)
                                # ����е���
                                elif enemy == 4:      #�Ⱥ��ˣ�����ת
                                    print("enemy",enemy,"����е���")
                                    t = time.time()
                                    n = self.edge_detect()
                                    #����Ե��
                                    while (((time.time()-t)<0.6) and n == 0):
                                        self.controller.move_cmd(-800, -800)                                           #0.3s
                                    #print("ad1","                                                     ",ad1)
                                    if n == 0 :    
                                        ad1 = self.controller.adc_data[1]
                                        # ad5 = self.controller.adc_data[5]
                                        t = time.time()
                                        while(ad1 > 1000 ):#and ad5 < 900
                                            ad1 = self.controller.adc_data[1]
                                            # ad5 = self.controller.adc_data[5]
                                            #print("ad1","                                                     ",ad1)
                                            self.controller.move_cmd(700, -700)
                                            # self.default_platform()
                                            if time.time() - t >= 1.1:    #timeout
                                                break
                                        self.controller.move_cmd(0,0)
                                        time.sleep(0.1)  
                                    else:
                                        self.controller.move_cmd(-900, -900)
                                        time.sleep(0.2)                                             #0.1s
                                    #time.sleep(0.5)
                                #  ��������
                                # if enemy == 5:      #���ˣ���ת��ǰ��
                                #     print("enemy",enemy,"��������")
                                #     self.controller.move_cmd(-600, -600)
                                #     time.sleep(0.2)
                                #     self.controller.move_cmd(-600, 600)
                                #     time.sleep(0.5)
                                #     self.controller.move_cmd(600, 600)
                                #     time.sleep(0.4)
                                # # ǰ����⵽����
                                # if enemy == 11:     #����ǰ��
                                #     print("enemy",enemy,"ǰ������")
                                #     id = self.apriltag_detect_thread(img)
                                #     print("id =", id)
                                #     if (id != 1):
                                #         self.controller.move_cmd(600, 600)
                                #         time.sleep(0.3)
                                #         self.pack_up_ahead()
                                #         time.sleep(0.5)
                                #     else :
                                #         self.controller.move_cmd(-600,-600)
                                #         time.sleep(0.5)
                                #         self.controller.move_cmd(800,-800)
                                #         time.sleep(1)
                                #         self.controller.move_cmd(600,600)
                                #         time.sleep(1)
                                #     self.pack_up_ahead()
                                #     # time.sleep(0.001)
                            
                            print("������",time.time()-abcd)
                            self.controller.move_cmd(-900, -900)
                            time.sleep(0.4)
                            clif = self.cliff()
                            break
                    elif clif == 1: #��ǰ��⵽����
                        t = time.time()
                        fafa = t - nnn
                        print("��ǰʱ���һ",fafa)
                        n = self.edge_detect()
                        print("�򿪹���ʱ��",time.time-t)
                        while (((time.time()-t)<0.5) and n == 0):
                            self.controller.move_cmd(-900, -900)
                        self.controller.move_cmd(600, -850)
                        time.sleep(0.6)
                        
                    elif clif == 2: #��ǰ��⵽����
                        t = time.time()
                        n = self.edge_detect()
                        fafa = t - nnn
                        print("��ǰʱ���һ",fafa)
                        while (((time.time()-t)<0.5) and n == 0):
                            self.controller.move_cmd(-900, -900)
                        self.controller.move_cmd(-850, 600)
                        time.sleep(0.6)
                    elif clif == 3: #��ǰ����⵽���� 
                        t = time.time()
                        fafa = t - nnn
                        print("��ǰʱ���һ",fafa)
                        n = self.edge_detect()
                        while (((time.time()-t)<0.5) and n == 0):
                            self.controller.move_cmd(-900, -900)
                        # self.front_paw_half()
                        # time.sleep(0.4)
                        self.pack_up_ahead()
                        self.pack_up_behind()
                        self.controller.move_cmd(-850, 600)
                        time.sleep(0.8)   
                # ��ǰ��⵽��Ե
                elif edge == 1:       #���ˣ���ת
                    t = time.time()
                    fafa = t - nnn
                    print("��ǰʱ����",fafa)
                    n = self.edge_detect()
                    while (((time.time()-t)<0.5) and n == 0):
                        self.controller.move_cmd(-900, -900)
                    self.controller.move_cmd(-750, 800)
                    time.sleep(0.6)
                    # self.controller.move_cmd(800,-800)
                    # time.sleep(1)                                #0.3s
                # ��ǰ��⵽��Ե
                elif edge == 2:       #���ˣ���ת
                    t = time.time()
                    fafa = t - nnn
                    print("��ǰʱ����",fafa)  
                    n = self.edge_detect()
                    while (((time.time()-t)<0.5) and n == 0):
                        self.controller.move_cmd(-900, -900)
                    self.controller.move_cmd(800, -750)
                    time.sleep(0.6)
                    
                    #self.default_platform()
                    #self.pack_up_ahead()
                    # self.controller.move_cmd(-800, 800)
                    # time.sleep(1)                                           #1s  
                    #self.pack_up_behind()
                    # self.controller.move_cmd(600,600)
                    # time.sleep(0.5)                                          #0.3s
                # �Һ��⵽��Ե
                elif edge == 3:       #ǰ������ת
                    #print("edge",edge,"�Һ��⵽��Ե")
                    self.controller.move_cmd(800, 800)
                    time.sleep(0.3)                                           #1s
                    # self.controller.move_cmd(0,0)
                    # time.sleep(0.3)                                         #0.3s
                    # self.controller.move_cmd(800, -800)
                    # # self.pack_up_ahead()
                    # # self.pack_up_behind()
                    # time.sleep(1)                                         #0.5s
                    self.controller.move_cmd(600,600)
                    time.sleep(0.5)                                           #0.3s
                # ����⵽��Ե
                elif edge == 4:       #ǰ������ת
                    #print("edge",edge,"����⵽��Ե")
                    # self.default_platform()
                    self.controller.move_cmd(800, 800)
                    time.sleep(0.3)                                           #1s
                    # self.controller.move_cmd(0,0)
                    # time.sleep(0.3)                                         #0.3s
                    # self.controller.move_cmd(-800, 800)
                    # # self.pack_up_ahead()
                    # # self.pack_up_behind()
                    # time.sleep(1)                                         #0.5s
                    # # self.controller.move_cmd(0,0)
                    # # time.sleep(0.3)                                         #0.3s
                # ǰ��������⵽��Ե
                elif edge == 5:       #���ˣ���ת
                    self.controller.move_cmd(-850,-850)          #ɲ����������Ҫ��Ҫ
                    #��ǰצ
                    t = time.time()
                    fafa = t - nnn
                    print("��ǰʱ����",fafa)
                    #print("edge",edge,"ǰ����⵽��Ե")
                    #self.default_platform()
                    time.sleep(0.6)
                    self.self.front_paw_half()
                    time.sleep(0.4)  
                    self.pack_up_ahead()
                    self.pack_up_behind()                                        #1s
                    # self.controller.move_cmd(0,0)
                    # time.sleep(0.3)                                         #0.3s
                    self.controller.move_cmd(800, -800)
                    # # self.pack_up_ahead()
                    # # self.pack_up_behind()
                    # time.sleep(0.8)                                         #0.5s
                    
                    # self.controller.move_cmd(600,600)
                    # time.sleep(0.2)                                         #0.3s
                # ��������⵽��Ե
                elif edge == 6:       #ǰ��
                    #print("edge",edge,"�󷽼�⵽��Ե")

                    self.default_platform()
                    self.controller.move_cmd(900, 900)
                    time.sleep(0.6)                                         #1s
                # �Ҳ�������⵽��Ե 
                elif edge == 7:       #��ת��ǰ��
                    #print("edge",edge,"�Ҳ��⵽��Ե")
                    self.controller.move_cmd(-450,-450)          #ɲ����������Ҫ��Ҫ
                    #��ǰצ
                    #self.front_paw()
                    self.default_platform()
                    self.controller.move_cmd(-600,700)
                    time.sleep(0.5)                                         #0.5s
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    self.controller.move_cmd(800,800)
                    time.sleep(0.5)                                         #0.3s
                    # self.controller.move_cmd(0,0)
                    # time.sleep(0.3)                                         #0.3s
                # ���������⵽��Ե
                elif edge == 8:
                    self.controller.move_cmd(-450, -450)          #ɲ����������Ҫ��Ҫ
                    #��ǰצ
                    #self.front_paw()
                    self.controller.move_cmd(700,-600)
                    self.default_platform()
                    time.sleep(0.5)                                         #0.5s
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.5)                                         #0.3s
                    # self.controller.move_cmd(0,0)
                    # time.sleep(0.3)                                         #0.3s
                # elif edge == 9:
                #     print("���ǰ��")
                #     self.go_up_behind_platform()
                # elif edge == 10:
                #     print("ǰ�ߺ��")
                #     self.go_up_ahead_platform()
                # # ��ǳǰ�ڵ���
                # elif edge == 9:
                #     self.nd += 1
                #     if self.nd > 20:
                #         self.nd = 0
                #         self.controller.move_cmd(0, 0)
                #         time.sleep(0.01)
                #         self.controller.move_cmd(-800, -800)
                #         time.sleep(0.2)
                #         self.go_up_ahead_platform()
                #         self.controller.move_cmd(-800, -800)
                #         time.sleep(0.8)
                #         self.default_platform()
                #         self.controller.move_cmd(-800, -800)
                #         time.sleep(0.5)
                #         self.controller.move_cmd(800, -800)
                #         time.sleep(0.3)
                #         self.controller.move_cmd(0, 0)
                #         time.sleep(0.1)
                #     else:
                #         time.sleep(0.02)
                # elif edge == 10:
                #     self.ne += 1
                #     if self.ne > 20:
                #         self.ne = 0
                #         self.controller.move_cmd(0, 0)
                #         time.sleep(0.01)
                #         self.controller.move_cmd(800, 800)
                #         time.sleep(0.2)
                #         self.go_up_ahead_platform()
                #         self.controller.move_cmd(800, 800)
                #         time.sleep(0.8)
                #         self.default_platform()
                #         self.controller.move_cmd(800, 800)
                #         time.sleep(0.4)
                #         self.controller.move_cmd(0, 0)
                #         time.sleep(0.1)
                #     else:
                #         time.sleep(0.02)
                elif edge == 102:
                    self.controller.move_cmd(700, 700)
                    time.sleep(0.7)
                    self.controller.move_cmd(-700,700)
                    time.sleep(0.5)
                    
            # ��ǳ�������̨�Ҳ��ڵ���
            elif stage == 3:
                print("�ҵ����")
                t = time.time()
                ad7 = self.controller.adc_data[7]
                while 1:
                    self.controller.move_cmd(-800,800)
                    if ad7 > self.BD or (time.time() - t >= 3):
                        break
                # self.na += 1
                # if self.na == 350:
                #     self.controller.move_cmd(-800, 800)
                #     self.controller.up.CDS_SetAngle(5, 1000, self.servo_speed)
                #     self.controller.up.CDS_SetAngle(7, 24, self.servo_speed)
                #     time.sleep(0.8)
                #     self.default_platform()
                #     time.sleep(0.6)
                #     self.na = 0
                # else:
                #     time.sleep(0.001)
            # ��ǳ�Ҳ�����̨����ڵ���
            elif stage == 4:
                print("����Ҹ�")
                t = time.time()
                ad7 = self.controller.adc_data[7]
                while 1:
                    self.controller.move_cmd(800,-800)
                    if ad7 > self.BD or (time.time() - t >= 3):
                        break
                # self.na += 1
                # if self.na == 350:
                #     self.controller.move_cmd(800, -800)
                #     self.controller.up.CDS_SetAngle(6, 24, self.servo_speed)
                #     self.controller.up.CDS_SetAngle(8, 1000, self.servo_speed)
                #     time.sleep(0.8)
                #     self.default_platform()
                #     time.sleep(0.6)
                #     self.na = 0
                # else:
                #     time.sleep(0.001)
                
            elif stage == 5:
                print("�Ѹ���")
                self.pack_up_ahead()
                self.controller.up.CDS_SetAngle(8, 790, self.servo_speed)
                self.controller.up.CDS_SetAngle(6, 190, self.servo_speed)
                self.controller.move_cmd(800,800)
                time.sleep(0.5)
                self. shovel_state()
                self.controller.move_cmd(0,0)
                time.sleep(0.5)
                self.controller.move_cmd(800,-800)
                time.sleep(0.5)
                self.controller.move_cmd(-800,-800)
                time.sleep(0.5)
                self.default_platform()

if __name__ == '__main__':
    # uptech.UpTech().MPU6500_Open()
    match_demo = MatchDemo()
    # match_demo.stop()
    match_demo.start_match()
