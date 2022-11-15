from flask import Flask
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#buat form
parser = reqparse.RequestParser()
parser.add_argument('firstname', type=str, help='Nama Depan')
parser.add_argument('lastname', type=str, help='Nama Belakang')
parser.add_argument('age', type=int, help='Umur')


@api.route('/phb')
class Muhammadfaridbaehaqi(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        firstname = args['firstname']
        lastname = args['lastname']
        age = args['age']
        return {'firstname': firstname, 'lastname': lastname, 'age': age}

    def put(self):
        return "PUT"
    def post(self):
        return "POST"
    def delete(self):
        return "DELETE"

if __name__ == '__main__':
    app.run(debug=True)