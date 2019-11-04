import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from flask_restplus import Resource, Api
from werkzeug.utils import secure_filename
from app import app
from app.detector import DetectImg
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        print(app.config['RESULT_FOLDER'])
        return {'hello': 'world'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload_img', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('detect_image',
                                    filename=filename))
    return render_template('upload.html')


@app.route('/result/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'],
                               filename)


@app.route('/detect_image/<filename>')
def detect_image(filename):
    DetectImg(filename)
    # return send_from_directory(app.config['RESULT_FOLDER'], filename)
    src_image = f"http://localhost:5000/result/{filename}"
    return render_template('upload.html', src_image=src_image)
