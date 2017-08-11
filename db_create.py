# -*- coding: utf-8 -*-
#!/usr/bin/env python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
import os


db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO,
        api.version(SQLALCHEMY_MIGRATE_REPO)
    )