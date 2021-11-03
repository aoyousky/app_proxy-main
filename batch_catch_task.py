# -*- coding: utf-8 -*-

import os
import sys

import install_catch


def batch_catch(file_path, app_category):
    files = os.listdir(file_path)

    for file in files:
        if not os.path.isdir(file):
            currentFileName = os.path.basename(file)
            apkPath = file_path + "/" + currentFileName
            try:
                install_catch.main(apkPath, app_category)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    file_dir = sys.argv[1]
    app_category = sys.argv[2]
    batch_catch(file_dir, app_category)
