import paho.mqtt.client as mqtt #MQTT 통신을 사용하기 위해 paho-mqtt 라이브러리 불러오기
import time                     #시간 지연 기능을 사용하기 위해 time 라이브러리 불러오기
from gpiozero import LED        #GPIO핀으로 LED를 제어하기 위해 LED 클래스 불러오기
import threading                #발행과 구독을 동시에 처리하기 위한 threading 라이브러리 불러오기 

greenLed = LED(16)              #GPIO 16번핀에 연결된 초록 LED 객체 생성
blueLed = LED(20)               #GPIO 20번핀에 연결된 파랑 LED 객체 생성
redLed = LED(21)                #GPIO 21번핀에 연결된 빨강 LED 객체 생성

def on_message(client, userdata, msg):    #브로커로부터 메시지가 수신 시 자동으로 실행되는 콜백 함수
    print(msg.topic+" "+str(msg.payload)) #수신한 메시지의 토픽과 페이로드를 터미널에 출력
    message = msg.payload.decode()        #바이트 형태의 페이로드를 문자열로 변환
    print(message)                        #문자열로 변환된 메시지를 터미널에 출력
    if message == "green_on":             #수신한 메시지가 green_on이면
        greenLed.on()                     #초록 LED를 킴
    elif message == "green_off":          #수신한 메시지가 green_off면
        greenLed.off()                    #초록 LED를 끔
    elif message == "blue_on":            #수신한 메시지가 blue_on이면
        blueLed.on()                      #파랑 LED를 켬
    elif message == "blue_off":           #수신한 메시지가 blue_off면
        blueLed.off()                     #파랑 LED를 끔
    elif message == "red_on":             #수신한 메시지가 red_on이면
        redLed.on()                       #빨강 LED를 켬
    elif message == "red_off":            #수신한 메시지가 red_off면
        redLed.off()                      #빨강 LED를 끔

client = mqtt.Client()                    #MQTT 통신을 위한 클라이언트 객체 생성
client.on_message = on_message            #메시지를 수신하면 on_message 함수가 실행되도록 설정

broker_address="192.168.0.54"             #MQTT 브로커가 실행중인 라즈베리파이의 IP 주소 설정
client.connect(broker_address)            #설정한 브로커 주소로 MQTT 클라이언트 연결
client.subscribe("led",1)                 #led 토픽을 구독하여 pc에서 보내는 LED 제어 메시지를 수신
                                          #(QoS 1로 설정 = 메시지 최초 1회 수신 보장)

count = 0                                 #hello 토픽으로 발행할 숫자 데이터의 초기값 설정
def send_thread():                        #hello 토픽으로 데이터를 계속 발행하는 스레드 함수 정의
    global count                          #함수 외부에서 선언한 count 변수를 함수 안에서 사용하기 위함
    while 1:                              #무한반복
        count = count + 1                 #count의 값이 1씩 증가 
        client.publish("hello", str(count))  #hello 토픽으로 증가한 count 값을 문자열 형태로 발행
        time.sleep(1.0)                   #1초 동안 대기한 후 다시 반

task = threading.Thread(target = send_thread)  #send_thread() 함수를 별도의 스레드 작업으로 생
task.start()                                   #스레드를 시작하여 발행과 구독을 동시에 실행

client.loop_forever()                          #MQTT 메시지를 계쏙 수신하기 위해 무한 대기 상태 실행
