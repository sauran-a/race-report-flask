from peewee import *


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

