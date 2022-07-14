#红外光电控制电机
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController

###红外控制舵机运动
if __name__ == '__main__':
    up=uptech.UpTech()
    up.ADC_IO_Open()
    up.LCD_Open(2)
    up.ADC_Led_SetColor(0,0x07E0)
    up.ADC_Led_SetColor(1,0x07E0)
    up.LCD_PutString(10, 0, 'cds_test')
    up.LCD_Refresh()
    up.CDS_Open()
    up.CDS_SetMode(1,1)
    io_data = []
    while True:
        io_all_input = up.ADC_IO_GetAllInputLevel()
        io_array = '{:08b}'.format(io_all_input)
        io_data.clear()
        for index, value in enumerate(io_array):       
            io = (int)(value)     
            io_data.append(io)  
            io_data =io_data[::-1]
        if io_data[0]==1:
            up.ADC_Led_SetColor(0,0X8430)
            up.ADC_Led_SetColor(1,0X8430)
            up.CDS_SetSpeed(1,500)
            time.sleep(0.2)
        else:
        #up.CDS_SetAngle(1,256,800)
            up.ADC_Led_SetColor(0,0xF800)
            up.ADC_Led_SetColor(1,0xF800)
            up.CDS_SetSpeed(1,-500)
        #up.CDS_SetAngle(1,500,256)
            time.sleep(0.2)


