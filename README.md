# Downloading APKs from the Google Play Store
This repository was used to download APKs for the NoMoATS project.
For an overview of the project, please visit the
project [website](http://athinagroup.eng.uci.edu/projects/nomoads/).

### Prerequisites
* Python 3, pip, and protobuf compiler:
  ```
  $ sudo apt install python3
  $ sudo apt install python3-pip
  $ sudo apt install protobuf-compiler
  ```
* [GooglePlay APIs, version 0.4.4](https://github.com/NoMore201/googleplay-api/tree/v0.4.4):
  ```
  $ git clone --branch v0.4.4 https://github.com/NoMore201/googleplay-api.git
  $ cd googleplay-api/
  $ python3 setup.py build
  $ pip3 install -e .
  ```

### Running
* First you will need an authentication token for Google APIs. You will
only need to run this once and then you will no longer need to keep
providing your email and password. Open the `prep_token_id.py` script,
enter your email and password where indicated, and then run the script:
    ```
    $ python3 prep_token_id.py
    ```
    **Note**: you may get an error when running it for the first time, but
    this API seems to work the second time.
* Save the `gsfId` and the `authSubToken`. Now you can crawl the Google
Play Store. We provide a script for fetching the top 10 apps from each
Google Play category and save the information in a CSV file.
You can run it as-is, or modify it as you see fit:
    ```
    $ python3 prep_app_list.py <gsfId> <authSubToken> <apps.csv>
    ```
    Where `<apps.csv>` is the CSV file to which you want save the list of apps.
* Next, you can download APKs corresponding to package names in `<apps.csv>`:
    ```
    $ python3 download_apks.py <gsfId> <authSubToken> <apps.csv> <output_dir>
    ```
    Where `<apps.csv>` is the CSV file from the earlier step, and
    `<output_dir>` is the directory to which you want to save APKs to.
