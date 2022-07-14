#coding:UTF-8
#运行前需先安装pyserial，用WIN+R调出运行框，输入CMD，进入命令行，输入pip install pyserial更新一下函数库

import serial
 
ACCData=[0.0]*8
GYROData=[0.0]*8
AngleData=[0.0]*8          
FrameState = 0            #通过0x后面的值判断属于哪一种情况
Bytenum = 0               #读取到这一段的第几位
CheckSum = 0              #求和校验位         
 
a = [0.0]*3
w = [0.0]*3
Angle = [0.0]*3
def DueData(inputdata):   #新增的核心程序，对读取的数据进行划分，各自读到对应的数组里
    global  FrameState    #在局部修改全局变量，要进行global的定义
    global  Bytenum
    global  CheckSum
    global  a
    global  w
    global  Angle
    for data in inputdata:  #在输入的数据进行遍历
        #Python2软件版本这里需要插入 data = ord(data)*****************************************************************************************************
        if FrameState==0:   #当未确定状态的时候，进入以下判断
            if data==0x55 and Bytenum==0: #0x55位于第一位时候，开始读取数据，增大bytenum
                CheckSum=data
                Bytenum=1
                continue
            elif data==0x51 and Bytenum==1:#在byte不为0 且 识别到 0x51 的时候，改变frame
                CheckSum+=data
                FrameState=1
                Bytenum=2
            elif data==0x52 and Bytenum==1: #同理
                CheckSum+=data
                FrameState=2
                Bytenum=2
            elif data==0x53 and Bytenum==1:
                CheckSum+=data
                FrameState=3
                Bytenum=2
        elif FrameState==1: # acc    #已确定数据代表加速度
            
            if Bytenum<10:            # 读取8个数据
                ACCData[Bytenum-2]=data # 从0开始
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):  #假如校验位正确
                    a = get_acc(ACCData)
                CheckSum=0                  #各数据归零，进行新的循环判断
                Bytenum=0
                FrameState=0
        elif FrameState==2: # gyro
            
            if Bytenum<10:
                GYROData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):
                    w = get_gyro(GYROData)
                CheckSum=0
                Bytenum=0
                FrameState=0
        elif FrameState==3: # angle
            
            if Bytenum<10:
                AngleData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):
                    Angle = get_angle(AngleData)
                    d = a+w+Angle
                    print("a(g):%10.3f %10.3f %10.3f w(deg/s):%10.3f %10.3f %10.3f Angle(deg):%10.3f %10.3f %10.3f"%d)
                CheckSum=0
                Bytenum=0
                FrameState=0
 
 
def get_acc(datahex):  
    axl = datahex[0]                                        
    axh = datahex[1]
    ayl = datahex[2]                                        
    ayh = datahex[3]
    azl = datahex[4]                                        
    azh = datahex[5]
    
    k_acc = 16.0
 
    acc_x = (axh << 8 | axl) / 32768.0 * k_acc
    acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
    acc_z = (azh << 8 | azl) / 32768.0 * k_acc
    if acc_x >= k_acc:
        acc_x -= 2 * k_acc
    if acc_y >= k_acc:
        acc_y -= 2 * k_acc
    if acc_z >= k_acc:
        acc_z-= 2 * k_acc
    
    return acc_x,acc_y,acc_z
 
 
def get_gyro(datahex):                                      
    wxl = datahex[0]                                        
    wxh = datahex[1]
    wyl = datahex[2]                                        
    wyh = datahex[3]
    wzl = datahex[4]                                        
    wzh = datahex[5]
    k_gyro = 2000.0
 
    gyro_x = (wxh << 8 | wxl) / 32768.0 * k_gyro
    gyro_y = (wyh << 8 | wyl) / 32768.0 * k_gyro
    gyro_z = (wzh << 8 | wzl) / 32768.0 * k_gyro
    if gyro_x >= k_gyro:
        gyro_x -= 2 * k_gyro
    if gyro_y >= k_gyro:
        gyro_y -= 2 * k_gyro
    if gyro_z >=k_gyro:
        gyro_z-= 2 * k_gyro
    return gyro_x,gyro_y,gyro_z
 
 
def get_angle(datahex):                                 
    rxl = datahex[0]                                        
    rxh = datahex[1]
    ryl = datahex[2]                                        
    ryh = datahex[3]
    rzl = datahex[4]                                        
    rzh = datahex[5]
    k_angle = 180.0
 
    angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
    angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >=k_angle:
        angle_z-= 2 * k_angle
 
    return angle_x,angle_y,angle_z
 
 
if __name__=='__main__': 
    # use raw_input function for python 2.x or input function for python3.x
    port = input('please input port No. such as com7:');                #Python2软件版本用    port = raw_input('please input port No. such as com7:');*****************************************************************************************************
    #port = input('please input port No. such as com7:'));
    baud = int(input('please input baudrate(115200 for JY61 or 9600 for JY901):'))
    ser = serial.Serial(port, baud, timeout=0.5)  # ser = serial.Serial('com7',115200, timeout=0.5) 
    print(ser.is_open)
    while(1):
        datahex = ser.read(33)
        DueData(datahex)         
