from peewee import *
from report_monaco.report_monaco import build_report
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABBREVIATIONS = os.path.join(BASE_DIR, 'files/abbreviations.txt')
START_LOG = os.path.join(BASE_DIR, 'files/start.log')
END_LOG = os.path.join(BASE_DIR, 'files/end.log')

db = SqliteDatabase('race_report.db')


class Driver(Model):
    id = PrimaryKeyField(unique=True)
    full_name = CharField()
    club_name = CharField()
    abbreviation = CharField()
    time = TimeField()

    class Meta:
        database = db
        order_by = 'time'
        db_table = 'drivers'


results = list(build_report(ABBREVIATIONS, START_LOG, END_LOG))

db.connect()
Driver.create_table()
for result in results:
    Driver.create(full_name=result['full_name'], club_name=result['club'], abbreviation=result['abr'],
                  time=result['time'])
db.close()