# -*- coding: utf-8 -*-


import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from config import Config


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

engine = create_engine(
    Config.SQLALCHEMY_URL.format('3306'),
    pool_size=int(Config.POOL_SIZE),
    max_overflow=int(Config.MAX_OVERFLOW),
    pool_recycle=int(Config.POOL_RECYCLE),
    poolclass=QueuePool,
    pool_pre_ping=True,
)

Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)