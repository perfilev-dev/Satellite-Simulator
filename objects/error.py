# -*- coding: utf-8 -*-

from json import dumps
from mongoalchemy.document import Document
from mongoalchemy.fields import *


class Error(Document):

    code = IntField(min_value=0)
    message = StringField(max_length=200)

    def __str__(self):
        return dumps({
            'error': {
                'error_code': self.code,
                'error_msg': self.message
            }
        })
