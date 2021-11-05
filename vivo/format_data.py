# -*- coding: utf-8 -*-

from model import AppInfo
from database import db_session

def fmt_data(base, data, cat_lev1, cat_lev2):
    app = AppInfo(
        crawl_platform = 'VIVO',
        app_name = base.get('title_zh',''),
        app_package_name = base.get('package_name', ''),
        dowload_link = base.get('download_url', ''),
        desc =  data.get('introduction',''),
        size =  base.get('size',''),
        score =  base.get('score',''),
        tags = '|'.join([i.get('tag','') for i in data.get('tags',[]) ]) if data.get('tags',[]) else '',
        level1_catagory = cat_lev1,
        level2_catagory = cat_lev2,
        origin_catagory = '',
        author =  base.get('developer',''),
        version =  base.get('version_name',''),
        upate_time = data.get('upload_time',''),
        dowload_count = base.get('download_count','')
    )
    db_session.add(app)
    try:
        db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()