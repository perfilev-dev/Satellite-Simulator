# -*- coding: utf-8 -*-

import os
import sys
import __builtin__

from flask import Flask
__builtin__.app = Flask(__name__)


from methods.satellites import *
from utils import database as db


if __name__ == "__main__":

    # Заполним БД
    db.drop()
    db.import_satellites_from_file('/Users/s.perfilev/Downloads/tle-new.txt')

    app.run()
