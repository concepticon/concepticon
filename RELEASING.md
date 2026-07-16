
Releasing clld/concepticon
==========================

- Recreate the database (in concepticon-data/ passing in the DOI of the concepticon-data release):
  ```shell
  clld initdb development.ini --cldf ../concepticon-cldf/cldf/Wordlist-metadata.json
  ```

- Make sure the tests pass (in clld/concepticon):
  ```shell
  pytest
  ```

- Create downloads (in clld/concepticon):
  ```shell
  clld create_downloads development.ini concepticon.clld.org
  ```
  unzip and add as file of new version to https://doi.org/10.5281/zenodo.21396763

- Commit and push all changes
  ```shell
  git commit -a -m"release <version>"
  git push origin
  ```

- Deploy to https://concepticon.clld.org
  ```shell
  (appconfig)$ appconfig appdeploy concepticon
  ```
