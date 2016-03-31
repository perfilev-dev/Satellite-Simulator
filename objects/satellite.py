# -*- coding: utf-8 -*-

from mongoalchemy.document import Document
from mongoalchemy.fields import *
from datetime import datetime
from math import copysign


class Satellite(Document):

    name = StringField(max_length=24)

    number = IntField(min_value=0)
    classification = EnumField(StringField(), 'S', 'C', 'U')

    # International Designator
    id_launch_year = IntField(min_value=0, max_value=99)
    id_launch_number = IntField(min_value=0, max_value=999)
    id_launch_piece = StringField(max_length=3)

    epoch = DateTimeField(min_date=datetime(1957,10,4,19,28,34))

    # Orbital elements
    excentricity = FloatField(min_value=0)
    inclination = FloatField(min_value=0, max_value=180)
    right_ascension = FloatField(min_value=0, max_value=360)
    arg_perigee = FloatField(min_value=0, max_value=360)
    mean_anomaly = FloatField(min_value=0, max_value=360)

    mean_motion = FloatField(min_value=0)
    mean_motion_derivative = FloatField()
    mean_motion_sec_derivative = FloatField()

    # Other fields
    bstar = FloatField()
    version = IntField(min_value=0, max_value=9999)
    revolutions = IntField(min_value=0)

    def to_tle(self):
        '''Представляет данные об орбите в двухстрочном формате'''

        title = self.name
        line1 = ' '.join([
            '1',
            '%5d%s' % (self.number, self.classification),
            '%02d%03d%s' % (self.id_launch_year, self.id_launch_number,
                            self.id_launch_piece.ljust(3)),
            '%02d%012.8f'% (self.epoch.year % 100,
                            (self.epoch-datetime(self.epoch.year,1,1)).total_seconds()/86400+1),
            '%10s' % ('%.8f'%self.mean_motion_derivative).replace('0.', '.'),
            ' %s-%d'%(('%.4e'%self.mean_motion_sec_derivative).replace('.','')[:5],
                      int(('%.e'%self.mean_motion_sec_derivative)[-1]) -
                      (0 if ('%.e'%self.mean_motion_sec_derivative)[0] == '0' else 1)),
            '%s%s%s%d' % ('-' if copysign(1, self.bstar) < 0 else ' ',
                          ('%.4e' % self.bstar).replace('.','').replace('-','')[:5],
                          ('%.4e' % self.bstar)[-3],
                          abs(int(('%.e'%self.bstar)[-1]) +
                              copysign(1, int(('%.e'%self.bstar)[-3:])) * (1 if ('%.e'%self.bstar)[:2].replace('e','')[-1] != '0' else 0))),
            '0',
            '%4d' % self.version
        ])
        line2 = ' '.join([
            '2',
            '%5d' % self.number,
            '%8.4f' % self.inclination,
            '%8.4f' % self.right_ascension,
            ('%.7f' % self.excentricity)[2:],
            '%8.4f' % self.arg_perigee,
            '%8.4f' % self.mean_anomaly,
            '%11.8f%5d' % (self.mean_motion, self.revolutions)
        ])

        line1 += str(sum([int(x) for x in list(line1.replace('-','1')) if x.isdigit()]) % 10)
        line2 += str(sum([int(x) for x in list(line2.replace('-','1')) if x.isdigit()]) % 10)

        return '\n'.join([title, line1, line2])
