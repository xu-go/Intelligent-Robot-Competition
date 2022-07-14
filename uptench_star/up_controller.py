#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
import threading
import closed_loop_controller
class UpController:
    

    # cmd
    NO_CONTROLLER = 0
    MOVE_UP = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    MOVE_YAW_LEFT = 4
    MOVE_YAW_RIGHT = 5
    MOVE_STOP = 6
    PICK_UP_BALL = 7

    SPEED = 512
    YAW_SPEED = 210

    # GET_AD_DATA
    # chassis_mode 1 for servo ,2 for controller
    CHASSIS_MODE_SERVO = 1
    CHASSIS_MODE_CONTROLLER = 2

    def __init__(self):
        self.up=uptech.UpTech()
        self.up.LCD_Open(2)
        open_flag = self.up.ADC_IO_Open()
        print("ad_io_open = {}".format(open_flag))
        self.up.CDS_Open()
        self.cmd = 0
        self.closed_loop=closed_loop_controller.ClosedLoopController()
        self.adc_data = []
        self.io_data = []
        controller_thread = threading.Thread(name = "up_controller_thread",target=self.send_cmd)
        controller_thread.setDaemon(True)
        controller_thread.start()

        self.open_edge_detect()

    def open_edge_detect(self):
        edge_thread = threading.Thread(name = "edge_detect_thread",target=self.edge_detect_thread)
        #edge_thread = threading.Thread(name = "edge_detect_thread",target=self.edge_detect_func)
        edge_thread.setDaemon(True)
        edge_thread.start()
        # time.sleep(1)
        time.sleep(0.2)

    def edge_detect_thread(self):
        while True:
            self.adc_data = self.up.ADC_Get_All_Channle()
            io_all_input = self.up.ADC_IO_GetAllInputLevel()
            #print("io_vaule = {}".format(io_all_input))
            io_array = '{:08b}'.format(io_all_input)
            self.io_data.clear()
            for index, value in enumerate(io_array):
                io_value = (int)(value)
                self.io_data.insert(0, io_value)
                # print(self.io_data)
    #底层去掉一个循环改上面的代码
    def edge_test_func(self):
        self.adc_data = self.up.ADC_Get_All_Channle()
        io_all_input = self.up.ADC_IO_GetAllInputLevel()
        #print("io_vaule = {}".format(io_all_input))
        io_array = '{:08b}'.format(io_all_input)
        self.io_data.clear()
        for index, value in enumerate(io_array):
            io_value = (int)(value)
            self.io_data.insert(0, io_value)
            # print(self.io_data)

    def set_chassis_mode(self, mode):
        self.chassis_mode = mode

    def send_cmd(self):
        while True:
            if self.cmd == self.MOVE_UP:
                self.move_up()
            if self.cmd == self.MOVE_LEFT:
                self.move_left()
            if self.cmd == self.MOVE_RIGHT:
                self.move_right()
            if self.cmd == self.MOVE_YAW_LEFT:
                self.move_yaw_left()
            if self.cmd == self.MOVE_YAW_RIGHT:
                self.move_yaw_right()
            if self.cmd == self.MOVE_STOP:
                self.move_stop()
            if self.cmd == self.PICK_UP_BALL:
                self.pick_up_ball()
            
    def get_ad_data(self):
        return self.adc_data

    # 速度指令，自由控制-开环控制器
    def move_cmd(self, left_speed, right_speed):
        self.up.CDS_SetSpeed(1, -left_speed)
        self.up.CDS_SetSpeed(2, right_speed)
    #  速度指令，闭环控制器，使用闭环控制时替换开环控制代码
    #def move_cmd(self, left_speed, right_speed):
    #    self.closed_loop.set_motor_speed(1,  left_speed)
    #    self.closed_loop.set_motor_speed(1,  -right_speed)



    def move_up(self): 
        if self.chassis_mode == self.CHASSIS_MODE_SERVO:
            self.up.CDS_SetSpeed(1, self.SPEED)
            self.up.CDS_SetSpeed(2, -self.SPEED)
            self.up.CDS_SetSpeed(3, self.SPEED)
            self.up.CDS_SetSpeed(4, -self.SPEED) 

        if self.chassis_mode == self.CHASSIS_MODE_CONTROLLER:
            self.up.CDS_SetSpeed(1, self.SPEED)
            self.up.CDS_SetSpeed(2, -self.SPEED)

        self.cmd = self.NO_CONTROLLER

    def move_left(self):
        if self.chassis_mode == self.CHASSIS_MODE_SERVO:
            self.up.CDS_SetSpeed(1, -self.SPEED)
            self.up.CDS_SetSpeed(2, -self.SPEED)
            self.up.CDS_SetSpeed(3, self.SPEED)
            self.up.CDS_SetSpeed(4, self.SPEED) 
        
        if self.chassis_mode == self.CHASSIS_MODE_CONTROLLER:
            self.up.CDS_SetSpeed(1,-200)
            self.up.CDS_SetSpeed(2, 200)
        self.cmd = self.NO_CONTROLLER

    def move_right(self):
        if self.chassis_mode == self.CHASSIS_MODE_SERVO:
            self.up.CDS_SetSpeed(1, self.SPEED)
            self.up.CDS_SetSpeed(2, self.SPEED)
            self.up.CDS_SetSpeed(3, -self.SPEED)
            self.up.CDS_SetSpeed(4, -self.SPEED) 
        
        if self.chassis_mode == self.CHASSIS_MODE_CONTROLLER:
            self.up.CDS_SetSpeed(1, 200)
            self.up.CDS_SetSpeed(2, -200)
        self.cmd = self.NO_CONTROLLER

    def move_yaw_left(self):
        if self.chassis_mode == self.CHASSIS_MODE_SERVO:
            self.up.CDS_SetSpeed(1, -self.SPEED)
            self.up.CDS_SetSpeed(2, self.SPEED)
            self.up.CDS_SetSpeed(3, -self.SPEED)
            self.up.CDS_SetSpeed(4, self.SPEED) 
        
        if self.chassis_mode == self.CHASSIS_MODE_CONTROLLER:
            self.up.CDS_SetSpeed(1, -self.YAW_SPEED)
            self.up.CDS_SetSpeed(2, -self.YAW_SPEED)
        self.cmd = self.NO_CONTROLLER

    def move_yaw_right(self):
        if self.chassis_mode == self.CHASSIS_MODE_SERVO:
            self.up.CDS_SetSpeed(1, -self.SPEED)
            self.up.CDS_SetSpeed(2, self.SPEED)
            self.up.CDS_SetSpeed(3, -self.SPEED)
            self.up.CDS_SetSpeed(4, self.SPEED) 
        
        if self.chassis_mode == self.CHASSIS_MODE_CONTROLLER:
            self.up.CDS_SetSpeed(1, self.YAW_SPEED)
            self.up.CDS_SetSpeed(2, self.YAW_SPEED)
        self.cmd = self.NO_CONTROLLER

    def move_stop(self):
        self.up.CDS_SetSpeed(1, 0)
        self.up.CDS_SetSpeed(2, 0)
        self.up.CDS_SetSpeed(3, 0)
        self.up.CDS_SetSpeed(4, 0) 
        self.cmd = self.NO_CONTROLLER

    def pick_up_ball(self):
        self.move_stop()
        time.sleep(2)
        self.up.CDS_SetAngle(5,512,self.SPEED)
        time.sleep(2)
        self.up.CDS_SetAngle(6,580,self.SPEED)
        self.up.CDS_SetAngle(7,450,self.SPEED)
        time.sleep(2)
        self.up.CDS_SetAngle(5,921,self.SPEED)
        time.sleep(2)
        self.up.CDS_SetAngle(6,495,self.SPEED)
        self.up.CDS_SetAngle(7,530,self.SPEED)
        self.cmd = self.NO_CONTROLLER

    def go_up_platform(self):
        self.move_up()
        time.sleep(1)
        self.up.CDS_SetAngle(5,900,self.SPEED)
        self.up.CDS_SetAngle(6,100,self.SPEED)
        time.sleep(3)
        self.up.CDS_SetAngle(5,512,self.SPEED)
        self.up.CDS_SetAngle(6,512,self.SPEED)
        time.sleep(2)
        self.up.CDS_SetAngle(7,100,self.SPEED)
        self.up.CDS_SetAngle(8,900,self.SPEED)
        time.sleep(2)
        time.sleep(1)
        self.up.CDS_SetAngle(7,512,self.SPEED)
        self.up.CDS_SetAngle(8,512,self.SPEED)
        #self.up.CDS_SetAngle(9,500,self.SPEED * 3)

    def servo_reset(self):
        self.up.CDS_SetAngle(5,512,self.SPEED)
        self.up.CDS_SetAngle(6,512,self.SPEED)
        self.up.CDS_SetAngle(7,512,self.SPEED)
        self.up.CDS_SetAngle(8,512,self.SPEED)


    def set_cds_mode(self,ids,mode):
        for id in ids:
            self.up.CDS_SetMode(id,mode)

    def set_controller_cmd(self,cmd):
        self.cmd = cmd

    def lcd_display(self,content):
        self.up.LCD_PutString(30, 0, content)
        self.up.LCD_Refresh()
        self.up.LCD_SetFont(self.up.FONT_8X14)


if __name__ == '__main__':
    # up_controller = UpController()
    # ids = [1,2]
    # servoids = [5,6,7,8]
    # up_controller.set_chassis_mode(up_controller.CHASSIS_MODE_CONTROLLER)
    # up_controller.set_cds_mode(ids,1)
    # up_controller.set_cds_mode(servoids,0)
    # # up_controller.go_up_platform()
    # up_controller.servo_reset()
    # up_controller.open_edge_detect()
    b = int("0x0b",16)
    c = '{:08b}'.format(b)
    print(c)
    


    




