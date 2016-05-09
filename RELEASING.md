
Releasing clld/concepticon
==========================

- update clld/concepticon-data
- recreate the database
- Update DOI badge on start page
- Create downloads:
```
$ clld-create-downloads development.ini 
```

- Make sure the tests pass
- Commit and push all changes
- Create a release of clld/concepticon with the same version number as the data release.
- Deploy to http://concepticon.clld.org
- Copy downloads