
Releasing clld/concepticon
==========================

- Make sure the database can be recreated (in concepticon-data/):
  ```shell script
  concepticon-app init --dry-run
  ```

- Recreate the database (in concepticon-data/):
  ```shell script
  concepticon-app --repos-version v<VERSION> init --doi "<DOI>"
  ```

- Make sure the tests pass (in clld/concepticon):
  ```shell script
  pytest
  ```

- Create downloads (in clld/concepticon):
  ```shell script
  clld-create-downloads development.ini 
  ```

- Upload the downloads to CDSTAR (in clld/concepticon):
  ```shell script
  clldmpg dl2cdstar --version=<version>
  ```

- Commit and push all changes
  ```shell script
  git commit -a -m"release <version>"
  ```

- Create a release of `clld/concepticon` with the same version number as the data release.
- Deploy to https://concepticon.clld.org
  ```shell script
  (appconfig)$ fab deploy:production
  ```
