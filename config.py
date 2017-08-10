# -*- coding: utf-8 -*-
#!/usr/bin/python
import os


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'tugboat')
