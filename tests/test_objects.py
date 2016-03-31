# -*- coding: utf-8 -*-

import sys
import unittest

from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestSatellite(unittest.TestCase):

    def test_existence(self):
        from objects.satellite import Satellite

    def test_to_tle(self):
        from objects.satellite import Satellite
        from datetime import datetime


        sat = Satellite(name='ISS (ZARYA)',
                        number=25544,
                        classification='U',
                        id_launch_year=98,
                        id_launch_number=67,
                        id_launch_piece='A',
                        epoch=datetime(2008, 9, 20, 12, 25, 40, 104192),
                        excentricity=0.0006703,
                        inclination=51.6416,
                        right_ascension=247.4627,
                        arg_perigee=130.536,
                        mean_anomaly=325.0288,
                        mean_motion=15.72125391,
                        mean_motion_derivative=-2.182e-05,
                        mean_motion_sec_derivative=0.0,
                        bstar=-1.1606e-05,
                        version=292,
                        revolutions=56353)

        tle = ('ISS (ZARYA)\n'
               '1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927\n'
               '2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537')

        self.assertEqual(sat.to_tle(), tle)

    def test_propagate(self):
        from objects.satellite import Satellite
        from datetime import datetime, timedelta


        sat = Satellite(name='ISS (ZARYA)',
                        number=25544,
                        classification='U',
                        id_launch_year=98,
                        id_launch_number=67,
                        id_launch_piece='A',
                        epoch=datetime(2008, 9, 20, 12, 25, 40, 104192),
                        excentricity=0.0006703,
                        inclination=51.6416,
                        right_ascension=247.4627,
                        arg_perigee=130.536,
                        mean_anomaly=325.0288,
                        mean_motion=15.72125391,
                        mean_motion_derivative=-2.182e-05,
                        mean_motion_sec_derivative=0.0,
                        bstar=-1.1606e-05,
                        version=292,
                        revolutions=56353)

        ts_locations = [
            (0, 4083648.051837333, -994393.038365178, 5243675.307422497),
            (20, 4132841.856021626, -848951.049648657, 5230638.006955366),
            (40, 4179871.056770562, -703064.1008434822, 5214852.974849476)
        ]

        self.assertEqual(sat.propagate(sat.epoch,
                                       sat.epoch + timedelta(seconds=60),
                                       20),
                         ts_locations);


if __name__ == '__main__':
    unittest.main()
