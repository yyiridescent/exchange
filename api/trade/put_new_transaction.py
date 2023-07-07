import base64

from flask import session

from utils import login_required
from ..trade import bp

from flask import request
import os
from data_sheet import session,User, Transaction
from utils.tool import get_age


@bp.route("/put_new_transaction",methods=["POST"])
@login_required
def put_new_transaction():
    user_id= request.json.get("uid")
    price = request.json.get("price")
    channel = request.json.get("channel")
    login_method = request.json.get("login_method")
    message = request.json.get("message")
    system = request.json.get("system")
    addiction = request.json.get("addiction")
    photolist  =request.json.get("photolist")
    user = session.query(User).filter(User.id == user_id).first()
    birthday  = user.birthday
    if birthday is None:
        return {"code":401,"message":"您未完成实名认证"}
    age = get_age(birthday)
    if age < 18:
        return {"code": 402, "message": "您未成年，不可进行交易"}
    save_path = r"E:\trade\account"
    if not os.path.exists(save_path):  # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    try:
        newTransaction = Transaction(price = price,addiction = addiction,channel = channel,login_method = login_method,seller = user_id,system = system,approved = False)
        session.add(newTransaction)
        session.commit()
        tradtionId = session.query(Transaction).first().id
        f = open(save_path ++ '\\' + str(tradtionId) + '\\' + str(tradtionId) + ".txt", 'w')
        f.write(message)
        i = 1
        for photo in photolist:
            imgdata = base64.b64decode(photo)
            # 将图片保存为文件
            with open(save_path ++ '\\' + str(tradtionId) + '\\' + str(i) + ".png", 'wb') as f:
                f.write(photo)
            i += 1
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息储存失败，请稍后再试"}
    return {"code":200,"message":"success"}

