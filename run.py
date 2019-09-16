# -*- coding: utf-8 -*-
#/usr/lib/env python

from main import app
from main.utils.config import config

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

