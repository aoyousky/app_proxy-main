# -*- coding: utf-8 -*-

from model import AppInfo
from database import db_session


def fmt_data(data, cat_lev1, cat_lev2):
    base = data.get('base', {})
    app = AppInfo(
        crawl_platform='OPPO',
        app_name=base.get('appName', ''),
        app_package_name=base.get('pkgName', ''),
        dowload_link=base.get('url', ''),
        desc=base.get('desc', ''),
        size=base.get('size', ''),
        score=base.get('grade', ''),
        tags='|'.join([i.get('tagName', '') for i in data.get('appTags', [])]) if data.get('appTags', []) else '',
        level1_catagory=cat_lev1,
        level2_catagory=cat_lev2,
        origin_catagory=base.get('catName', ''),
        author=data.get('developer', {}).get('developer', ''),
        version=base.get('verName', ''),
        dowload_count=base.get('dlCount', '')
    )
    db_session.add(app)
    try:
        db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
