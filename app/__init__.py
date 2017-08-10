# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import Flask


app = Flask(__name__)
from app import views
