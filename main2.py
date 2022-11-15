from flask import Flask
from flask_restx import Resource, Api, reqparse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.String, nullable=False)

@app.route("/database/create", methods=["GET"])
def createDatabase():
    with app.app_context():
        db.create_all()
        return "Database Created Successfully!"

@app.route("/student/all", methods=["GET"])
def getAllStudents():
    students = db.session.execute(db.select(Student).order_by(Student.nim)).scalars()
    data = []
    for student in students:
        data.append({
            'nim': student.nim,
            'firstname': student.firstname,
            'lastname': student.lastname,
            'birthdate': student.birthdate,
        })
    return json.dumps(data)

parser4Param = reqparse.RequestParser()
parser4Param.add_argument('firstname', type=str, help='Nama Depan', location='args')
parser4Param.add_argument('lastname', type=str, help='Nama Belakang', location='args')
parser4Param.add_argument('birthdate', type=str, help='Tanggal Lahir', location='args')
parser4Body = reqparse.RequestParser()
parser4Body.add_argument('firstname', type=str, help='Nama Depan', location='form')
parser4Body.add_argument('lastname', type=str, help='Nama Belakang', location='form')
parser4Body.add_argument('birthdate', type=str, help='Tanggal Lahir', location='form')

@api.route('/student/<string:nim>')
class StudentAPI(Resource):
    def get(self, nim):
        students = db.session.execute(db.select(Student).filter_by(nim=nim)).first()
        if(students is None):
            return f"Data Mahasiswa dengan NIM {nim} tidak ditemukan!"
        else:
            student = students[0]
            bDate = datetime.strptime(student.birthdate, "%Y-%m-%d")
            today = datetime.today()
            age = (today.year-bDate.year)
            return { 'METHOD': "GET",
                     'id': student.id,
                     'nim': student.nim,
                     'firstname': student.firstname,
                     'lastname': student.lastname,
                     'birthdate': student.birthdate,
                     'age': f'{age} tahun', 'status': 200,
                     }
    @api.expect(parser4Body)
    def post(self, nim):
        args = parser4Body.parse_args()
        firstname = args['firstname']
        lastname = args['lastname']
        birthdate = args['birthdate']
        bDate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = (today.year-bDate.year)
        student = Student(
            nim=nim,
            firstname=firstname,
            lastname=lastname,
            birthdate=birthdate, )
        db.session.add(student)
        db.session.commit()
        return { 'nim': nim,
                 'firstname': firstname,
                 'lastname': lastname,
                 'birthdate': birthdate,
                 'age': f'{age} tahun',
                 'status': 200,
                 'message': f"Data Mahasiswa dengan NIM {nim} berhasil ditambahkan!"
                 }
    @api.expect(parser4Body)
    def put(self, nim):
        args = parser4Body.parse_args()
        firstname = args['firstname']
        lastname = args['lastname']
        birthdate = args['birthdate']
        bDate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = (today.year-bDate.year)
        students = db.session.execute(db.select(Student).filter_by(nim=nim)).first()
        if(students is None):
            return f"Data Mahasiswa dengan NIM {nim} tidak ditemukan!"
        else:
            student = students[0]
            student.firstname = firstname
            student.lastname = lastname
            student.birthdate = birthdate
            db.session.commit()
            return { 'METHOD': "PUT",
                     'nim': nim,
                     'firstname': firstname,
                     'lastname': lastname,
                     'birthdate': birthdate,
                     'age': f'{age} tahun',
                     'status': 200,
                     'message': f"Data Mahasiswa dengan NIM {nim} berhasil diubah!"
                     }
    def delete(self, nim):
        students = db.session.execute(db.select(Student).filter_by(nim=nim)).first()
        if(students is None):
            return f"Data Mahasiswa dengan NIM {nim} tidak ditemukan!"
        else:
            student = students[0]
            db.session.delete(student)
            db.session.commit()
            return f"Data Mahasiswa dengan NIM {nim} berhasil dihapus!"

from werkzeug.datastructures import FileStorage
from flask import send_file
uploadParser = api.parser()
uploadParser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/image/<string:nim>')
class ImageAPI(Resource):
    @api.expect(uploadParser)
    def post(self, nim):
        args = uploadParser.parse_args()
        file = args['file']
        file.save(file.filename)
        #buat AI
        # return send_file(file.filename)
        return {'nim': nim,
                'filename': file.filename,
                'message': 'SUCCESSFUL'
                }
    def get(self, nim):
        filename = 'riyan.png'
        return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)