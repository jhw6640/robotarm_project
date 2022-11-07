# !/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import random
import time
from Arm_Lib import Arm_Device
import threading

import demjson
import pygame 
from aip import AipBodyAnalysis
from aip import AipSpeech
from PIL import Image, ImageDraw, ImageFont

class gesture_action:
    def __init__(self):

        self.Arm = Arm_Device()
        self.color_name = None
        self.image = None

        self.look_at = [90, 164, 18, 0, 90, 90]
        self.p_top = [90, 80, 50, 50, 270]

        self.p_Yellow = [64, 25, 65, 53, 270]
        self.p_Red = [117, 24, 61, 59, 270]

        self.p_Green = [137, 63, 26, 21, 270]
        self.p_Blue = [44, 66, 20, 24, 265]

        self.p_gray = [90, 52, 37, 29, 270]

        self.p_Prayer = [90, 90, 0, 180, 90, 180] 
        self.p_Thumb_up = [90, 90, 90, 90, 90, 180] 
        self.p_Heart_single = [90, 0, 180, 0, 90, 90] 

        self.p_Eight = [90, 180, 18, 0, 90, 90] 

        self.p_Congratulation = [90, 131, 52, 0, 90, 180]
        self.p_Rock = [90, 0, 90, 180, 90, 0]
        self.p_fist = [90, 90, 0, 0, 90, 0]
        self.p_horse_1 = [90, 7, 153, 19, 0, 126]
        self.p_horse_2 = [90, 5, 176, 0, 0, 180]
        self.p_horse_3 = [90, 62, 158, 0, 0, 0]

        self.g_state_arm = 0
        self.started = 0
        self.running = 0

        

    def cv2ImgAddText(self, img, text, left, top, textColor=(0, 255, 0), textSize=20):
        print("cv2ImgAddText-----in")
        if (isinstance(img, np.ndarray)):  
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        draw = ImageDraw.Draw(img)

        fontStyle = ImageFont.truetype(
            "simhei.ttf", textSize, encoding="utf-8")

        draw.text((left, top), text, textColor, font=fontStyle)
        print("cv2ImgAddText-----out")

        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    def ctrl_arm_move(self, index):
        if index == "Prayer":
            self.Arm.Arm_serial_servo_write6_array(self.p_Prayer, 1000)
            time.sleep(1.5)
            self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
            time.sleep(1)
        elif index == "Thumb_up":
            s_time = 500
            self.Arm.Arm_serial_servo_write(6, 180, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(6, 90, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(6, 180, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(6, 90, s_time)
            time.sleep(s_time/1000)
        elif index == "Ok":
            s_time = 300
            self.Arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
        elif index == "Heart_single":
            self.Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 30], 800)
            time.sleep(1.5)
            self.Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 90], 800)
            time.sleep(1)
            self.Arm.Arm_serial_servo_write6_array(self.p_Heart_single, 1000)
            time.sleep(1)
        elif index == "Five":
            self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
            time.sleep(.5)
        elif index == "Eight":
            s_time = 300
            self.Arm.Arm_serial_servo_write6_array(self.p_Eight, 0)
            time.sleep(1)
            self.Arm.Arm_serial_servo_write(2, 165, s_time)
            time.sleep(s_time/1000)
        elif index == "Rock": #rock
            self.Arm.Arm_serial_servo_write6_array(self.p_Rock, 1300)
            time.sleep(3)
            self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
            time.sleep(1)
        elif index == "Thumb_down": 
            self.Arm.Arm_serial_servo_write6_array(self.p_horse_1, 1300)
            time.sleep(1) 
        elif index == "Congratulation": 
            self.Arm.Arm_serial_servo_write6_array(self.p_horse_2, 1000)
            time.sleep(1)
            self.running = 1
            while self.running == 1:
                self.horse_running()
        elif index == "Seven":
            self.Arm.Arm_Buzzer_On(8)   
            self.Arm.Arm_serial_servo_write6_array(self.p_horse_3, 1000)
            time.sleep(2)
            self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
            time.sleep(1)
        
        else:
            pass
        self.g_state_arm = 0


    def arm_move(self, p, s_time = 500):
        for i in range(5):
            id = i + 1
            if id == 5:
                time.sleep(.1)
                self.Arm.Arm_serial_servo_write(id, p[i], int(s_time*1.2))
            elif id == 1 :
                self.Arm.Arm_serial_servo_write(id, p[i], int(3*s_time/4))
            else:
                self.Arm.Arm_serial_servo_write(id, p[i], int(s_time))
            time.sleep(.01)
        time.sleep(s_time/1000)
    

    def arm_clamp_block(self, enable):
        if enable == 0:
            self.Arm.Arm_serial_servo_write(6, 60, 400)
        else:
            self.Arm.Arm_serial_servo_write(6, 135, 400)
        time.sleep(.5)


    def horse_running(self):
        # Arm.Arm_serial_servo_write6_array(p_horse_1, 300)
        # time.sleep(.3)
        # Arm.Arm_serial_servo_write6_array(p_horse_2, 300)
        # time.sleep(.3)
            
        self.Arm.Arm_serial_servo_write(6, 150, 300)
        time.sleep(.3)
        self.Arm.Arm_serial_servo_write(6, 180, 300)
        time.sleep(.3)


    def number_action(self, index):
        if index == 1:

            self.arm_move(self.p_top, 1000)
            self.arm_move(self.p_Yellow, 1000)
            self.arm_clamp_block(1)
            self.arm_move(self.p_top, 1000)
        elif index == 2:

            self.arm_move(self.p_top, 1000)
            self.arm_move(self.p_Red, 1000)
            self.arm_clamp_block(1)
            self.arm_move(self.p_top, 1000)
        elif index == 3:

            self.arm_move(self.p_top, 1000)
            self.arm_move(self.p_Green, 1000)
            self.arm_clamp_block(1)
            self.arm_move(self.p_top, 1000)
        elif index == 4:

            self.arm_move(self.p_top, 1000)
            self.arm_move(self.p_Blue, 1000)
            self.arm_clamp_block(1)
            self.arm_move(self.p_top, 1000)

  
    def put_down_block(self):
        self.arm_move(self.p_gray, 1000)
        self.arm_clamp_block(0) 
        self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
        time.sleep(1)

    def start_move_arm(self, index):

        if self.g_state_arm == 0:
            self.g_state_arm = 1
            closeTid = threading.Thread(target = self.ctrl_arm_move, args = [index])
            closeTid.setDaemon(True)
            closeTid.start()
            # self.ctrl_arm_move(index)
        if self.running == 1 and index == "Seven":
            self.running = 0


    def bgr8_to_jpeg(self, value, quality=75):
        return bytes(cv2.imencode('.jpg', value)[1])

    def Gesture_Action(self, gesture):
        self.start_move_arm(gesture) 
    
    def reset_state(self):
        self.started = 0

    def start_gesture(self, frame):

        if self.started == 0:

            self.hand = {'One':'number1','Two':'number2','Three':'number3','Four':'number4',
                          'Five':'number5', 'Six':'number6','Seven':'number7',
                          'Eight':'number8','Nine':'number9','Fist':'fist','Ok':'OK',
                          'Prayer':'prayer','Congratulation':'congratulation','Honour':'honour',
                          'Heart_single':'heart','Thumb_up':'thumb_up','Thumb_down':'Diss',
                          'ILY':'i love you','Palm_up':'palm_up','Heart_1':'Heart_1',
                          'Heart_2':'Heart_1','Heart_3':'Heart_3','Rock':'Rock','Face':'face'}

            """ APPID AK SK """
            self.APP_ID = '18550528'
            self.API_KEY = 'K6PWqtiUTKYK1fYaz13O8E3i'
            self.SECRET_KEY = 'IDBUII1j6srF1XVNDX32I2WpuwBWczzK'

            self.client = AipBodyAnalysis(self.APP_ID, self.API_KEY, self.SECRET_KEY)

            self.Arm.Arm_serial_servo_write6_array(self.look_at, 1000)
            time.sleep(1.2)

            self.Arm.Arm_Buzzer_On(1)
            s_time = 300
            self.Arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 10, s_time)
            time.sleep(s_time/1000)
            self.Arm.Arm_serial_servo_write(4, 0, s_time)
            time.sleep(s_time/1000)
            self.started = 1

        raw = str(self.client.gesture(self.bgr8_to_jpeg(frame)))
        text = demjson.decode(raw)
        try:
            res = text['result'][0]['classname']
        except:
            # print('nothing' )
            # img = self.cv2ImgAddText(frame, "unrecognized", 250, 30, (0, 0 , 255), 30)
            self.image = frame
            res = ''
        else:
            # print('Recognition result:' + self.hand[res])
            # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
            # self.image = cv2.putText(frame, res, (450, 50),
            # cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            if res == 'Prayer': 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res) 
            elif res == 'Thumb_up':
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == 'Ok': 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == 'Heart_single': 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == 'Five': 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == "Eight": 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == "Rock": # rock
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            # elif res == "Congratulation":
            #     print('Recognition result:' + self.hand[res])
            #     # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
            #     self.image = cv2.putText(frame, res, (450, 50),
            #                             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            #     self.start_move_arm(res)
            elif res == "Seven": 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            elif res == "Thumb_down": 
                print('Recognition result:' + self.hand[res])
                # img = self.cv2ImgAddText(frame, self.hand[res], 250, 30, (0, 255 , 0), 30)
                self.image = cv2.putText(frame, res, (450, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                self.start_move_arm(res)
            else:
                self.image = frame
                res = ''
            
        return self.image, res


