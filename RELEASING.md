
Releasing clld/concepticon
==========================

- recreate the database:
  ```shell script
  concepticon-app --repos-version v<VERSION> init --doi "<DOI>"
  ```

- Make sure the tests pass
  ```shell script
  pytest
  ```

- Create downloads:
  ```shell script
  clld-create-downloads development.ini 
  ```

- Upload the downloads to CDSTAR:
  ```shell script
  clldmpg --version=<version> dl2cdstar
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
