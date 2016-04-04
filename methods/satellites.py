# -*- coding: utf-8 -*-

import __builtin__ as shared

from json import dumps
from flask import request
from objects.satellite import Satellite
from dateutil import parser


@shared.app.route("/method/satellites.get")
def satellites_get():
    """Возвращает список спутников."""

    response = []
    for sat in list(shared.session.query(Satellite)):
        response.append({
            'id': sat.number,
            'name': sat.name
            });

    return dumps({'response': response})

@shared.app.route("/method/satellites.getDetail")
def satellites_getDetail():
    """Возвращает расширенную информацию о спутниках."""

    satellite_ids = request.args.get('satellite_ids')
    fields = request.args.get('fields')

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

    return dumps({'response': response})

@shared.app.route("/method/satellites.getOrbit")
def satellites_getOrbit():
    """Возвращает рассчитанную траекторию для указанных спутников в json-формате Cesium."""

    satellite_ids = request.args.get('satellite_ids')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sample = request.args.get('sample')

    try:
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
                    'availability': '%sZ/%sZ' % (sat.epoch.isoformat(),
                                                 date_to.isoformat()),
                    'path': {
                        'show': '%sZ/%sZ' % (sat.epoch.isoformat(),
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
                            'number': 3600
                            }],
                        'trailTime': [{
                            'number': 3600
                            }]
                    },
                    'position': {
                        'epoch': '%sZ' % sat.epoch.isoformat(),
                        'interpolationAlgorithm': 'LAGRANGE',
                        'interpolationDegree': 7,
                        'referenceFrame': 'INERTIAL',
                        'cartesian': sat.propagate(date_from, date_to, sample)
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
        return dumps({'response': response})
    except:
        return '[]'
