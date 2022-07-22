from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('formId', type=str)
            parser.add_argument('formTitle', type=str)
            parser.add_argument('results', type=str)
            args = parser.parse_args()

            _userEmail = args['formId']
            _userName = args['formTitle']
            _userPassword = args['results']
            return {'formId': args['formId'], 'formTitle': args['formTitle'], 'results': args['results']}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)