#!/usr/local/bin/python2.7
# --*--coding:utf8--*--

from application.avatar import VisteAvatar
from application.register import Register
from application.signin import Signin
from application.signout import Signout
from application.upload import Upload
from application.utility.app_runner import AppRunner
from application.utility.render_template import render_index


app = AppRunner(debug=False)
# app = AppRunner(debug=True)


@app.route("/")
def index():
    return render_index()


@app.route("/check_email")
def check_email():
    reg = Register()
    reg.check_email()


@app.route("/check_name")
def check_name():
    reg = Register()
    reg.check_name()


@app.route("/register")
def register():
    reg = Register()
    reg.register()


@app.route("/confirm")
def confirm_email():
    reg = Register()
    reg.confirm_email()


@app.route("/signin")
def signin():
    signin = Signin()
    signin.signin()


@app.route("/upload")
def upload():
    upload = Upload()
    upload.upload()


@app.route("/avatar")
def avatar():
    avatar = VisteAvatar()
    avatar.visit()


@app.route("/signout")
def signout():
    signout = Signout()
    signout.signout()


if __name__ == '__main__':
    app.dispatch_request()
