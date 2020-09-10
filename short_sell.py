"""
    Download daily short sell data from https://www.asx.com.au/data/shortsell.txt.
"""

from datetime import date

import requests


def download_asx_daily_short_sell(url="https://www.asx.com.au/data/shortsell.txt"):
    resp = requests.get(url, allow_redirects=True)

    today = date.today().strftime("%Y%m%d")
    open('data/short_sell/asx_short_sell_{today}.txt'.format(today=today), 'wb').write(resp.content)


if __name__ == "__main__":
    # execute only if run as a script
    download_asx_daily_short_sell()
