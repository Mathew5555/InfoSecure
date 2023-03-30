import os
from flask import Flask, flash, request, redirect, url_for, make_response, render_template
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/HappyMatDuckling/mysite/data'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'doc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """ Проверка расширения файла """
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('Файл не читается')
            return redirect(request.url)
        file = request.files['file']
        if not file.filename:
            flash('Нет выбранного файла')
            return redirect("/")
        if file and allowed_file(file.filename):
            my_file = request.files["input_file"]
            data = my_file.stream.read().decode("utf-8")
            with open(f"{app.config['UPLOAD_FOLDER']}/data/bad_sites.txt", "at", encoding="utf8") as block_sites:
                block_sites.write(data)
            return redirect("/")

    return  render_template('base.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], "bad_sites.txt")


if __name__ == '__main__':
    app.run(host="127.0.0.2", port=5000)
