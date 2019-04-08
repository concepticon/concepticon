
Releasing clld/concepticon
==========================

- update the clone of concepticon/concepticon-data:
```bash
cd ../concepticon-data
git checkout vX.Y
```
- recreate the database. This assumes a soft link `data/concepticon-data`.
```bash
dropdb concepticon
createdb concepticon
python concepticon/scripts/initializedb.py development.ini
```

- Update the latest DOI badge for concepticon/concepticon-data on the landing page.
- Create downloads:
```
clld-create-downloads development.ini 
```

- Upload the downloads to CDSTAR:
```
clldmpg --version=<version> dl2cdstar
```

- Make sure the tests pass
```
tox
  ...
  py35: commands succeeded
  congratulations :)
```

- Commit and push all changes
```
git commit -a -m"release <version>"
```

- Create a release of clld/concepticon with the same version number as the data release.
- Deploy to http://concepticon.clld.org
```
(appconfig)$ fab deploy:production
```
