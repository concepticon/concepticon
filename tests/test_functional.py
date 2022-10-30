import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_json', '/relations'),
        ('get_html', '/parameters/1'),
        ('get_xml', '/parameters/1.rdf'),
        ('get_html', '/contributions/Hattori-1973-200'),
        ('get_xml', '/contributions/Hattori-1973-200.rdf'),
        ('get_html', '/contributions/Matisoff-1978-200'),
        ('get_dt', '/parameters'),
        ('get_xml', '/parameters/127.rdf'),
        ('get_xml', '/parameters/2209.rdf'),
        ('get_xml', '/parameters/2140.rdf'),
        ('get_dt', '/contributions?sSearch_5=chinese'),
        ('get_dt', '/values?iSortingCols=1&iSortCol_0=0'),
        ('get_dt', '/values?parameter=2'),
        ('get_dt', '/values?contribution=Brinton-1891-21&iSortingCols=2&iSortCol_0=0&iSortCol_1=1&sSearch_1=a'),
        ('get_html', '/values/Matisoff-1978-200-65'),
        ('get_xml', '/values/Matisoff-1978-200-65.rdf'),
        ('get_html', '/sources/Haspelmath2009'),
        ('get_dt', '/contributors'),
        ('get_dt', '/contributions'),

    ])
def test_pages(app, method, path):
    getattr(app, method)(path)


def test_misc(app):
    assert 'request.route' not in app.get_html('/')
    app.get('/contributions/Bennet-1976-100', status=301)
    app.get('/values/Bennet-1976-100-1', status=301)


def test_error(app):
    app.get('/search_concept', status=404)
    app.get('/search_concept?url=http://wold.clld.org/meaning/12-42', status=302)
