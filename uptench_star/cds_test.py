##舵机角度控制
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
from up_controller import UpController


if __name__ == '__main__':
    up=uptech.UpTech()
    up.CDS_Open()
    up.CDS_SetMode(1,0)
    up_controller=UpController()
    while True:
#         up_controller.set_chassis_mode(1)
#         up_controller.move_up()
        # up.CDS_SetSpeed(1,500)
        # up.CDS_SetAngle(1,256,800)
        time.sleep(1)
        up.CDS_SetSpeed(2,-500)
        # up.CDS_SetAngle(1,500,256)
        time.sleep(1)

    




