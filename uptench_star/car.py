##避障小车
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController


if __name__ == '__main__':
##初始化
    up=uptech.UpTech()
    up.ADC_IO_Open()
    up.LCD_Open(2)    
    up.ADC_Led_SetColor(0,0x07E0)          #led绿色
    up.ADC_Led_SetColor(1,0x07E0)
    up.LCD_PutString(10, 0, 'uptech_car')
    up.LCD_Refresh()                       #刷新屏幕
    up_controller=UpController()
    servo_ids = [1,2,3,4]
    up_controller.set_cds_mode(servo_ids,1)#电机模式
    io_data = []
    while True:
##获取io
        io_all_input = up.ADC_IO_GetAllInputLevel()
        io_array = '{:08b}'.format(io_all_input)
        io_data.clear()
        up_controller.set_chassis_mode(1)        #舵机控制模式，1 for servo，2 for controller；
        for index, value in enumerate(io_array):       
            io = (int)(value)     
            io_data.insert(0,io)
        if io_data[0]==1 and io_data[1]==1:      #前进
            up.ADC_Led_SetColor(0,0x0000)
            up.ADC_Led_SetColor(1,0x0000)
            up_controller.move_up()
            time.sleep(0.2)
        elif io_data[0]==0:                    #左转
            up.ADC_Led_SetColor(0,0xF800)
            up.ADC_Led_SetColor(1,0X0000)
            up_controller.move_back()
            time.sleep(1)
            up_controller.move_left()
            time.sleep(1)
        else:                                 #右转
            up.ADC_Led_SetColor(0,0x0000)
            up.ADC_Led_SetColor(1,0XF800)
            up_controller.move_back()
            time.sleep(1)
            up_controller.move_right()
            time.sleep(1)
    
            

    





