# -*- coding: utf-8 -*-

import sys
import unittest
import __builtin__ as shared

from os import path, remove
from mongoalchemy.session import Session

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
shared.session = Session.connect('database')


class TestDatabase(unittest.TestCase):

    def test_existence(self):
        from utils import database

    def test_import_satellites_from_tle(self):
        """Импортирует данные из файла в формате tle в базу данных."""
        from utils import database as db
        from objects.satellite import Satellite


        tle = [
            ('ISS (ZARYA)\n'
             '1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927\n'
             '2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537'),
            ('FALCON 9 R/B\n'
             '1 41381U 16013B   16087.98861961  .00001159  00000-0  17610-2 0  9991\n'
             '2 41381  27.9019 340.8136 7501703 189.9391 135.1696  1.97428959   459')
            ]

        with open('temp.txt', 'w') as f:
            f.write('\n'.join(tle) + '\n')

        db.drop()
        db.import_satellites_from_file('temp.txt')

        self.assertEqual(len(list(shared.session.query(Satellite))), 2)
        for i, sat in enumerate(shared.session.query(Satellite).ascending(Satellite.number)):
            self.assertEqual(tle[i], sat.to_tle())

        remove('temp.txt')

    def test_import_errors_from_xml(self):
        """Импортирует коды и тексты ошибок из XML файла."""
        from utils import database as db
        from objects.error import Error


        xml = (
            '<?xml version="1.0" encoding="UTF-8" ?>'
            '   <errors>'
            '       <error>'
            '           <code>1</code>'
            '           <msg>error_msg 1</msg>'
            '       </error>'
            '       <error>'
            '           <code>2</code>'
            '           <msg>error_msg 2</msg>'
            '       </error>'
            '   </errors>')

        with open('temp.xml', 'w') as f:
            f.write(xml)

        db.drop()
        db.import_errors_from_xml('temp.xml')

        template = ('{"error": '
                    '{"error_code": %d, '
                    '"error_msg": "error_msg %d"}}')

        self.assertEqual(len(list(shared.session.query(Error))), 2)
        for i, err in enumerate(shared.session.query(Error).ascending(Error.code)):
            self.assertEqual(template % (i+1, i+1), str(err))

        remove('temp.xml')


if __name__ == '__main__':
    unittest.main()
