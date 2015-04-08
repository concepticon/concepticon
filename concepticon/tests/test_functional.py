from path import path

from clld.tests.util import TestWithApp

import concepticon


class Tests(TestWithApp):
    __cfg__ = path(concepticon.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get_html('/')

    def test_misc(self):
        self.app.get_html('/parameters/1')
        self.app.get_xml('/parameters/1.rdf')
        self.app.get_html('/contributions/Shiro-1973-200')
        self.app.get_xml('/contributions/Shiro-1973-200.rdf')
        self.app.get_html('/contributions/Matisoff-1978-200')
        self.app.get_dt('/parameters')
        self.app.get_dt('/contributions')
        self.app.get_dt('/values')
        self.app.get_dt('/values?parameter=2')
        self.app.get_dt('/values?contribution=Brinton-1891-21')
        self.app.get_xml('/values/Matisoff-1978-200-65.rdf')
