# -*- coding: utf-8 -*-

import __builtin__ as shared

from pyorbital import tlefile
from objects.satellite import Satellite
from objects.error import Error
from xml.etree import ElementTree


def import_satellites_from_file(path_to_file):
    """Импортирует данные из файла в формате tle в базу данных.

    @param: path_to_file Путь к файлу с tle наборами.

    """

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

            shared.session.save(sat)

def import_errors_from_xml(path_to_file):
    """Импортирует коды и тексты ошибок из XML файла.

    @param: path_to_file Путь к XML файлу.

    """

    root = ElementTree.parse(path_to_file).getroot()

    for error in root.findall('error'):

        err = Error(code=int(error.find('code').text),
                    message=error.find('msg').text)

        shared.session.save(err)

def drop():
    """Очищает базу данных."""

    shared.session.clear_collection(Satellite)
    shared.session.clear_collection(Error)
