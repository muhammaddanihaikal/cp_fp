from flask import Flask
from flask_restx import Resource, Api, reqparse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from flask import send_file
import json
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///record.db"

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)

@app.route("/database/create", methods=["GET"])
def createDatabase():
    with app.app_context():
        db.create_all()
        return "Database Created Successfully!"

@app.route("/record/all", methods=["GET"])
def getAllTimes():
    records = db.session.execute(db.select(Record).order_by(Record.id)).scalars()
    data = []
    for record in records:
        data.append({
            'id': record.id,
            'method': record.method,
            'file': record.file,
            'time': record.time,
        })
    return json.dumps(data)

#form upload image
uploadParser = api.parser()
uploadParser.add_argument('file', location='files', type=FileStorage, required=True)
@api.route('/image')
class ImageAPI(Resource):
    @api.expect(uploadParser)
    def post(self):
        args = uploadParser.parse_args()
        file = args['file']
        file.save(file.filename)

        method = 'POST'
        date_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        record = Record(
            method=method,
            file=file.filename,
            time=date_now
        )
        db.session.add(record)
        db.session.commit()

        #buat AI
        # return send_file(file.filename)
        return {'method': method,
                'file': file.filename,
                'time': date_now
                }
    def get(self):
        filename = 'riyan.png'
        method = 'GET'
        date_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        record = Record(
            method=method,
            file=filename,
            time=date_now
        )
        db.session.add(record)
        db.session.commit()

        # return send_file(filename, mimetype='image/jpg')
        return {'method': method,
                'file': filename,
                'time': date_now
                }

if __name__ == '__main__':
    app.run(debug=True)