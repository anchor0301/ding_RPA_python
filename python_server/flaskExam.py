from flask import Flask , request, render_template
import GY

app = Flask(__name__)

# 현재는 GET만 허용되었다.
# POST까지 허가를 요청한다면 -> 추가 코드 필요...
#@app.route('/login')  <- GET 만 허가 된것..
# 1개의 url에서 GET방식과 POST방식을 모두 지원하고 싶다 -> Restful 방식 : url을 최소로 사용..
@app.route('/logi', methods=['GET', 'POST']) #GET, POST 모두 허가됨...
def login():
    # 분기
    if request.method == 'GET': #GET방식으로 들어오면..
        return render_template('login.html')
    else:
        # 전달된 데이터 추출 : 아이디, 비번 추출...
        # POST
        # 1. 전달된 아이디,비번을 뽑는다.
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        GY.GY(uid,upw)
        # 2. 아이디, 비번을 가지고 데이터베이스에 쿼리를 수행 (사전에 이미 가입이 되어 있어야 한다...)
        # 3. 수행결과를 받는다
        # 4. 회원이면 -> 서비스 페이지로 이동
        # 5. 회원 아니면 => 아이디 혹은 비번이 틀립니다.. -> 회원가입 유도, 재 로그인 유도
        return 'POST 방식으로 데이터가 잘 전달 됨.'

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=80)
