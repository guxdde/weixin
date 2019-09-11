# -*- coding: utf-8 -*-

from flask import request
from .. import app

@app.route('/', methods=['GET','POST'])
def wechat_verify():
    return request.args.get('echostr', '')



