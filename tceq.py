from datetime import datetime
import pytz
import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class API:
    # TCEQ URLs
    tceq_site_data_url = "https://www.tceq.texas.gov/cgi-bin/compliance/monops/daily_summary.pl"
    tceq_sites_url = "https://www17.tceq.texas.gov/tamis/index.cfm?fuseaction=report.site_list&sort=AQS_SITE_CD&order" \
                     "=asc&formSub=1&cams=checked&TCEQRegion=checked&siteName=checked&strAddr=checked&cityName" \
                     "=checked&zipCode=checked&cntyName=checked&lat=checked&long=checked&latLongType=dec&actDT" \
                     "=checked&urbanArea=checked&ownByName=checked&EPARegistered=checked&showActiveOnly=1&regFilter" \
                     "=&cntyFilter=&camsFilter= "

    # Setting local TZ because all TCEQ monitors are in Texas.
    local_tz = pytz.timezone('America/Chicago')

    def __init__(self):
        # Give default timestamp
        self.timestamp = datetime.now().astimezone(tz=self.local_tz).timestamp()

    def get_html_from_url(self, url: object, params: object = None, method: object = None) -> object:
        # Use get or post
        if method == 'post':
            resp = requests.post(url, params=params)
        else:
            resp = requests.get(url, params=params)

        # Debug URL
        pprint(resp.url)

        # Convert to HTML
        html = BeautifulSoup(resp.text, 'html.parser')
        return html.prettify()

    def get_sites(self):
        dfs = pd.read_html(self.tceq_sites_url)
        table = dfs[-1]
        return table.to_json(orient="records")

    def get_date(self, timestamp):
        return datetime.fromtimestamp(timestamp).astimezone(tz=self.local_tz)

    def get_site_data(self, site_id=56, timestamp=None):
        # Get timestamp
        if timestamp is None:
            timestamp = self.timestamp

        # Generate date
        date = self.get_date(timestamp)

        # Prepare JSON
        params = {
            'select_date': "user",
            'user_month': date.month - 1,  # TCEQ has a weird offset.
            'user_day': date.day,
            'user_year': date.year,
            'select_site': "|||" + str(site_id),
            'time_format': '24hr'
        }

        html = self.get_html_from_url(self.tceq_site_data_url, params=params)
        dfs = pd.read_html(html, header=0)
        table = dfs[-1]
        # table.drop(table.index[-1], axis=1)
        pprint(table)
        return table.to_json()
