
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

- Upload the downloads to CDSTAR (in clld/concepticon):
  ```shell
  clldmpg dl2cdstar --version=<version>
  ```

- Commit and push all changes
  ```shell
  git commit -a -m"release <version>"
  git push origin
  ```

- Deploy to https://concepticon.clld.org
  ```shell
  (appconfig)$ fab deploy:production
  ```

