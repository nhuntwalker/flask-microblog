# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'tugboat')
