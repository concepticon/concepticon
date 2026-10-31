
Releasing clld/concepticon
==========================

```shell
git clone https://github.com/concepticon/concepticon
git clone --branch v3.4.1 --depth 1 https://github.com/concepticon/concepticon-cldf
git clone --branch v1.1 --depth 1 https://github.com/concepticon/norare-cldf
cd concepticon
pip install -e .[test]
```

Recreate the database (in concepticon-data/ passing in the DOI of the concepticon-data release) (DOI: 10.5281/zenodo.21373838):
```shell
clld initdb development.ini --cldf ../concepticon-cldf/cldf/Wordlist-metadata.json
```

Make sure the tests pass (in clld/concepticon):
```shell
pytest
```

Create downloads (in clld/concepticon):
```shell
clld create_downloads development.ini concepticon.clld.org
```
unzip and add as file of new version to https://doi.org/10.5281/zenodo.21396763

Run the tests `pytest`.
```shell
pytest
```

Commit and push all changes
```shell
git commit -a -m"release <version>"
git push origin
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 concepticon > concepticon.sql.gz
```

