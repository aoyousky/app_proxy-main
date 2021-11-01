# -*- coding: utf-8 -*-

from model import AppCatchInfo
from database import db_session
import json

def fmt_catch_info(app_info, domain_list):
    app_info = AppCatchInfo(
        app_name = app_info.get('app_name', ''),
        app_package_name = app_info.get('package_name', ''),
        version = app_info.get('version_name', ''),
        domains = json.dumps(domain_list, ensure_ascii=False),
        main_activity = app_info.get('app_activity', '')
    )
    db_session.add(app_info)
    db_session.commit()