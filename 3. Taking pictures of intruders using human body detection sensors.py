from gpiozero import MotionSensor   #gpiozero 라이브러리에서 MotionSensor 클래스를 가져옴
import time                         #time 라이브러리를 가져
from picamera2 import Picamera2     #picamera2 라이브러리에서 Picamera2 클래스를 가져옴
import datetime                     #날짜/시간 처리를 위한 datetime 라이브러리를 가져옴

pirPin = MotionSensor(16)           #GPIO 16번 핀을 PIR 모션 센서 입력 핀으로 초기화

picam2 = Picamera2()                                   #Picamera2 객체 생성
camera_config = picam2.create_preview_configuration()  #카메라 미리보기 설정 구성
picam2.configure(camera_config)                        #카메라에 설정 적용
picam2.start()                                         #카메라 시작

try:                                                          #무한반복문 시작
    while True:
        try:
            sensorValue = pirPin.value                        #PIR 센서의 현재 값을 변수 sensorValue에 저장
            if sensorValue == 1:                              #sensorValue가 1일때(움직임이 감지 되었을 때) 작동
                now = datetime.datetime.now()                 #now에 현재 날짜와 시간을 저장
                print(now)                                    #저장한 날짜와 시간을 터미널에 출력
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')  #now에 저장된 시각을 년-월-일 시:분:초 형태의 문자열로 바꿔 파일이름으로 만듦
                picam2.capture_file(fileName + '.jpg')        #위에서 만든 파일 이름에 .jpg를 붙여 사진을 촬영하고 저장함. 
                                                              #이때 경로를 따로 저장하지 않아서 실행된 파이썬 코드가 있는 파일에 저장됨.
                time.sleep(0.5)                               #사진이 너무 많이 찍히는 것을 방지하기 위해 0.5초 대기 시간을 검
        except:                                               #센서가 작동하여 사진을 찍고 터미널에 값을 출력하는동안 에러가 나면
            pass                                              #그냥 무시하고 진행

except KeyboardInterrupt:                                     #KeboardInterrupt 발생시 
    pass                                                      #다른 행동 없이 종료
