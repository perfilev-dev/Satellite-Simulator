# -*- coding: utf-8 -*-

import __builtin__

from json import dumps
from flask import request
from mongoalchemy.session import Session
from objects.satellite import Satellite


@__builtin__.app.route("/method/satellites.get")
def satellites_get():
    """Возвращает расширенную информацию о спутниках."""

    session = Session.connect('database')

    satellite_ids = request.args.get('satellite_ids')
    fields = request.args.get('fields')

    response = []
    for satellite_id in [int(x.strip()) for x in satellite_ids.split(',') if x.strip().isdigit()]:
        sat = session.query(Satellite).filter(Satellite.number==satellite_id).first()
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