from app import app
import unittest
from contextlib import contextmanager
from flask import template_rendered


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_default_view(self):
        view_context = {
            'results': [{'abr': 'SVF', 'time': '0:01:04.415000', 'full_name': 'Sebastian Vettel', 'club': 'FERRARI'},
                        {'abr': 'VBM', 'time': '0:01:12.434000', 'full_name': 'Valtteri Bottas', 'club': 'MERCEDES'},
                        {'abr': 'SVM', 'time': '0:01:12.463000', 'full_name': 'Stoffel Vandoorne', 'club': 'MCLAREN RENAULT'},
                        {'abr': 'KRF', 'time': '0:01:12.639000', 'full_name': 'Kimi Räikkönen', 'club': 'FERRARI'},
                        {'abr': 'FAM', 'time': '0:01:12.657000', 'full_name': 'Fernando Alonso', 'club': 'MCLAREN RENAULT'},
                        {'abr': 'CLS', 'time': '0:01:12.829000', 'full_name': 'Charles Leclerc', 'club': 'SAUBER FERRARI'},
                        {'abr': 'SPF', 'time': '0:01:12.848000', 'full_name': 'Sergio Perez', 'club': 'FORCE INDIA MERCEDES'},
                        {'abr': 'RGH', 'time': '0:01:12.930000', 'full_name': 'Romain Grosjean', 'club': 'HAAS FERRARI'},
                        {'abr': 'PGS', 'time': '0:01:12.941000', 'full_name': 'Pierre Gasly', 'club': 'SCUDERIA TORO ROSSO HONDA'},
                        {'abr': 'CSR', 'time': '0:01:12.950000', 'full_name': 'Carlos Sainz', 'club': 'RENAULT'},
                        {'abr': 'NHR', 'time': '0:01:13.065000', 'full_name': 'Nico Hulkenberg', 'club': 'RENAULT'},
                        {'abr': 'BHS', 'time': '0:01:13.179000', 'full_name': 'Brendon Hartley', 'club': 'SCUDERIA TORO ROSSO HONDA'},
                        {'abr': 'MES', 'time': '0:01:13.265000', 'full_name': 'Marcus Ericsson', 'club': 'SAUBER FERRARI'},
                        {'abr': 'LSW', 'time': '0:01:13.323000', 'full_name': 'Lance Stroll', 'club': 'WILLIAMS MERCEDES'},
                        {'abr': 'KMH', 'time': '0:01:13.393000', 'full_name': 'Kevin Magnussen', 'club': 'HAAS FERRARI'},
                        {'abr': 'DRR', 'time': '0:02:47.987000', 'full_name': 'Daniel Ricciardo', 'club': 'RED BULL RACING TAG HEUER'},
                        {'abr': 'SSW', 'time': '0:04:47.294000', 'full_name': 'Sergey Sirotkin', 'club': 'WILLIAMS MERCEDES'},
                        {'abr': 'EOF', 'time': '0:05:46.972000', 'full_name': 'Esteban Ocon', 'club': 'FORCE INDIA MERCEDES'},
                        {'abr': 'LHM', 'time': '0:06:47.540000', 'full_name': 'Lewis Hamilton', 'club': 'MERCEDES'}]
        }

        with captured_templates(app) as templates:
            response = self.app.get('/report')
            template, context = templates[0]
            self.assertEqual('report.html', template.name)
            self.assertEqual(200, response.status_code)

            for key in view_context:
                self.assertEqual(context[key], view_context[key])

    def test_index(self):
        with captured_templates(app) as templates:
            response = self.app.get('/')
            template, context = templates[0]
            self.assertEqual('report.html', template.name)
            self.assertEqual(200, response.status_code)

    def test_drivers(self):
        tester = app.test_client(self)
        response = tester.get('/report/drivers', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_index_header(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Race Report' in response.data.title())

    def test_report_header(self):
        tester = app.test_client(self)
        response = tester.get('/report', content_type='html/text')
        self.assertTrue(b'Race Report' in response.data.title())

    def test_drivers_header(self):
        tester = app.test_client(self)
        response = tester.get('/report/drivers', content_type='html/text')
        self.assertTrue(b'Drivers Report' in response.data.title())

    def test_drivers_id(self):
        tester = app.test_client(self)
        response = tester.get('/report/drivers?driver_id=SVF', content_type='html/text')
        self.assertIn(b'Sebastian Vettel', response.data.title())
        self.assertIn(b'Ferrari', response.data.title())
        self.assertIn(b'0:01:04.415000', response.data.title())

        response = tester.get('/report/drivers?driver_id=BHS', content_type='html/text')
        self.assertIn(b'Brendon Hartley', response.data.title())


if __name__ == '__main__':
    unittest.main()
