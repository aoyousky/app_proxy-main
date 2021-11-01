# -*- coding: utf-8 -*-


class Config:
    SQLALCHEMY_URL = 'mysql+mysqlconnector://cmft:aoyousky@localhost:{}/cmft_knowledge?charset=utf8mb4'
    POOL_RECYCLE= '500'
    MAX_OVERFLOW = '20'
    POOL_SIZE = '100'

