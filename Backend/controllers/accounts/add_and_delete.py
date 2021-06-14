import datetime
from uuid import uuid1
from threading import Thread
from flask import Blueprint, request, render_template
from flask_mail import Message

from common.email_sender import send_email
from common.global_value_manage import global_values
from common.authorization.jwt_management import *

account_add_delete = Blueprint("account_add_delete", __name__, url_prefix="/account")

@account_add_delete.post("/sign-in")
def sign_in():
    username = request.args.get("username")
    password = request.args.get("password")

    if username is None or password is None:
        return {
            "status": "request denied",
            "status_code": "REQDID",
            "reason": "cannot load payload",
            "reason_code": "PAYERR"
        }, 400

    entity = account(account.query.filter_by(username=username, password=password_process(password)).first())

    # 无法从数据库读取到目标用户
    if entity is None:
        return {
            "status": "sign in failed",
            "status_code": "FAILED",
            "reason": "wrong data",
            "reason_code": "WRODAT"
        }, 201

    # 登陆成功
    # 更新 AccessToken
    if not verify_access_token(entity.access_token, entity.uuid):

        # 需要更新
        summon_new_access_token(entity)

    # 返回 AccessToken 以及登陆成功
    return {
        "status": "sign in success",
        "information": entity.access_token,
        "status_code": "PASSED"
    }

@account_add_delete.post("/register")
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    email = request.args.get("email")
    email_code = request.args.get("email_code")

    if username is None or password is None or email is None:
        return {
            "status": "request denied",
            "status_code": "REQDID",
            "reason": "cannot load payload",
            "reason_code": "PAYERR"
        }, 400

    # 第一次请求
    if email_code is None:

        # 创建临时账户
        entity = account()
        entity.uuid = uuid1()
        entity.state = -1
        entity.permission = 0
        entity.email = email
        entity.username  = username
        entity.password = password_process(password)
        entity.create_date = datetime.datetime.now().date()
        entity.destroy_date = datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp() + 7200).date()

        # 提交至数据库
        global_values().get("database").session.add(entity)

        email_message = Message("SpeedCode access request code", sender="<CodeCraft Official> smartsheep.codecraft@outlook.com", recipients=[email])
        email_message.html = render_template("mail/register-email-code.html").replace("EMAIL_CODE", summon_new_access_token()).replace("USERNAME", username)
        Thread(target=send_email, args=[account_add_delete, email_message]).start()

        return {

        }