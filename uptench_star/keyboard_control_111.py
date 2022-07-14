#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController
from matchdemo import MatchDemo
import mpu6500

self = MatchDemo()

def stop():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,0)

def move_up():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,800)

def move_up1():
    #前进
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,800)

def move_up_highspeed():
    up.CDS_SetSpeed(1,-1023)
    up.CDS_SetSpeed(2,1023)

def move_back():
    up.CDS_SetSpeed(1,1000)
    up.CDS_SetSpeed(2,-1000)

def move_back1():
    up.CDS_SetSpeed(1,600)
    up.CDS_SetSpeed(2,-600)

def move_rotation_right():
    up.CDS_SetSpeed(1,1023)
    up.CDS_SetSpeed(2,1023)

def move_rotation_right1():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,800)
    
def move_rotation_left():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,-800)

def move_rotation_left1():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,-800)

def move_right():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,800)

def move_right_back():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,0)

def move_left():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,800)
    
def move_left_back():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,0)

if __name__ == '__main__':
    up=uptech.UpTech()
    
    #up.ADC_IO_Open()
    #up.ADC_Led_SetColor(0,0x0000)
    #up.ADC_Led_SetColor(1,0x0000)
    #io_data = []
    
    #up.LCD_Open(3)
    #up.LCD_SetFont(up.FONT_7X12) #set 5th for font
    #up.LCD_SetForeColor(up.COLOR_WHITE)
    #up.LCD_SetBackColor(up.COLOR_GREEN)
    #up.LCD_FillScreen(up.COLOR_GREEN)
    #up.LCD_FillFrame(0,0,20,20,up.COLOR_BLACK)
    #up.LCD_FillRoundFrame(0,20,40,50,10,up.COLOR_BRED)
    #up.LCD_DrawMesh(0,0,100,100,up.COLOR_BLUE)
    #up.LCD_DrawFrame(0,0,100,100,up.COLOR_BLUE)
    #for i in range(0,50):
    #    for j in range(0,50):
    #        up.LCD_DrawPixel(i,j,up.COLOR_WHITE)
    #up.LCD_DrawArc(50,50,100,10,up.COLOR_BRED)
    
    up.CDS_Open()
    up.CDS_SetMode(1,1)
    up.CDS_SetMode(2,1)
    up.CDS_SetMode(5,0)
    up.CDS_SetMode(6,0)
    up.CDS_SetMode(7,0)
    up.CDS_SetMode(8,0)
    while True:
        
        #up.CDS_SetAngle(5,650,512)
        #up.CDS_SetAngle(6,650,512)
        #up.CDS_SetAngle(7,300,512)
        #up.CDS_SetAngle(8,300,512)
        #time.sleep(3)
        #up.CDS_SetAngle(5,300,512)
        #up.CDS_SetAngle(6,300,512)
        #up.CDS_SetAngle(7,650,512)
        #up.CDS_SetAngle(8,650,512)
        #time.sleep(3)
        
        key = input("get word:")
        #print("put word",key)
        if key == 's':
            stop()
            time.sleep(0.3)
            move_back1()
            #time.sleep(0.1)
        elif key == 'w':
            stop()
            time.sleep(0.3)
            move_up()
            time.sleep(0.2)

        elif key == 'r':
            stop()
            time.sleep(0.3)
            move_up_highspeed()
        elif key == 'a':
            stop()
            time.sleep(0.3)
            move_rotation_left1()
            #time.sleep(2)
            #stop()
        elif key == 'd':
            stop()
            time.sleep(0.3)
            move_rotation_right1()
            #time.sleep(0.1)
        elif key == 'q':
            stop()
            time.sleep(0.3)
            move_left()
            #time.sleep(0.1)
        elif key == 'e':
            stop()
            time.sleep(0.3)
            move_right()
            #time.sleep(0.1)
        elif key == 'z':
            #前后双方都抬起
            stop()
            up.CDS_SetAngle(5,590,1000)
            up.CDS_SetAngle(6,685,1000)
            up.CDS_SetAngle(7,370,1000)
            up.CDS_SetAngle(8,295,1000)
            #time.sleep(0.1)
        elif key == 'x':
            stop()
        
        elif key == 'n':  
            uptech.UpTech().MPU6500_Open()

        elif key == 't':        #测试区域
            #右转
            self.controller.up.CDS_SetAngle(6, 320, self.servo_speed)
            self.controller.up.CDS_SetAngle(8, 660, self.servo_speed)
            #左转
            #self.controller.move_cmd(600, 900)
            # up.CDS_SetAngle(5,260,1000)   
            # up.CDS_SetAngle(7,690,1000)
            # up.CDS_SetAngle(6,320,1000)   
            # up.CDS_SetAngle(8,660,1000)
            # while 1 :
            #     #更新传感器数值
            #     self.controller.edge_test_func()
            #     # 左前红外光电传感器
            #     io_0 = self.controller.io_data[0]
            #     # 右前红外光电传感器
            #     io_1 = self.controller.io_data[1]
            #     # 右后红外光电传感器
            #     io_2 = self.controller.io_data[2]
            #     # 左后红外光电传感器
            #     io_3 = self.controller.io_data[3]
            #     #铲子上的座光电
            #     io_l = self.controller.io_data[4]
            #     #铲子上的右光电
            #     io_r = self.controller.io_data[5]
            #     print(io_0,io_1,io_2,io_3,io_l,io_r)

            #     if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 1:
            #         self.controller.move_cmd(700, 700)
            #     if io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 1:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 1:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 1:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 0:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 0:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 1 and io_r == 0:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
            #     if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0 and io_l == 0 and io_r == 1:
            #         up.CDS_SetSpeed(1,800)
            #         up.CDS_SetSpeed(2,-800)
            #         time.sleep(0.5)
                
                    

            # # self.controller.move_cmd(500, 700)  
            # # time.sleep(0.3)     
            # # self.controller.move_cmd(500, 700)  
            # # time.sleep(0.3)     
            # # time.sleep(0.5)
            
            
        elif key == 'o':
            while(1):
                self.controller.edge_test_func()
                #底部前方红外光电
                ad1 = self.controller.adc_data[1]
                #底部右方红外光电
                ad2 = self.controller.adc_data[2]
                #底部后方红外光电
                ad3 = self.controller.adc_data[3]
                #底部左方红外光电
                ad4 = self.controller.adc_data[4]

                # 前红外测距传感器
                ad5 = self.controller.adc_data[5]
                # 右红外测距传感器
                ad6 = self.controller.adc_data[6]
                # 后红外测距传感器
                ad7 = self.controller.adc_data[7]
                # 左红外测距传感器
                ad8 = self.controller.adc_data[8]

                # 左前红外光电传感器
                io_0 = self.controller.io_data[0]
                # 右前红外光电传感器
                io_1 = self.controller.io_data[1]
                # 右后红外光电传感器
                io_2 = self.controller.io_data[2]
                # 左后红外光电传感器
                io_3 = self.controller.io_data[3]
                #铲子上的座光电
                io_l = self.controller.io_data[4]
                #铲子上的右光电
                io_r = self.controller.io_data[5]

                # print("******************")
                print("红外左前 右前 左后 右后",io_0, io_1, io_2, io_3)
                # print("------------------")
                print("ad1底部光电前",ad1)
                print("ad2底部光电右",ad2)
                print("ad3底部光电后",ad3)
                print("ad4底部光电左",ad4)
                print("------------------")
                print("ad5红外前",ad5)
                print("ad6红外右",ad6)
                print("ad7红外后",ad7)
                print("ad8红外左",ad8)
                print("******************")
                print("铲子左 铲子右",io_l,io_r)
                time.sleep(1)
        elif key == 'n':
            n = self.edge_detect()
            print("edge",n)
        elif key == '1':
            #放下前爪
            up.CDS_SetAngle(5,250,512)
            up.CDS_SetAngle(7,700,512)
            #time.sleep(1)
        elif key == '2':
            #放下后爪
            up.CDS_SetAngle(6,340,600)
            up.CDS_SetAngle(8,620,605)
            #time.sleep(1)
        elif key == '3':
            up.CDS_SetAngle(6,300,512)
            up.CDS_SetAngle(7,650,512)
            #time.sleep(1)
        elif key == '4':
            up.CDS_SetAngle(5,300,512)
            up.CDS_SetAngle(8,668,512)
            #time.sleep(1)
        elif key == '5':
            #后方的铲子过低撑起
            up.CDS_SetAngle(6,320,600)
            up.CDS_SetAngle(8,660,600)
            #time.sleep(1)
        elif key == '6':
            #四个爪子抬起
            up.CDS_SetAngle(5,305,512)
            up.CDS_SetAngle(7,710,512)
            up.CDS_SetAngle(6,370,600)
            up.CDS_SetAngle(8,600,600)

        elif key == '0':
            #self.default_platform()
            time.sleep(0.2)
            self.controller.move_cmd(700, 900)
            time.sleep(0.8)
            # 支前爪
            self.controller.move_cmd(0, 0)
            self.controller.up.CDS_SetAngle(5, 240, self.servo_speed)
            self.controller.up.CDS_SetAngle(7, 710, self.servo_speed)
            # self.pack_up_ahead()
            time.sleep(0.5)
            # 收起前爪
            self.controller.move_cmd(800,800)
            time.sleep(0.5)
            self.controller.move_cmd(0,0)
            time.sleep(0.3)
            self.controller.move_cmd(800,700)
            time.sleep(0.2)
            #self.controller.up.CDS_SetAngle(5, 600, self.servo_speed)
            #self.controller.up.CDS_SetAngle(7, 360, self.servo_speed)
            # 支后爪
            #time.sleep(0.5)
            # self.pack_up_behind()
            self.controller.up.CDS_SetAngle(6, 320, self.servo_speed)
            self.controller.up.CDS_SetAngle(8, 660, self.servo_speed)
            time.sleep(1.0)
            # 默认上台
            #self.controller.up.CDS_SetAngle(6, 700, self.servo_speed)
            #self.controller.up.CDS_SetAngle(8, 300, self.servo_speed)
            # time.sleep(0.5)
            #self.shovel_state()
            self.controller.move_cmd(500,900)
            time.sleep(0.3)
            self.controller.move_cmd(-500,900)
            time.sleep(0.5)
            self.controller.move_cmd(0,0)
            time.sleep(0.3)
            # self.default_platform()


            
