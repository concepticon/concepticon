from setuptools import setup, find_packages


setup(
    name='concepticon',
    version='0.0',
    description='concepticon',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='http://concepticon.clld.org',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld~=4.0',
        'clldmpg~=3.1',
        'markdown',
        'uritemplate',
        'pyconcepticon',
        'sqlalchemy',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'psycopg2',
            'tox',
        ],
        'test': [
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="concepticon",
    entry_points="""\
[paste.app_factory]
main = concepticon:main
""")
