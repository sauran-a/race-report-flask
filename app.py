from flask import Flask, request, render_template
from flask_restful import Api
from flasgger import Swagger
from api import RaceReport, DriversReport
from modules import *


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
api = Api(app)
swagger = Swagger(app)


def get_results():
    with db:
        results = list(Driver.select().dicts())
    for result in results:
        result['time'] = result['time'].strftime("%M:%S.%f")
    return results


@app.route('/')
@app.route('/report')
def report():
    # Prepare data for views
    results = get_results()
    order = request.args.get('order')
    if order == "desc":
        results = sorted(results, key=lambda y: y['time'], reverse=True)
    return render_template('report.html', order=order, results=results)


@app.route('/report/drivers')
def drivers():
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')
    results = get_results()
    if order == "desc":
        results = sorted(results, key=lambda y: y['full_name'], reverse=True)
    else:
        results = sorted(results, key=lambda y: y['full_name'])

    driver = next((item for item in results if item['abbreviation'] == driver_id), None)

    return render_template('drivers.html', order=order, driver_id=driver_id, results=results, driver=driver)


api.add_resource(RaceReport, '/api/<string:version>/report/')
api.add_resource(DriversReport, '/api/<string:version>/report/drivers')


if __name__ == '__main__':
    app.run(debug=True)