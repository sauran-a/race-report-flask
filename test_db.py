from app import app


def test_race_report_no_params():
    tester = app.test_client()
    response = tester.get('/api/v1/report/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.get_json()) == 19


def test_race_report_json():
    tester = app.test_client()
    response = tester.get('/api/v1/report/?format=json')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.get_json()) == 19


def test_race_report_xml():
    tester = app.test_client()
    response = tester.get('/api/v1/report/?format=xml')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'


def test_drivers_report_no_param():
    tester = app.test_client()
    response = tester.get('/api/v1/report/drivers')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


def test_drivers_report_json():
    tester = app.test_client()
    response = tester.get('/api/v1/report/drivers?format=json')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


def test_drivers_report_xml():
    tester = app.test_client()
    response = tester.get('/api/v1/report/drivers?format=xml')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/xml'


def test_driver():
    driver_svf = {
        "abbreviation": "SVF",
        "club_name": "FERRARI",
        "full_name": "Sebastian Vettel",
        "time": "01:04.415000",
        'id': 1
    }
    tester = app.test_client()
    response = tester.get('/api/v1/report/drivers?driver_id=SVF')
    assert response.status_code == 200
    assert response.get_json() == driver_svf
