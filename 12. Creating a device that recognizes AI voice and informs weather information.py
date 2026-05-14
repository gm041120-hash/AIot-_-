import speech_recognition as sr  #음성인식 기능을 사용하기 위하나 라이브러리
import requests                  #OpenWeatherMap API에 HTTP 요청을 보내기 위한 라이브러리
import os                        #운영체제 명령어를 실행하기 위한 라이브러리
import time                      #시간 관련 기능을 사용하기 위한 라이브러리

API_KEY = "API"                  #OpenWeatherMap API 키 입력
#서울의 현재 날씨 정보를 요청할 API 주소 설정
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

def speak(option, msg):  #텍스트를 음성으로 출력하는 함수 정의
    os.system("espeak {} '{}'".format(option, msg))  #espeak 명령어를 실행해 msg 내용을 음성으로 출력

try:  
    while True:  #음성 입력을 계속 받기 위한 무한반복
        r = sr.Recognizer()  #음성인식을 위한 Recognizer 객체 생성
        
        with sr.Microphone() as source:  #마이크를 음성 입력 장치로 설정
            print("Say something!")      #사용자에게 말하라는 안내 문구 출력
            audio = r.listen(source)     #마이크로 입력된 음성을 오디오 데이터로 저장
            
        try:
            text = r.recognize_google(audio, language='ko-KR')  #녹음된 음성을 한국어 텍스트로 변환
            print("You said: " + text)                          #음성 텍스트를 터미널에 출
            if text in "날씨":                                  #인식된 텍스트에 날씨가 포함되어있는지 확인
                print("날씨 음성을 인식하였습니다.")             #날씨 음성 인식 성공 메시지 출력
                response = requests.get(url)                    #OpenWeatherMap API에 서울 날씨 정보 요청
                data = response.json()                          #API 응답 데이터를 JSON 형식으로 변환
                temp = data["main"]["temp"]                     #JSON 데이터에서 현재 기온 값 추출
                humi = data["main"]["humidity"]                 #JSON 데이터에서 현재 습도 값 추출

                #기온과 습도 정보를 한글 안내 문장으로 저장
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                option = '-s 180 -p 50 -a 200 -v ko+f5' #espeak 음성 속도, 음높이, 음량, 한국어 음성 옵션 설정
                speak(option, msg)                      #설정한 옵션으로 날씨 안내 문장을 음성 출력
            
        except sr.UnknownValueError:  #음성은 입력되었지만 내용을 인식하지 못한 경
            print("Google Speech Recognition could not understand audio") #음성 인식 실패 메시지 출력
        except sr.RequestError as e:  #Google Speech Recognition 서비스 요청에 실패한 경우
            print("Could not request results from Google Speech Recognition service; {0}".format(e)) #요청 실패 오류 메시지 출력

except KeyboardInterrupt: #컨트롤 + C를 눌러 프로그램 종료를 요청한 경우
    pass                  #아무 행동 없이 처리
