# -*- coding: utf-8 -*-
import sys
import dlib
import cv2

class myCorrelationTracker(object):
    def __init__(self, windowName='default window', cameraNum=0):
        # 自定义几个状态标志
        self.STATUS_RUN_WITHOUT_TRACKER = 0     # 不跟踪目标，但是实时显示
        self.STATUS_RUN_WITH_TRACKER = 1    # 跟踪目标，实时显示
        self.STATUS_PAUSE = 2   # 暂停，卡在当前帧
        self.STATUS_BREAK = 3   # 退出
        self.status = self.STATUS_RUN_WITHOUT_TRACKER   # 指示状态的变量

        # 这几个跟前面程序1定义的变量一样
        self.track_window = None  # 实时跟踪鼠标的跟踪区域
        self.drag_start = None   # 要检测的物体所在区域
        self.start_flag = True   # 标记，是否开始拖动鼠标
        self.selection = None

        # 创建好显示窗口
        cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(windowName, self.onMouseClicked)
        self.windowName = windowName

        # 打开摄像头
        self.cap = cv2.VideoCapture(0)

        # correlation_tracker()类，跟踪器，跟程序1中一样
        self.tracker = dlib.correlation_tracker()

        # 当前帧
        self.frame = None

    # 按键处理函数
    def keyEventHandler(self):
        keyValue = cv2.waitKey(5)  # 每隔5ms读取一次按键的键值
        if keyValue == 27:  # ESC
            self.status = self.STATUS_BREAK
        if keyValue == 32:  # 空格
            if self.status != self.STATUS_PAUSE:    # 按下空格，暂停播放，可以选定跟踪的区域
                #print self.status
                self.status = self.STATUS_PAUSE
                #print self.status
            else:   # 再按次空格，重新播放，但是不进行目标识别
                if self.track_window:
                    self.status = self.STATUS_RUN_WITH_TRACKER
                    self.start_flag = True
                else:
                    self.status = self.STATUS_RUN_WITHOUT_TRACKER
        if keyValue == 13:  # 回车
            #print '**'
            if self.status == self.STATUS_PAUSE:    # 按下空格之后
                if self.track_window:   # 如果选定了区域，再按回车，表示确定选定区域为跟踪目标
                    self.status = self.STATUS_RUN_WITH_TRACKER
                    self.start_flag = True

    # 任务处理函数        
    def processHandler(self):
        # 不跟踪目标，但是实时显示
        if self.status == self.STATUS_RUN_WITHOUT_TRACKER:
            ret, self.frame = self.cap.read()
            cv2.imshow(self.windowName, self.frame)
        # 暂停，暂停时使用鼠标拖动红框，选择目标区域，与程序1类似
        elif self.status == self.STATUS_PAUSE:
            img_first = self.frame.copy()  # 不改变原来的帧，拷贝一个新的变量出来
            if self.track_window:   # 跟踪目标的窗口画出来了，就实时标出来
                cv2.rectangle(img_first, (self.track_window[0], self.track_window[1]), (self.track_window[2], self.track_window[3]), (0,0,255), 1)
            elif self.selection:   # 跟踪目标的窗口随鼠标拖动实时显示
                cv2.rectangle(img_first, (self.selection[0], self.selection[1]), (self.selection[2], self.selection[3]), (0,0,255), 1)
            cv2.imshow(self.windowName, img_first)
        # 退出
        elif self.status == self.STATUS_BREAK:
            self.cap.release()   # 释放摄像头
            cv2.destroyAllWindows()   # 释放窗口
            sys.exit()   # 退出程序
        # 跟踪目标，实时显示
        elif self.status == self.STATUS_RUN_WITH_TRACKER:
            ret, self.frame = self.cap.read()  # 从摄像头读取一帧
            if self.start_flag:   # 如果是第一帧，需要先初始化
                self.tracker.start_track(self.frame, dlib.rectangle(self.track_window[0], self.track_window[1], self.track_window[2], self.track_window[3]))  # 开始跟踪目标
                self.start_flag = False   # 不再是第一帧
            else:
                self.tracker.update(self.frame)   # 更新

                # 得到目标的位置，并显示
                box_predict = self.tracker.get_position()   
                cv2.rectangle(self.frame,(int(box_predict.left()),int(box_predict.top())),(int(box_predict.right()),int(box_predict.bottom())),(0,255,255),1)
                cv2.imshow(self.windowName, self.frame)

    # 鼠标点击事件回调函数
    def onMouseClicked(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下
            self.drag_start = (x, y)
            self.track_window = None
        if self.drag_start:   # 是否开始拖动鼠标，记录鼠标位置
            xMin = min(x, self.drag_start[0])
            yMin = min(y, self.drag_start[1])
            xMax = max(x, self.drag_start[0])
            yMax = max(y, self.drag_start[1])
            self.selection = (xMin, yMin, xMax, yMax)
        if event == cv2.EVENT_LBUTTONUP:   # 鼠标左键松开
            self.drag_start = None
            self.track_window = self.selection
            self.selection = None

    def run(self):
        while(1):
            self.keyEventHandler()
            self.processHandler()


if __name__ == '__main__':
    testTracker = myCorrelationTracker(windowName='image', cameraNum=1)
    testTracker.run()
