# -*- coding: utf-8 -*-

import __builtin__ as shared

from json import dumps
from flask import request
from flask import Response
from objects.satellite import Satellite
from objects.error import Error
from dateutil import parser
from iso8601 import parse_date, ParseError


@shared.app.route("/method/satellites.get")
def satellites_get():
    """Возвращает список спутников."""

    offset = request.args.get('offset')
    count = request.args.get('count')

    err_100 = shared.session.query(Error).filter(Error.code == 100).first()

    if not offset is None:
        try:
            offset = int(offset)
            if offset < 0:
                return str(err_100) % 'offset should be positive or zero'
        except ValueError:
            return str(err_100) % 'offset not integer'
    else:
        offset = 0

    if not count is None:
        try:
            count = int(count)
            if count > 200:
                return str(err_100) % 'count should be less than 200'
            elif count < 1:
                return str(err_100) % 'count should be positive'
        except ValueError:
            return str(err_100) % 'offset not integer'
    else:
        count = 200

    response = {
        'count': shared.session.query(Satellite).count(),
        'items': []
    }
    for sat in list(shared.session.query(Satellite).skip(offset).limit(count)):
        response['items'].append({
            'id': sat.number,
            'name': sat.name
            });

    return Response(response=dumps({'response': response}),
                    status=200,
                    mimetype="application/json")


@shared.app.route("/method/satellites.getDetail")
def satellites_getDetail():
    """Возвращает расширенную информацию о спутниках."""

    satellite_ids = request.args.get('satellite_ids')
    fields = request.args.get('fields')

    err_100 = shared.session.query(Error).filter(Error.code == 100).first()
    err_113 = shared.session.query(Error).filter(Error.code == 113).first()

    if satellite_ids is None:
        return str(err_100) % 'satellite_ids is undefined'
    elif not len([x for x in satellite_ids.split(',') if x.strip().isdigit()]):
        return str(err_113)

    response = []
    for satellite_id in [int(x.strip()) for x in satellite_ids.split(',') if x.strip().isdigit()]:
        sat = shared.session.query(Satellite).filter(Satellite.number==satellite_id).first()
        if not sat is None:
            response.append({
                'id': satellite_id,
                'name': sat.name
                });
            if not fields is None:
                for field in [x.strip() for x in fields.split(',')]:
                    if field in sat.schema_json()['fields'].keys():
                        response[-1][field] = getattr(sat, field)

    return Response(response=dumps({'response': response}),
                    status=200,
                    mimetype="application/json")


@shared.app.route("/method/satellites.getOrbit")
def satellites_getOrbit():
    """Возвращает рассчитанную траекторию для указанных спутников в виде массива
    [ts1, x1, y1, z1, ts2, x2, ...], где ts — время в секундах относительно
    date_from, а x,y,z — декартовы координаты объектов.
    """

    satellite_ids = request.args.get('satellite_ids')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sample = request.args.get('sample')

    err_100 = shared.session.query(Error).filter(Error.code == 100).first()
    err_101 = shared.session.query(Error).filter(Error.code == 101).first()
    err_113 = shared.session.query(Error).filter(Error.code == 113).first()

    if satellite_ids is None:
        return str(err_100) % 'satellite_ids is undefined'
    elif not len([x for x in satellite_ids.split(',') if x.strip().isdigit()]):
        return str(err_113)

    if not sample is None:
        try:
            sample = int(sample)
            if sample < 1:
                return str(err_100) % 'sample should be positive'
        except ValueError:
            return str(err_100) % 'sample not integer'
    else:
        sample = 300

    if date_from is None:
        return str(err_100) % 'date_from is undefined'
    else:
        try:
            date_from = parse_date(date_from).replace(tzinfo=None)
        except ParseError:
            return str(err_100) % 'date_from is not ISO 8601-compliant'

    if date_to is None:
        return str(err_100) % 'date_to is undefined'
    else:
        try:
            date_to = parse_date(date_to).replace(tzinfo=None)
        except ParseError:
            return str(err_100) % 'date_to is not ISO 8601-compliant'

    if date_from > date_to:
        return str(err_101) % 'date_from comes after date_to'

    response = []
    for satellite_id in [int(x.strip()) for x in satellite_ids.split(',') if x.strip().isdigit()]:
        sat = shared.session.query(Satellite).filter(Satellite.number==satellite_id).first()
        if not sat is None:
            response.append({
                'id': satellite_id,
                'name': sat.name,
                'position': sum([list(x) for x in sat.propagate(date_from, date_to, sample)],[])
            })

    return Response(response=dumps({'response': response}),
                    status=200,
                    mimetype="application/json")


@shared.app.route("/method/satellites.getCZML") # deprecated
def satellites_getCZML():
    """Возвращает рассчитанную траекторию для указанных спутников в json-формате Cesium."""

    satellite_ids = request.args.get('satellite_ids')
    epoch = request.args.get('epoch')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sample = request.args.get('sample')

    try:
        epoch = parser.parse(epoch).replace(tzinfo=None)
        date_from = parser.parse(date_from).replace(tzinfo=None)
        date_to = parser.parse(date_to).replace(tzinfo=None)
        sample = int(sample) if not sample is None else 300

        response = [{
            'id': 'document',
            'name': 'Simple CZML',
            'version': '1.0'
            }]

        for satellite_id in [int(x.strip()) for x in satellite_ids.split(',') if x.strip().isdigit()]:
            sat = shared.session.query(Satellite).filter(Satellite.number==satellite_id).first()
            if not sat is None:
                response.append({
                    'id': 'Satellite/%s' % sat.name,
                    'name': sat.name,
                    'availability': '%sZ/%sZ' % (epoch.isoformat(),
                                                 date_to.isoformat()),
                    'path': {
                        'show': '%sZ/%sZ' % (epoch.isoformat(),
                                             date_to.isoformat()),
                        'width': 1,
                        'material': {
                            'solidColor': {
                                'color': {
                                    'rgba': [255, 255, 0, 255]
                                }
                            }
                        },
                        'resolution': 120,
                        'leadTime': [{
                            'number': 24 * 60 * 60 / sat.mean_motion
                            }],
                        'trailTime': [{
                            'number': 24 * 60 * 60 / sat.mean_motion
                            }]
                    },
                    'position': {
                        'epoch': '%sZ' % date_from.isoformat(),
                        'interpolationAlgorithm': 'LAGRANGE',
                        'interpolationDegree': 7,
                        'referenceFrame': 'INERTIAL',
                        'cartesian': sum([list(x) for x in sat.propagate(date_from, date_to, sample)],[])
                    },
                    'label': {
                        'fillColor': {
                            'rgba': [255, 255, 0, 255]
                        },
                        'font': '11pt Lucida Console',
                        'horizontalOrigin': 'LEFT',
                        'outlineColor': {
                            'rgba': [0, 0, 0, 255]
                        },
                        'outlineWidth': 2,
                        'pixelOffset': {
                            'cartesian2': [20, -4]
                        },
                        'show': 'true',
                        'style': 'FILL_AND_OUTLINE',
                        'text': sat.name,
                        'verticalOrigin': 'CENTER'
                    }
                })
        return Response(response=dumps({'response': response}),
                    status=200,
                    mimetype="application/json")
    except:
        return '[]'
