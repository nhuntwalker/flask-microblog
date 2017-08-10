# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'tugboat')

DATABASE_USER = os.environ.get('DATABASE_USER', '')
DATABASE_PASS = os.environ.get('DATABASE_PASS', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'microblog')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')

SQLALCHEMY_DATABASE_URI = 'postgresql://'
if DATABASE_USER:
    SQLALCHEMY_DATABASE_URI += f'{DATABASE_USER}'

    if DATABASE_PASS:
        SQLALCHEMY_DATABASE_URI += f':{DATABASE_PASS}'
    SQLALCHEMY_DATABASE_URI += f'@'
SQLALCHEMY_DATABASE_URI += f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
