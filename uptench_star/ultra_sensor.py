##超声波传感器
import time
from serial_helper import SerialHelper
import threading


class UltraSensor():
    
    def __init__(self):
        # 创建串口对象
        self.ser = SerialHelper()
        self.ser.on_connected_changed(self.myserial_on_connected_changed)

        # 发送的数据队列
        self.msg_list = []
        # 是否连接成功
        self._isConn = True

        # 通信线程创建启动
        sendThread = threading.Thread(name = "send_thread",target=self.send_msg)
        sendThread.setDaemon(True)
        sendThread.start()

    # 串口连接状态回调函数
    def myserial_on_connected_changed(self, is_connected):
        if is_connected:
            print("Connected")
            self._isConn = True
            self.ser.connect()
            self.ser.on_data_received(self.on_data_received)
        else:
            print("DisConnected")

    # 串口通信发送
    def write(self, data):
        self.ser.write(data, True)

    # 串口通信线程发送函数
    def send_msg(self):
        while True:
            if len(self.msg_list) > 0 and self._isConn:
                self.ser.write(self.msg_list[0])
                time.sleep(0.1)
                self.msg_list.remove(self.msg_list[0])

    # 串口数据包构建方法
    def generateCmd(self, id, l, data):
        buffer = [0] * (len(data) + 7)
        buffer[0] = 0x55
        buffer[1] = 0xAA
        buffer[2] = id & 0xFF
        buffer[3] = 0x00 & 0xFF
        buffer[4] = 0x05 & 0xFF
        buffer[5] = 0x00 & 0xFF

        for i in range(len(data)):
            buffer[6 + i] = data[i]

        check = 0
        for i in range(len(buffer)):
            check += buffer[i]

        buffer[len(data) + 6] = check & 0xFF

        # for i in range(len(buffer)):
        #     print(hex(int(buffer[i])))
        return buffer


    # 获取超声波传感器数据线程启动
    def get_sensor_data(self):
        print("start sensor thread")
        self.get_sensor_data_thread = threading.Thread(target=self.get_sensor_data_callback, name="get_sensor")
        self.get_sensor_data_thread.setDaemon(False)
        self.get_sensor_data_thread.start()

    # 获取超声波传感器数据，循环执行
    def get_sensor_data_callback(self):
        while True:
            if self._isConn:
                buffer = [0] * 0
                data = self.generateCmd(0x60, 0, buffer)
                self.write(data)
                time.sleep(1)
                
    # 超声传感器数据读取回调函数
    def on_data_received(self, data):
        if len(data) > 8:
            if data[3] == 0x02 and data[4] == 0x05:
                value = ((data[8] & 0xFF) | ((data[7] & 0xFF) << 8))
                print("sensor data = {} cm".format(value))


if __name__ == '__main__':
    connect = UltraSensor()
    time.sleep(1)
    connect.get_sensor_data()


        
        


