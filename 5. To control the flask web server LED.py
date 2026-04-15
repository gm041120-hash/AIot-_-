from flask import Flask, request, render_template #Flask 웹을 만들기 위해 flask 라이브러리에서 Flask, request, render_template을 가져옴
                                                  # Flask는 웹서버의 기본 틀을 만들고, request는 웹서버에서 보낸 데이터를 받아옴
                                                  # render_template는 HTML파일을 불러와서 사용하기 위해 씀
from gpiozero import LED                          # LED 제어를 위해 gpiozero 라이브러리에서 LED 클래스를 가져옴

app = Flask(__name__)                             # Flask 앱을 생성

red_led = LED(21)                                 # 21번 핀에 연결된 LED를 제어하기 위해 설정

@app.route('/')                                   # 기본주소인 (/)에 접속했을 때 밑에 home함수 실행
def home():                                       
   return render_template("led.html")             #led.html 파일을 가져와 브라우저에 출력

@app.route('/data', methods = ['POST'])           # /data 주소로 POST 방식의 요청이 들어왔을 때 아래 data함수 실행
def data(): 
    data = request.form['led']                    # 브라우저에서 led값을 받아옴
    
    if(data == 'on'):                             # 받아온 led값이 on일때
        red_led.on()                              # led를 켬
        return home()                             # 다시 첫화면으로 돌아감

    elif(data == 'off'):                          # 받아온 led값이 off일때
        red_led.off()                             # led를 끔
        return home()                             # 다시 첫화면으로 돌아

if __name__ == '__main__':                        
   app.run(host = '0.0.0.0', port = '80')         # 모든 IP(0.0.0.0)에서 80번 포트로 서버 실행
