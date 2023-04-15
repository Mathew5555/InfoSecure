from flask import Flask, flash, request, redirect, url_for, make_response, render_template
from flask import send_from_directory, send_file
from docx import Document
from form.user import LoginForm
import csv
import os

UPLOAD_FOLDER = ''  # '/home/HappyMatDuckling/mysite/'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'doc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
ADMIN = False


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if "submit-2" in request.values:
            text = request.values["message"].split("\r\n")
            with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as block_sites:
                lines = list(map(str.strip, block_sites.readlines()))
            with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "at", encoding="utf8") as block_sites:
                for el in text:
                    if el not in lines and "." in el and len(el.split(".")) >= 2:
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
                with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "at", encoding="utf8") as block_sites:
                    for el in data:
                        if el not in lines and "." in el and len(el.split(".")) >= 2:
                            block_sites.write(el + "\n")
                return redirect("/")

    return render_template('main_page.html', is_user=ADMIN)


@app.route('/list')
def list_sites():
    with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as block_sites:
        params = block_sites.readlines()
    return render_template('site_list.html', is_user=ADMIN,
                           params=[params[:len(params) // 2], params[len(params) // 2::]])


@app.route('/uploads/bad_sites.txt')
def download_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "data/bad_sites.txt")


@app.route('/block')
def block_sites():
    return render_template('block.html', is_user=ADMIN)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global ADMIN
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == "admin":
            ADMIN = True
            return redirect("/")
        return render_template('login.html', message="Неправильный пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form, is_user=ADMIN)


@app.route('/check')
def check():
    if ADMIN:
        with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "rt", encoding="utf8") as check_sitess:
            params = check_sitess.readlines()
        return render_template('check_liat.html', is_user=ADMIN, params=params)
    return redirect("/")


@app.route('/logout')
def logout():
    global ADMIN
    if ADMIN:
        ADMIN = False
    return redirect("/")


@app.route('/check_add/<site>')
def check_add(site):
    if ADMIN:
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "at", encoding="utf8") as bad_site:
            bad_site.write(site + "\n")
        with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "rt", encoding="utf8") as bad_site:
            list_ = list(map(str.strip, bad_site.readlines()))
            list_.remove(site)
        with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "wt", encoding="utf8") as bad_site:
            for el in list_:
                bad_site.write(el + "\n")
        return redirect("/check")
    return redirect("/")


@app.route('/check_cancel/<site>')
def check_cancel(site):
    if ADMIN:
        list_ = []
        with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "rt", encoding="utf8") as bad_site:
            list_ = list(map(str.strip, bad_site.readlines()))
            list_.remove(site)
        with open(f"{app.config['UPLOAD_FOLDER']}data/check_sites.txt", "wt", encoding="utf8") as bad_site:
            for el in list_:
                bad_site.write(el + "\n")
        return redirect("/check")
    return redirect("/")


@app.route('/delete_site/<site>')
def delete_site(site):
    if ADMIN:
        list_ = []
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as bad_site:
            list_ = list(map(str.strip, bad_site.readlines()))
            list_.remove(site)
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "wt", encoding="utf8") as bad_site:
            for el in list_:
                bad_site.write(el + "\n")
        return redirect("/list")
    return redirect("/")


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if request.method == "POST":
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as bad_site:
            list_ = list(map(str.strip, bad_site.readlines()))
        if request.values['domain'] not in list_:
            return render_template('error.html', is_user=ADMIN)
        with open(f"{app.config['UPLOAD_FOLDER']}data/complaints.csv", 'a', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([request.values['domain'], request.values['message']])
        return render_template('we_get_complaint.html', is_user=ADMIN)
    return render_template('send_complaint.html', is_user=ADMIN)


@app.route('/check_complaint')
def check_complaint():
    if ADMIN:
        params = []
        with open('data/complaints.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                params.append(row)
        return render_template('complaints_for_admin.html', params=params, is_user=ADMIN)
    return redirect('/')


@app.route('/ok_complaint/<site>')
def ok_complaint(site):
    if ADMIN:
        ls = []
        with open('data/complaints.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                if row and row[0] != site:
                    ls.append(row)
        writer = csv.writer(open('data/complaints.csv', 'wt'))
        for row in ls:
            if row:
                writer.writerow(row)
        list_ = []
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "rt", encoding="utf8") as bad_site:
            list_ = list(map(str.strip, bad_site.readlines()))
            list_.remove(site)
        with open(f"{app.config['UPLOAD_FOLDER']}data/bad_sites.txt", "wt", encoding="utf8") as bad_site:
            for el in list_:
                bad_site.write(el + "\n")
        return redirect('/check_complaint')
    return redirect('/')


@app.route('/delete_complaint/<site>')
def delete_complaint(site):
    if ADMIN:
        ls = []
        with open('data/complaints.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                if row and row[0] != site:
                    ls.append(row)
        writer = csv.writer(open('data/complaints.csv', 'wt'))
        for row in ls:
            if row:
                writer.writerow(row)
        return redirect('/check_complaint')
    return redirect('/')


if __name__ == '__main__':
    app.run(host="127.0.0.2", port=5000)
