# -*- coding: utf-8 -*-

from pyorbital import tlefile
from mongoalchemy.session import Session
from objects.satellite import Satellite


def import_satellites_from_file(path_to_file):
    """Импортирует данные из файла в формате tle в базу данных.

    @param: path_to_file Путь к файлу с tle наборами.

    """

    session = Session.connect('database')

    with open(path_to_file) as f:

        lines = f.read()[:-1].split('\n')
        tles = [lines[i:i+3] for i in range(0, len(lines),3)]

        for tle in tles:

            s = tlefile.read('', line1 = tle[1], line2 = tle[2])

            sat = Satellite(name=tle[0].strip(),
                            number=int(s.satnumber),
                            classification=s.classification,
                            id_launch_year=int(s.id_launch_year),
                            id_launch_number=int(s.id_launch_number),
                            id_launch_piece=s.id_launch_piece,
                            epoch=s.epoch,
                            excentricity=s.excentricity,
                            inclination=s.inclination,
                            right_ascension=s.right_ascension,
                            arg_perigee=s.arg_perigee,
                            mean_anomaly=s.mean_anomaly,
                            mean_motion=s.mean_motion,
                            mean_motion_derivative=s.mean_motion_derivative,
                            mean_motion_sec_derivative=s.mean_motion_sec_derivative,
                            bstar=s.bstar,
                            version=s.element_number,
                            revolutions=s.orbit)

            session.save(sat)

def drop():
    """Очищает базу данных."""

    session = Session.connect('database')

    session.clear_collection(Satellite)
