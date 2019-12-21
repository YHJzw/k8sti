from flask import Flask, request, render_template, redirect, make_response, session, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import pymysql

builder_url = "http://112.150.189.246:8080"
k8s_url = "http://34.97.171.66"

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'Distribute!Computing!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://WEB:k8sti@localhost/k8sti'  # user: WEB pw: k8sti db: k8sti
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(16), unique=True, nullable=False)
    pw = db.Column(db.String(128), nullable=False)

    project = db.relationship('Project', backref='manager')

    def __init__(self, uname, pw):
        self.uname = uname
        self.pw_hash(pw)

    def pw_hash(self, pw):
        self.pw = generate_password_hash(pw)


class Project(db.Model):
    __tablename__ = 'project'

    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    url = db.Column(db.Text, nullable=False)
    branch = db.Column(db.Text, nullable=True)
    token = db.Column(db.Text, nullable=True)
    k8s_url = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = ""

    def __init__(self, title, url, branch, token, k8s_url, uid):
        self.title = title
        self.url = url
        self.branch = branch
        self.token = token
        self.k8s_url = k8s_url
        self.uid = uid


# Main Page
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        if request.method == 'POST': # Build Service로 프로젝트 정보 전송
            title = request.form['title']
            url = request.form['url']
            branch = request.form['branch']
            token = request.form['token']

            if len(title) == 0 or len(url) == 0 or len(branch) == 0:
                return render_template('home.html', result="Input all information")

            uname = request.cookies.get('uname')
            data = User.query.filter_by(uname=uname).first()
            u_data = data.__dict__
            uid = u_data['id']

            data = Project.query.filter_by(title=title).first()
            # 중복 타이틀 방지

            if data is not None:
                return render_template('home.html', result="There is same titled project")

            project = {"title": title, "url": url, "branch": branch, "token": token}

            json_data = json.dumps(project, sort_keys=True, indent=4)  # Dict to JSON

            resp = requests.post(url=f"{builder_url}/repo", data=json_data, timeout=300)
            # Build Service 서버로 프로젝트 정보 JSON 전달
 
            status = resp.status_code

            if status < 400:  # http status 400 이상은 오류
                result = resp.json()
                res = result['result']  # 빌드 및 컨테이너 등록 결과

                # res = 성공 시 build Start / 실패 시 res에 failed 저장
                if res != 'failed':
                    new_p = Project(title, url, branch, token, "k8s_url", uid)
                    db.session.add(new_p)
                    db.session.commit()
                    # 프로젝트 등록

                return render_template('home.html', result=res)  # URL 출력

            else:
                return render_template('home.html', result="Error: {}".format(status))

        return render_template('home.html', result="None")


# Project List
@app.route('/projects', methods=['GET', 'POST'])
def plist():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        uname = request.cookies.get('uname')

        data = User.query.filter_by(uname=uname).first()
        u_data = data.__dict__

        data = Project.query.filter_by(uid=u_data['id']).all()

        for project in data:
            resp = requests.get(url=f"{builder_url}/repo/{project.title}", timeout=120)
            result = resp.json()

            project.status = result.get('status', "")
            project.k8s_url = result.get('url', "")
        db.session.commit()

        if request.method == 'POST':  # K8S에 삭제 요청 전송
            pid = request.form.getlist('project')

            if not pid:
                return render_template('plist.html', result="Select the Project", projects=data)

            remove = Project.query.filter_by(pid=pid[0]).first()
            p_data = remove.__dict__

            p_info = {"project_name": p_data['title']} # Dict to JSON
            resp = requests.post(url=f"{k8s_url}/delete", json=p_info, timeout=300)
            # K8S API로 삭제할 프로젝트 정보 JSON 전달

            status = resp.status_code

            if status < 400:  # http status 400 이상은 오류
                result = resp.json()
                res = result['status']

                if res != 'failed':  # status 성공시 proceeded, 실패시 failed
                    db.session.delete(remove)
                    db.session.commit()
                    # 프로젝트 삭제

                return render_template('plist.html', result=res, projects=data)  # URL 출력

            else:
                return render_template('plist.html', result="Error: {}".format(status), projects=data)

        return render_template('plist.html', result="None", projects=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['pw']

        try:
            data = User.query.filter_by(uname=uname).first()

            if data is not None:  # 사용자 있으면
                p_data = data.__dict__
                pw = check_password_hash(p_data['pw'], password)

                if pw:  # 암호 True
                    session['logged_in'] = uname

                    resp = make_response(redirect(url_for('home')))
                    resp.set_cookie('uname', uname)

                    return resp
                else:
                    return render_template('login.html', message="Wrong Password!")
            else:
                return render_template('login.html', message="User not exist!")

        except Exception as e:
            print(e)
            return render_template('login.html', message="Error has occurred")

    return render_template('login.html')


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        uname = request.form['uname']
        pw = request.form['pw']

        if len(uname) == 0:
            return render_template('join.html', message="Input ID!")
        elif len(pw) == 0:
            return render_template('join.html', message="Input PW!")

        try:
            data = User.query.filter_by(uname=uname).first()

            if data is None:  # 사용자 없음
                new_u = User(uname, pw)
                db.session.add(new_u)
                db.session.commit()

                return render_template('login.html', message="You can now login")

            else:
                return render_template('join.html', message="User Already Exists!")

        except Exception as e:
            return render_template('join.html', message="Error has occurred")

    return render_template('join.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('uname', request.cookies.get('uname'), max_age=0)

    return resp


if __name__ == '__main__':
    db.create_all()
    builder_url = input("Build Service IP: ")
    k8s_url = input("Server IP: ")

    app.run(debug=True, host='0.0.0.0', port=8080)

''' # add user
    user = User('admin', 'admin')
    db.session.add(user)
    db.session.commit() '''
