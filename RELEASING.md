
Releasing clld/concepticon
==========================

- update clld/concepticon-data
- recreate the database
- Update landing page:
  - DOI badge
  - release number and github link
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
  py34: commands succeeded
  py27: commands succeeded
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
