from gpiozero import DigitalInputDevice #gpiozero 라이브러리에서 DigitalInputDevice 클래스를 가져옴
from gpiozero import OutputDevice       #gpiozero 라이브러리에서 OutputDevice 클래스를 가져옴
import time                             #time 라이브러리를 가져옴

bz = OutputDevice(18)                   #GPIO 18번 핀을 부저 제어 핀으로 초기화시킴
gas = DigitalInputDevice(17)            #GPIO 17번 핀을 MQ2 센서 입력 핀으로 초기화

try:                                    #무한루프 시작
    while True:
        if gas.value == 0:              #가스감지센서의 값이 0이면(가스가 감지된 상황)
            print("gas")                #"gas" 출력
            bz.on()                     #부저가 켜져서 소리가 남
        else:                           #그 외(가스가 감지되지 않은 상황, 가스감지센서의 값이 1일 때)
            print("no gas")             # "no gas" 출력
            bz.off()                    #부저를 꺼서 소리를 멈춤

        time.sleep(0.2)                 #반복문이 진행하는 동안 0.2초 간격으로 센서 값을 확인함

except KeyboardInterrupt:               #예외처리 : KeyboardInterrupt(컨트롤 + C) -> try 구문 멈춤
    pass                                #에러를 띄우지 않고 아무 작동 없이 넘어감

bz.off()                                #마지막으로 부저를 꺼줌
