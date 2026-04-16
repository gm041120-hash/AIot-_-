import urllib.request, json, tkinter, tkinter.font  # 웹 요청, JSON 데이터 처리, GUI 창 생성, 폰트 설정에 필요한 라이브러리들을 불러옴

API_KEY = "747397fe4739fee12713f52ce8cdb8fc"  # OpenWeatherMap에서 발급받은 API 키를 저장함

def tick1Min():  # 날씨 정보를 가져와 화면에 표시하는 함수
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"  # 서울의 현재 날씨정보를 요청하는 URL을 만듦
    with urllib.request.urlopen(url) as r:  # url 주소로 접속해 데이터를 요청하고 r로 받음
        data = json.loads(r.read())  # 서버가 보낸 JSON 형식의 데이터를 읽어서 파이썬에서 사용할 수 있는 형태로 변환함
    temp = data["main"]["temp"]  # 받아온 데이터 중 온도를 가져옴
    humi = data["main"]["humidity"]  # 받아 데이터 중 습도 값을 가져옴
    label.config(text=f"{temp:.1f}C   {humi}%")  # 가져온 온도와 습도 값을 문자열로 만들어 라벨 내용을 업데이트
    window.after(60000, tick1Min)  # 1분(60000밀리초) 후에 tick1Min 함수를 다시 실행하도록 예약

window = tkinter.Tk()  # tkinter를 이용해 기본 GUI 창을 생성
window.title("TEMP HUMI DISPLAY")  # 창의 제목을 TEMP HUMI DISPLAY로 설정
window.geometry("400x100")  # 창의 크기를 가로 400, 세로 100으로 설정
window.resizable(False, False)  # 사용자가 창의 가로세로 크기를 변경하지 못하도록 설정
font = tkinter.font.Font(size=30)  # 글자 크기 30의 폰트 객체를 생성
label = tkinter.Label(window, text="", font=font)  # 텍스트 라벨을 생성
label.pack()  # 라벨을 GUI 창 안에 배

tick1Min()  # 프로그램 시작되면 바로 한 번 날씨 정보를 불러오게함
window.mainloop()  # GUI 창을 유지(이벤트 루프)
