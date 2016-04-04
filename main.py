# -*- coding: utf-8 -*-

import os
import sys
import __builtin__ as shared

from flask import Flask
from mongoalchemy.session import Session
shared.app = Flask(__name__)
shared.session = Session.connect('database')


from methods.satellites import *
from utils import database as db


if __name__ == "__main__":

    # Заполним БД
    db.drop()
    db.import_satellites_from_file('./tle-new.txt')

    app.run()
