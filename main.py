import os

from flask import Flask
from flask_restx import Resource, Api, reqparse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = './image'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "dani"

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import send_file
uploadParser = api.parser()
uploadParser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/image')
class ImageAPI(Resource):
    @api.expect(uploadParser)
    def post(self):
        args = uploadParser.parse_args()
        file = args['file']
        filename = secure_filename(file.filename)
        # file.save(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # return send_file(file.filename)
        return {'path': os.path.join(app.config['UPLOAD_FOLDER'], file.filename)}
    def get(self):
        filename = './image/acer_oridyct_regustratuib.png'
        return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True)