##cpu、ram、温度、电压显示
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
import threading

import socket
import fcntl
import struct
import os
import psutil

#fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))
# def get_ip_address():
#     s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     s.connect(("1.1.1.1",80))
#     ipaddr=s.getsockname()[0]
#     s.close()
#     return ipaddr
    #return socket.inet_ntoa(0xff553644)
##获取网络地址
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])
##获取cpu信息
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
##获取cpu温度
def getCPUtemperature():
    res = os.popen('sudo cat /sys/class/thermal/thermal_zone0/temp').readline()
    tempfloat = float(res) / 1000
    temp = '%.1f' % tempfloat  #str(tempfloat)
    return(temp+"'C")

up=uptech.UpTech()

hostname = "Host:" + socket.gethostname() #获取当前主机名
##初始化
up.LCD_Open(2)
up.ADC_IO_Open()
up.CDS_Open()

#up.CDS_SetMode(1,up.CDS_MODE_SERVO)
#up.CDS_SetSpeed(1,512)

fore_color = up.COLOR_GREEN
back_color = up.COLOR_BLACK
##设置lcd字体背景颜色
up.LCD_SetForeColor(fore_color)
up.LCD_SetBackColor(back_color)
up.LCD_FillScreen(back_color)
up.LCD_SetFont(up.FONT_8X14)
time.sleep(0.1)
up.MPU6500_Open()
count = 0
sign = 0
sign2 = 0
while True:
##时间
    date = time.strftime("%Y-%m-%d")
    tt = time.strftime('%H:%M:%S')
##cpu温度
    cputemp = getCPUtemperature()
##cpu占用率
    cpu_usage = '%d' % psutil.cpu_percent(0)

    cpuinfo =  "CPU:" + cputemp + " " + cpu_usage + "%  "     #本机cpu的总占用率
##内存占用率
    ram_usage = '%.1f' % psutil.virtual_memory().percent 
##电压
    adc=up.ADC_Get_All_Channle()
    adc0_float = adc[9]*3.3*4.0/4096
    str_adc0= '%.2f' % adc0_float
    str_adc0 = str_adc0+"v "
    raminfo = "RAM:"  + ram_usage +"% " #+str_adc0+"v "
    try:
        ipaddr="IP:"+get_ip_address('eth0')+" "
    except:
        try:
            ipaddr="IP:"+get_ip_address('wlan0')+" " 
        except:       
            ipaddr="IP:"+"No Connected!"

    #up.LCD_FillScreen(back_color)
    up.LCD_SetForeColor(up.COLOR_BRED)
    up.LCD_PutString(0, 0,hostname)

    up.LCD_SetForeColor(fore_color)

    up.LCD_PutString(0, 16, ipaddr)
    up.LCD_PutString(0, 32, tt)
    up.LCD_PutString(0, 48, cpuinfo)
    up.LCD_PutString(0, 64, raminfo)

    up.LCD_SetForeColor(up.COLOR_LIGHTGREEN)
    up.LCD_PutString(90, 64, str_adc0)
    
##舵机控制
    if count >= 4:
        if sign != 0:
            up.CDS_SetAngle(9,0,256)
            #up.CDS_SetSpeed(1,256)
            #up.LCD_DrawFrame(150,0,159,9,up.COLOR_GREEN)
            sign = 0
        else:
            up.CDS_SetAngle(9,512,256)
            #up.CDS_SetSpeed(1,1023)
            #up.LCD_DrawFrame(150,0,159,9,up.COLOR_RED)
            sign = 1
        count = 0
    else:
        count += 1 

    if sign2 != 0:
        up.LCD_FillCircle(154,5,5,up.COLOR_GREEN)
        sign2 = 0
    else:
        up.LCD_FillCircle(154,5,5,up.COLOR_RED)
        sign2 = 1
    accel=up.MPU6500_GetAccel()
    gyro=up.MPU6500_GetGyro()
    attitude=up.MPU6500_GetAttitude()
    #print(‘my name is %s，my age is %s’ %(name,age))    
    print('Pitch:%.2f\tRoll:%.2f\tYaw:%.2f'%(attitude[0],attitude[1],attitude[2]))
    up.LCD_Refresh()
    time.sleep(0.05)


#intterupt_adc_disable()
while True:
    #up.LCD_Open()
    up.ADC_Get_All_Channle()
    #print adc_value
    time.sleep(0.1)

up.stop()





