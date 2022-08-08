from flask import Flask, render_template, request
from report_monaco.report_monaco import build_report
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABBREVIATIONS = os.path.join(BASE_DIR, 'files/abbreviations.txt')
START_LOG = os.path.join(BASE_DIR, 'files/start.log')
END_LOG = os.path.join(BASE_DIR, 'files/end.log')

app = Flask(__name__)


@app.route('/')
@app.route('/report')
def report():
    results = list(build_report(ABBREVIATIONS, START_LOG, END_LOG))
    order = request.args.get('order')
    if order == "desc":
        results = sorted(results, key=lambda y: y['time'], reverse=True)
    return render_template('report.html', order=order, results=results)


@app.route('/report/drivers')
def drivers():
    order = request.args.get('order')
    driver_id = request.args.get('driver_id')
    results = list(build_report(ABBREVIATIONS, START_LOG, END_LOG))
    if order == "desc":
        results = sorted(results, key=lambda y: y['full_name'], reverse=True)
    else:
        results = sorted(results, key=lambda y: y['full_name'])

    driver = next((item for item in results if item["abr"] == driver_id), None)

    return render_template('drivers.html', order=order, driver_id=driver_id, results=results, driver=driver)