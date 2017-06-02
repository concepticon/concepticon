from setuptools import setup, find_packages


requires = [
    'clld>=3.1.1',
    'clldmpg>=2.4.1',
    'markdown',
    'psycopg2',
    'uritemplate',
    'pyconcepticon',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock',
]


setup(name='concepticon',
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
      install_requires=requires,
      tests_require=tests_require,
      test_suite="concepticon",
      entry_points="""\
[paste.app_factory]
main = concepticon:main
""",
      )
