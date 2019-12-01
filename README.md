# Downloading APKs from the Google Play Store

### Prerequisites
* Python 3
* GooglePlay APIs:
  ```
  $ git clone --branch v0.4.3 https://github.com/NoMore201/googleplay-api.git
  $ cd googleplay-api/
  $ pip3 install -e .
  ```
### Running
* First you will need an authentication token for Google APIs. You will
only need to run this once and then you will no longer need to keep
providing your email and password. Enter your email in password in the
`prep_token_id.py` script and then run it:
    ```
    $ python3 prep_token_id.py
    ```
    **Note**: you may get an error when running it for the first time, but
    this API seems to work the second time.
* Save the `gsfId` and the `authSubToken`. Now you can crawl the Google
Play Store. We provide a script for fetching the top 10 apps from each
Google Play category and save the information in a CSV.
You can run it as-is, or modify it as you see fit:
    ```
    $ python3 prep_app_list.py <gsfId> <authSubToken> <output.csv>
    ```
* Once you have a list of apps, you can use our script to download the APKs:
    ```
    $ python3 download_apks.py <gsfId> <authSubToken> <apps.csv> <output_dir>
    ```
    Where `<apps.csv>` is the CSV file from the earlier step, and
    `<output_dir>` is the directory to which you want to save APKs to.