# -*- coding: utf-8 -*-

from flask import Flask

from flask import request

import json

import install_catch

from oppo.uilts import download_save_apk
from oppo.crawler import oppo_start
from vivo.crawler import vivo_start
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)

executor = ThreadPoolExecutor(2)


@app.route('/appCatch', methods=['POST'])
def handle_client():
    """
        app catch host
    """
    # request load request data
    data = json.loads(request.get_data())
    apkSerialNo = data['apkSerialNo'][0]
    apk_file_path = data["apkFilePath"][0]
    app_level_category = data['appCategory'][0]
    code = "0000"
    msg = "success"
    catch_result = ''
    try:
        catch_result = install_catch.main(apk_file_path, app_level_category)
    except Exception as e:
        print(e)
        code = "9999"
        msg = "failed"
    response = {"apkSerialNo": apkSerialNo, "code": code, "msg": msg, "catch_result": catch_result}
    return str(json.dumps(response, sort_keys=True, indent=4))


@app.route('/oppoAppSpiderByCategory', methods=['POST'])
def oppoAppSpiderByCategory():
    """
    oppo app-store spider via app_category
    """
    data = json.loads(request.get_data())
    app_category_name = data['app_category_name'][0]
    # async execute oppo_start method
    executor.submit(oppo_start, [app_category_name])
    response = {"code": "0000", "msg": "oppo spider"}
    return str(json.dumps(response, sort_keys=True, indent=4))


@app.route('/vivoAppSpiderByCategory', methods=['POST'])
def vivoAppSpiderByCategory():
    """
    vivo app-store spider via app_category
    """
    data = json.loads(request.get_data())
    app_category_name = data['app_category_name'][0]
    # async execute vivo_start method
    executor.submit(vivo_start, [app_category_name])
    response = {"code": "0000", "msg": "vivo spider"}
    return str(json.dumps(response, sort_keys=True, indent=4))


@app.route('/oppoAppDownload', methods=['POST'])
def oppo_app_download():
    """
    oppo app download
    """
    data = json.loads(request.get_data())
    download_path = data['download_path'][0]
    download_url = data['download_url'][0]
    file_name = download_save_apk(download_path, download_url)
    code = "0000"
    msg = "success"
    if not file_name:
        code = "9999"
        msg = "failed"
    response = {"code": code, "msg": msg}
    return str(json.dumps(response, sort_keys=True, indent=4))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
