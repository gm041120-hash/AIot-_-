from gpiozero import MotionSensor   #gpiozero 라이브러리에서 MotionSensor 클래스를 가져옴
import time                         #time 라이브러리를 가져
from picamera2 import Picamera2     #picamera2 라이브러리에서 Picamera2 클래스를 가져옴
import datetime                     #날짜/시간 처리를 위한 datetime 라이브러리를 가져옴

pirPin = MotionSensor(16)           #GPIO 16번 핀을 PIR 모션 센서 입력 핀으로 초기화

picam2 = Picamera2()                                   #
camera_config = picam2.create_preview_configuration()  #
picam2.configure(camera_config)                        #
picam2.start()                                         #

try:                                                          #무한반복문 시작
    while True:
        try:
            sensorValue = pirPin.value                        #
            if sensorValue == 1:                              #
                now = datetime.datetime.now()                 #
                print(now)                                    #
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')  #
                picam2.capture_file(fileName + '.jpg')        #
                time.sleep(0.5)                               #
        except:                                               #
            pass                                              #

except KeyboardInterrupt:                                     #
    pass                                                      #
