from flask_restful import Resource
import simplexml
from flask import request, jsonify, make_response
from modules import *


class RaceReport(Resource):
    def get(self, version):
        """
        Get results of Monaco 2018 Racing. By default, results are in json format and sorted from best to worst result
        ---
        parameters:
          - in: path
            name: version
            type: string
            required: true
        responses:
          200:
            description: REST API report of Monaco 2018 Racing
            schema:
              id: RaceReport
              properties:
                version:
                  type: string
                  description: version of the API
                  default: v1
        """

        # Collecting URL parameters
        report_format = request.args.get('format')
        report_order = request.args.get('order')

        # Connecting to database
        with db:
            results = list(Driver.select().dicts())

        # Converting 'time' parameter of each driver from datetime.time to string
        for result in results:
            result['time'] = result['time'].strftime("%M:%S.%f")

        if report_order == 'desc':
            results = sorted(results, key=lambda y: y['time'], reverse=True)
        if report_format == 'json' or report_format is None:
            return jsonify(results)
        elif report_format == 'xml':
            results = dict(results=results)
            results = simplexml.dumps(results)
            response = make_response(results)
            response.headers['content-type'] = 'application/xml'
            return response


class DriversReport(Resource):
    def get(self, version):
        """
        Get a list of drivers from Monaco 2018 Racing. By default, results are in json format and sorted alphabetical
        ---
        parameters:
          - in: path
            name: version
            type: string
            required: true
        responses:
          200:
            description: All good
            schema:
              id: DriversReport
              properties:
                version:
                  type: string
                  description: version of the API
                  default: v1
        """

        # Collecting URL parameters
        report_format = request.args.get('format')
        report_order = request.args.get('order')
        driver_id = request.args.get('driver_id')

        # Connecting to database
        with db:
            results = list(Driver.select().dicts())

        # Converting 'time' parameter of each driver from datetime.time to string.
        # datetime.time format is not serializable for json
        for result in results:
            result['time'] = result['time'].strftime("%M:%S.%f")

        drivers_report = list()
        for item in results:
            i = {key: item[key] for key in item.keys() & {'abbreviation', 'full_name', 'club_name'}}
            drivers_report.append(i)

        if report_order == 'desc':
            drivers_report = sorted(drivers_report, key=lambda y: y['full_name'], reverse=True)
        else:
            drivers_report = sorted(drivers_report, key=lambda y: y['full_name'])

        driver = next((item for item in results if item['abbreviation'] == driver_id), {'Error': 'No such driver'})

        if report_format == 'json' or report_format is None:
            if driver_id is not None:
                return jsonify(driver)
            else:
                return jsonify(drivers_report)
        elif report_format == 'xml':
            if driver_id is not None:
                driver = dict(driver=driver)
                driver = simplexml.dumps(driver)
                response = make_response(driver)
            else:
                drivers_report = dict(drivers_report=drivers_report)
                drivers_report = simplexml.dumps(drivers_report)
                response = make_response(drivers_report)

            response.headers['content-type'] = 'application/xml'
            return response
