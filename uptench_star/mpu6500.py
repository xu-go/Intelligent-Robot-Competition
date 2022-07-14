import uptech
import time
import cv2
import threading
import sys, select, termios, tty
#from matchdemo import MatchDemo

##初始化
def Read_mpu6500():
    mopp = uptech.UpTech()
    # MPU6500_Open() 
     ##获取加速度
    # mopp.MPU6500_Open()

    mopp.MPU6500_GetAccel()
    ##获取角速度
    mopp.MPU6500_GetGyro()
    ##获取姿态数据，pitch roll yaw
    mopp.MPU6500_GetAttitude()
    nnop = [1,2,3]
    for i in range(3):
        print("加速度%d",i)
        print(mopp.MPU6500_GetAttitude())



if __name__ == '__main__':
    mopp = uptech.UpTech()
    # MPU6500_Open() 
     ##获取加速度
    mopp.MPU6500_Open()

    mopp.MPU6500_GetAccel()
    ##获取角速度
    mopp.MPU6500_GetGyro()
    ##获取姿态数据，pitch roll yaw
    mopp.MPU6500_GetAttitude()
    nnop = [1,2,3]
    for i in range(3):
        print("加速度%d",i)
        print(mopp.MPU6500_GetAttitude())
    while 1:
        mopp.MPU6500_GetAccel()
        ##获取角速度
        mopp.MPU6500_GetGyro()
        ##获取姿态数据，pitch roll yaw
        mopp.MPU6500_GetAttitude()
        nnop = [1,2,3]
        for i in range(3):
            print("加速度%d",i)
            print(mopp.MPU6500_GetAttitude())