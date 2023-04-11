import os
from flask import Flask, flash, request, redirect, url_for, make_response, render_template
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename
from docx import Document

UPLOAD_FOLDER = ''  # '/home/HappyMatDuckling/mysite/'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'doc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'super secret key'


def allowed_file(filename):
    """ Проверка расширения файла """
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if "submit-2" in request.values:
            text = request.values["message"].split("\r\n")
            with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as block_sites:
                lines = list(map(str.strip, block_sites.readlines()))
            with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "at", encoding="utf8") as block_sites:
                for el in text:
                    if el not in lines:
                        block_sites.write(el + "\n")
        else:
            file = request.files['input_file']
            if not file.filename:
                flash('Нет выбранного файла')
                return redirect("/")
            if file and allowed_file(file.filename):
                if file.filename.split('.')[-1].lower() == "txt":
                    data = file.stream.read().decode("utf-8").split()
                else:
                    document = Document(file.filename)
                    data = []
                    for par in document.paragraphs:
                        data.append(par.text)
                with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as block_sites:
                    lines = list(map(str.strip, block_sites.readlines()))
                with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "at", encoding="utf8") as block_sites:
                    for el in data:
                        if el not in lines:
                            block_sites.write(el + "\n")
                return redirect("/")

    return render_template('main_page.html')


@app.route('/list')
def list_sites():
    with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as block_sites:
        params = block_sites.readlines()
    return render_template('site_list.html', params=params)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], "data/bad_sites.txt")


@app.route('/block')
def block_sites():
    return render_template('block.html')


if __name__ == '__main__':
    app.run(host="127.0.0.2", port=5000)
