from gpiozero import LEDBoard  # gpiozero 라이브러리에서 LEDBoard 클래스를 가져옴
from time import sleep  # time 라이브러리에서 sleep 함수를 가져옴

leds = LEDBoard(2, 3, 4, 20, 21)
# main 2와 다르게 2, 3, 4, 20, 21번 GPIO 핀에 연결된 LED들을 LED가 아닌 LEDBorad로 한번에 처리함
# 순서대로 1번은 gpio 2, 2번은 gpio 3 ...해서 들어감

# try - except 과 while 1로 무한반복
try:
    while 1:
        leds.value = (0, 0, 1, 1, 0)
        # leds.value는 leds의 현재 상태.
        # 현재 상태를 True=1/False=0으로 설정을 함
        # leds.value = (0,0,1,1,0)는 자동차 초록불과 사람 빨강불만 켜짐
        sleep(3.0)  # 현재 상태를 3초간 유지.
        leds.value = (0, 1, 0, 1, 0)  # 위와 같은 원리로 자동차 노랑(파랑)불과 사람 빨간불만 켜짐
        sleep(1.0)  # 현재 상태를 1초간 유지.(노랑불이 다른 신호보다 짧으니까)
        leds.value = (1, 0, 0, 0, 1)  # 위와 같은 원리로 자동차 빨강불과 사람 초록불만 켜짐
        sleep(3.0)  # 위와 동일.

except KeyboardInterrupt:  # 컨트롤 + C를 눌러  KeyboardInterrupt라는 예외를 발생시켜 무한반복을 멈춤
    pass  # KeyboardInterrupt가 발생했을 때 아무작업 없이 다음으로 넘어감

leds.off()  # 마지막에 모든 신호를 종료함.
sleep(5) #신호 종료가 유지가 되지 않아 sleep로 잠시 유지
