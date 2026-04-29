import urllib.request     #URL을 열고 데이터를 받아오기 위한 라이브러리
import json               #json 형식의 데이터를 처리하기 위한 라이브러리
import datetime           #현재 날짜와 시간을 사용하기 위한 라이브러리
import asyncio            #비동기 실행을 위한 라이브러리
from telegram import Bot  #텔레그램 봇을 사용하기 위한 Bot클래스
from telegram.request import HTTPXRequest  #텔레그램 요청 시간 제한 설정을 위한 클래스

telegram_id = 'id' #텔레그램 id 입력
my_token = 'token' #텔레그램 봇 토큰 입력
api_key = 'api' #OpenWeatherMap api키 입력

request = HTTPXRequest(
    connect_timeout=30,   #서버 연결을 최대 30초까지 기다리도록 설정
    read_timeout=30,      #서버 응답 읽기를 최대 30초까지 기다리도록 설정
    write_timeout=30,     #메시지 전송을 최대 30초까지 기다리도록 설정
    pool_timeout=30)      #연결 대기를 최대 30초까지 기다리도록 설정

bot = Bot(token=my_token, request=request)   #토큰과 요청 설정을 이용해 텔레그램 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22]    #3시간 간격 정각 알림 보낼 시간들을 저장하는 리스트
ALERT_TIMES = ["08:30", "14:40"]         #특정 시간에 알림을 보낼 시간들을 저장하는 리스트

def getWeather():  #날씨 정보를 가져오는 함수
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"
    #서울 날씨 예보 데이터를 요청하기 위해 url 저장
    with urllib.request.urlopen(url) as r:  #url을 열어 날씨 데이터를 받아옴
        data = json.loads(r.read())         #받은 데이터를 파이썬에서 사용할 수 있는 형태로 변환

    text = ""  #텔레그램으로 보낼 메시지를 저장할 문자열
    for i in range(8): #8번 반복문
        item = data['list'][i]  #i번째 예보 데이터를 가져와 item에 저장
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2) 
        #예보 시간에서 시(hour)만 꺼내서 한국시간으로 바꾸고 2자리로 맞춰서 저장
        temp = item['main']['temp']  #예보 데이터에서 온도값을 가져와 저장
        humi = item['main']['humidity']  #예보 데이터에서 습도값을 가져와 저
        desc = item['weather'][0]['description']  #예보 데이터에서 날씨 정보를 가져와 저장
        text += f"({hour}h {temp}C {humi}% {desc})\n" #시간, 온도, 습도, 날씨 정보를 한줄로 만들어 text에 추가

    return text #완성된 문자열 반

async def main():  #텔레그램 메시지 전송 함수
    try: #try-except 시작
        while True:  #무한반복문
            now = datetime.datetime.now() #현재날짜와 시간을 가져옴
            hm = now.strftime('%H:%M')    #현재 시간을 시:분 형태의 문자열로 저

            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0 
            #현재 시간이 ALERT_HOURS에 포함된 시간인지
            is_alert_time = hm in ALERT_TIMES and now.second == 0                            
            #현재 시간이 ALERT_TIMES에 포함된 시간인지
            if is_alert_hour or is_alert_time:  #위에 둘 중 하나에 해당되면 밑에 내용 실행  
                msg = getWeather()    #날씨 정보를 가져와 msg에 저장
                print(msg)            #날씨 정보를 터미널에 출력
                await bot.send_message(chat_id=telegram_id, text=msg)  #chat_id는 메시지를 받을 대상을, text는 메시지 내용을 의미

   
            await asyncio.sleep(1)  #1초 쉬었다가 다시 반복

    except KeyboardInterrupt:        #컨트롤 + c로 키보드인터럽트를 통해 무한반복문 종료
        pass                         #아무 행동도 취하지 않고 넘어

asyncio.run(main())                  #비동기 메인 함수를 실행해 프로그램 시작
