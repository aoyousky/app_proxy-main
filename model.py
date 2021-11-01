# -*- coding: utf-8 -*-



from database import engine
from sqlalchemy import Column, INTEGER, String, VARCHAR, DateTime, TEXT, BIGINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AppInfo(Base):
    """
    AppInfo
    """
    __tablename__ = "app_info"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    app_name = Column(String(500), comment='app_name')
    app_package_name = Column(String(500), comment='app_package_name')
    dowload_link = Column(String(1000), comment='dowload_link')
    desc = Column(TEXT, comment='desc')
    size = Column(String(20), comment='size')
    score = Column(String(20), comment='评分')
    tags = Column(String(200), comment='标签')
    level1_catagory = Column(String(200), comment='一级分类')
    level2_catagory = Column(String(200), comment='二级分类')
    origin_catagory = Column(String(200), comment='原始分类')
    author = Column(String(200), comment='作者')
    crawl_platform = Column(String(50), comment='crawl_platform')
    version = Column(String(50), comment='version')
    upate_time = Column(String(50), comment='更新日期')
    dowload_count = Column(String(50), comment='安装次数')

class AppCatchInfo(Base):
    """
    AppInfo
    """
    __tablename__ = "app_catch_info"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    app_name = Column(String(500), comment='app_name')
    app_package_name = Column(String(500), comment='app_package_name')
    version = Column(String(50), comment='version')
    domains = Column(TEXT, comment='domains')
    main_activity = Column(String(500), comment='main_activity')
    app_level_category = Column(String(64), comment='app_level_category')

Base.metadata.create_all(engine)