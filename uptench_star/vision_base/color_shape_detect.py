import cv2
import numpy as np
import utils

font = cv2.FONT_HERSHEY_SIMPLEX

class ColorDetect:
    def __init__(self):
        self.target_H = 0
        self.target_S = 0
        self.target_V = 0
        self.gray_frame = None
        self.hsv_frame = None
    
    def mouse_click(self, event, x, y, flags, para):
        if event == cv2.EVENT_LBUTTONDOWN:
            print ('PIX: ', x, y)
            print ('GRAY: ', self.gray_frame[y, x])
            print ('HSV: ', self.hsv_frame[y, x])
    
    def update_frame(self, img, h_min, h_max, s_min, s_max, v_min, v_max):
        src_frame = img
        self.gray_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2GRAY)
        self.hsv_frame = cv2.cvtColor(src_frame, cv2.COLOR_BGR2HSV)
        low_color = np.array([h_min, s_min, v_min])
        high_color = np.array([h_max, s_max, v_max])
        mask_color = cv2.inRange(self.hsv_frame, low_color, high_color)
        mask_color = cv2.medianBlur(mask_color, 7)
        s = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opened = cv2.morphologyEx(mask_color, cv2.MORPH_OPEN, s, iterations=2)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, s, iterations=2)
        edges = cv2.Canny(opened, 50, 100)
        circles = cv2.HoughCircles(
            edges, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=10, minRadius=10, maxRadius=500)
        cv2.imshow("edges", edges)
        if circles is not None:  # 如果识别出圆
            for circle in circles[0]:
                #  获取圆的坐标与半径
                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])
                cv2.circle(src_frame, (x, y), r, (0, 0, 255), 3)  # 标记圆
                cv2.circle(src_frame, (x, y), 3, (255, 255, 0), -1)  # 标记圆心
                text = 'x:  '+str(x)+' y:  '+str(y)
                cv2.putText(src_frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)  # 显示圆心位置
        else:
            # 如果识别不出，显示圆心不存在
            cv2.putText(src_frame, 'x: None y: None', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA, 0)
        '''
        cnts, hierarchy = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in cnts:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)  
            cv2.putText(result, 'target', (x, y - 5), font, 0.7, (0, 0, 255), 2)          
        '''
def nothing(x):
    pass


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cd = ColorDetect()
    cv2.namedWindow('img')
    cv2.createTrackbar("H_MIN","img",36,180,nothing)
    cv2.createTrackbar("H_MAX","img",38,180,nothing)
    cv2.createTrackbar("S_MIN","img",117,255,nothing)
    cv2.createTrackbar("S_MAX","img",121,255,nothing)
    cv2.createTrackbar("V_MIN","img",148,255,nothing)
    cv2.createTrackbar("V_MAX","img",160,255,nothing)
    cv2.setMouseCallback("img", cd.mouse_click)

    while True:
        ret, frame = cap.read()
        h_min = cv2.getTrackbarPos("H_MIN","img")
        h_max = cv2.getTrackbarPos("H_MAX","img")
        s_min = cv2.getTrackbarPos("S_MIN","img")
        s_max = cv2.getTrackbarPos("S_MAX","img") 
        v_min = cv2.getTrackbarPos("V_MIN","img")
        v_max = cv2.getTrackbarPos("V_MAX","img")
        cd.update_frame(frame, h_min, h_max, s_min, s_max, v_min, v_max)
        cv2.imshow("img", frame)
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()