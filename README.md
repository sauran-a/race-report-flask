# Flask Race Report

Web app to display Monaco Race report. All data on racers was transferred to an SQLite database from files.

Stack: Flask, HTML&CSS, Peewee (ORM), REST API, Swagger


## Usage

### Web-view 

Start the app with `python app.py` command in a terminal. Go to http://127.0.0.1:5000 with your browser to view race results. 

Other options:
* `?order=desc` - Display race results in descending order
* `/report/drivers` - Display information about drivers, their clubs and abbreviations, sorted by drivers' name
* `/report/drivers?driver_id=SVF` - Display information about particular driver

### API

The app supports API requests. requesting `http://127.0.0.1:5000/api/v1/report/` provides race report in json format. 

If xml format is preferred you can add `format=xml` parameter. 

documentation can be found on `/apidocs` subdirectory. 
