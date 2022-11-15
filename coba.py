from flask import Flask
from flask_restx import Resource, Api, reqparse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from flask import send_file
import pymysql
pymysql.install_as_MySQLdb()
import json
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://'root':''@127.0.0.1/db_flask"

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=False)

@app.route("/database/create", methods=["GET"])
def createDatabase():
    with app.app_context():
        db.create_all()
        return "Database Created Successfully!"

parser4Param = reqparse.RequestParser()
parser4Param.add_argument('time', type=str, help='time', location='args')
parser4Body = reqparse.RequestParser()
parser4Body.add_argument('time', type=str, help='time', location='form')

#form upload image
uploadParser = api.parser()
uploadParser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/time')
class TimeAPI(Resource):
    def post(self):
        time = datetime.now()
        return {'time': time}

@api.route('/image')
class ImageAPI(Resource):
    @api.expect(uploadParser)
    def post(self):
        args = uploadParser.parse_args()
        file = args['file']
        file.save(file.filename)

        date_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # time = Time(
        #     time=date_now)
        # db.session.add(time)
        # db.session.commit()

        #buat AI
        # return send_file(file.filename)
        return {'time': date_now,
                'filename': file.filename,
                'message': 'SUCCESSFUL'
                }
    def get(self):
        filename = 'riyan.png'
        return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)