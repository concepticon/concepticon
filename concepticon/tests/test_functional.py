from clldutils.path import Path
from clld.tests.util import TestWithApp

import concepticon


class Tests(TestWithApp):
    __cfg__ = Path(concepticon.__file__).parent.joinpath('..', 'development.ini').resolve()
    __setup_db__ = False

    def test_home(self):
        self.app.get_html('/')

    def test_misc(self):
        self.app.get_json('/relations')
        self.app.get_html('/parameters/1')
        self.app.get_xml('/parameters/1.rdf')
        self.app.get_html('/contributions/Hattori-1973-200')
        self.app.get_xml('/contributions/Hattori-1973-200.rdf')
        self.app.get_html('/contributions/Matisoff-1978-200')
        self.app.get_dt('/parameters')
        self.app.get_xml('/parameters/127.rdf')
        self.app.get_xml('/parameters/2209.rdf')
        self.app.get_xml('/parameters/2140.rdf')
        self.app.get_dt('/contributions')
        self.app.get_dt('/contributions?sSearch_5=chinese')
        self.app.get_dt('/values?iSortingCols=1&iSortCol_0=0')
        self.app.get_dt('/values?parameter=2')
        self.app.get_dt('/values?contribution=Brinton-1891-21&iSortingCols=2&iSortCol_0=0&iSortCol_1=1&sSearch_1=a')
        self.app.get_xml('/values/Matisoff-1978-200-65.rdf')
        self.app.get_html('/sources/haspelmath2009')
        self.app.get_dt('/contributors')
        self.app.get('/search_concept', status=404)
        self.app.get('/search_concept?url=http://wold.clld.org/meaning/12-42', status=302)
