from flask import Flask, request, render_template
from GY import worksheet
import Add_PhoneNumber.hide_api
from line_notify import LineNotify

error_notify = LineNotify(Add_PhoneNumber.hide_api.ERROR_TOKEN)



app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True)