from flask import Flask, request, render_template
from GY import worksheet
import Add_PhoneNumber.hide_api
from line_notify import LineNotify

error_notify = LineNotify(Add_PhoneNumber.hide_api.ERROR_TOKEN)
global count
count = 0  # 실행횟수

app = Flask(__name__)


# 현재는 GET만 허용되었다.
# POST까지 허가를 요청한다면 -> 추가 코드 필요...
# @app.route('/login')  <- GET 만 허가 된것..
# 1개의 url에서 GET방식과 POST방식을 모두 지원하고 싶다 -> Restful 방식 : url을 최소로 사용..
@app.route('/show', methods=['POST', 'GET'])  # GET, POST 모두 허가됨...
def show():
    error = None
    # 분기
    if request.method == 'get':  # GET방식으로 들어오면..
        # 전달된 데이터 추출 : 아이디, 비번 추출...
        # POST
        last_n = worksheet.col_values(6)
        last_a = len(last_n)

        list_of_dicts = worksheet.get_all_records()
        data_list = []
        i = 4
        for dic in list_of_dicts[-5:]:  # 튜플 안의 데이터를 하나씩 조회해서

            data_dic = {  # 딕셔너리 형태로
                # 요소들을 하나씩 넣음

                'cust_number': last_a - i,
                'dog_name': list(dic.values())[8],
                'breed': list(dic.values())[9],
                'PhoneNumber': "0" + str(list(dic.values())[5])
            }
            i = i - 1
            data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음
        error_notify.send("GET")
        add = request.form['add']
        print("add : ", add)
        error_notify.send("add : ", add)

        return render_template('show.html', error=error, data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김
    else:
        # 전달된 데이터 추출 : 아이디, 비번 추출...
        # POST
        last_n = worksheet.col_values(6)
        last_a = len(last_n)

        list_of_dicts = worksheet.get_all_records()
        data_list = []
        i = 4
        for dic in list_of_dicts[-5:]:  # 튜플 안의 데이터를 하나씩 조회해서

            data_dic = {  # 딕셔너리 형태로
                # 요소들을 하나씩 넣음

                'cust_number': last_a - i,
                'dog_name': list(dic.values())[8],
                'breed': list(dic.values())[9],
                'PhoneNumber': "0" + str(list(dic.values())[5])
            }
            i = i - 1
            data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음

        add = request.form['add']
        print("add : ", add)
        error_notify.send("add : ", add)

        return render_template('show.html', error=error, data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김
    return render_template('show.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
