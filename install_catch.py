# -*- coding: utf-8 -*-
import json

from format_data import fmt_catch_info
import subprocess
import os
import platform
import time
import stat
import aapt
import sys
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(os.path.split(curPath)[0])[0]
sys.path.append(rootPath)


class Catch():

    def __init__(self, apk_info, apk_path):
        system_name = platform.system()
        if (system_name != 'Darwin' and system_name !=
                'Linux' and system_name != 'Windows'):
            raise TypeError(
                'unknown system type, only support Darwin、Linux、Windows')
        self.adb_path = os.path.join(os.getcwd(), 'bin', system_name, 'adb')
        if system_name == 'Windows':
            self.adb_path += '.exe'
        if (system_name != 'Windows' and os.access(
                self.adb_path, os.X_OK) is not True):
            os.chmod(self.adb_path, stat.S_IRWXU)

        self.package_name = apk_info['package_name']
        self.main_activity = apk_info['app_activity']
        self.apk_path = apk_path

    def restart_adb(self):
        cmd_line = self.adb_path + ' kill-server'
        out = self.cmd_excute(cmd_line)
        return out

    def open_app(self, main_activity):

        cmd_line = self.adb_path + ' shell am start {}'.format(main_activity)
        out = self.cmd_excute(cmd_line)
        return out

    def stop_kill_app(self):
        cmd_line = self.adb_path + ' shell am force-stop ' + self.package_name
        self.cmd_excute(cmd_line)
        cmd_line = self.adb_path + ' shell am kill ' + self.package_name
        self.cmd_excute(cmd_line)

    def install_app(self):
        cmd_line = self.adb_path + ' install ' + self.apk_path
        out = self.cmd_excute(cmd_line)
        return out

    def uninstall_app(self):
        cmd_line = self.adb_path + ' uninstall ' + self.package_name
        self.cmd_excute(cmd_line)

    def get_all_activity(self):
        cmd_line = self.adb_path + \
            ' shell dumpsys package | grep -i {}|grep Activity'.format(
                self.package_name)
        print(cmd_line)
        all_activity = self.cmd_excute(cmd_line)
        return all_activity

    def cmd_excute(self, cmd_line):
        try:
            result = subprocess.Popen(cmd_line, shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      )
        except FileNotFoundError as e:
            print(e)
            return 'excute error'
        # print(result.stdout.read().decode())
        print(result.stderr.read())
        return result.stdout.read().decode()


def main(apk_path, apk_category='', dump_sql=True):
    apk_info = aapt.get_apk_info(apk_path)
    apk_info['app_level_category'] = apk_category
    catch = Catch(apk_info, apk_path)

    print('安装app ing。。。')
    catch.restart_adb()
    install_result = catch.install_app()
    print(install_result)
    if 'error' in install_result:
        return {
            'code': '0000',
            'msg': '安装失败!'
        }
    print('安装完成。。。')
    time.sleep(5)
    print('启动app ing。。。')
    # 启动抓包
    kill_out = subprocess.getoutput('sh ' + os.getcwd() + '/clear_mitm.sh')
    print(kill_out)
    rm_out = subprocess.getoutput('rm -rf ' + os.getcwd() + '/request')
    print(rm_out)
    mitm_path = os.path.join(os.getcwd(), 'mitm_script.py')
    cmd_line = 'mitmdump -s ' + mitm_path
    proxy_th = subprocess.Popen(cmd_line.split(' '))

    if not apk_info['app_activity']:
        all_activity = catch.get_all_activity()
        print(all_activity)
        for i in (all_activity.split('\n')):
            print(i.strip().split(' '))
            try:
                main_activity = i.strip().split(' ')[1]
            except Exception as e:
                print(e)
                continue
            catch.open_app(main_activity)
    else:
        catch.open_app(
            apk_info['package_name'] +
            '/' +
            apk_info['app_activity'])
    print('启动完成！')

    time.sleep(40)
    # 抓包
    proxy_th.kill()
    print('关闭app ing。。')
    catch.stop_kill_app()
    print('卸载app')
    catch.uninstall_app()
    print('卸载完成')
    domain_list = subprocess.getoutput('cat ' + os.getcwd() + '/request')
    print('输出结果：', domain_list)
    if dump_sql:
        fmt_catch_info(apk_info, domain_list)
    return {
        'code': '0000',
        'msg': '成功',
        'appName': apk_info.get('app_name', ''),
        'appVersion': apk_info.get('version_name', ''),
        'appPackageName': apk_info.get('package_name', ''),
        'domains': json.dumps(domain_list, ensure_ascii=False)
    }
    # rm_result = subprocess.getoutput('rm -rf ' + os.getcwd() + '/request')
    # print(rm_result)


if __name__ == '__main__':
    apk_path = sys.argv[1]
    apk_level_category = sys.argv[2]
    main(apk_path, apk_level_category)