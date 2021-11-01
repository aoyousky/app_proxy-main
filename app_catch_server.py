# -*- coding: utf-8 -*-

from flask import Flask

from flask import request

import json

import install_catch

app = Flask(__name__)

'''
app catch web服务
'''


@app.route('/appCatch', methods=['POST'])
def handle_client():
    # request load request data
    data = json.loads(request.get_data())
    apkSerialNo = data['apkSerialNo'][0]
    apk_file_path = data["apkFilePath"][0]
    code = "0000"
    msg = "success"
    try:
        install_catch.main(apk_file_path)
    except Exception as e:
        print(e)
        code = "9999"
        msg = "failed"
    response = {"apkSerialNo": apkSerialNo, "code": code, "msg": msg}
    return str(json.dumps(response, sort_keys=True, indent=4))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
