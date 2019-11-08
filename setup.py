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
        'clldutils>=3.3.0',
        'clld>=5.1.1',
        'clldmpg>=3.3.1',
        'markdown',
        'uritemplate',
        'pyconcepticon>=2.5.1',
        'sqlalchemy',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'mock',
            'psycopg2',
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
    entry_points={
        'console_scripts': [
            'concepticon-app=concepticon.__main__:main',
        ],
        'paste.app_factory': [
            'main=concepticon:main',
        ]
    },
)
