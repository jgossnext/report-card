import requests
from bs4 import BeautifulSoup
import pandas as pd

class HomePrices:
    def __init__(self):
        self.url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_by_median_home_price'

    def scrape_data(self):
        headers = []
        rows = []
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable sortable'})

        for th in table.find_all('th'):
            headers.append(th.text.strip())
        for tr in table.find_all('tr'):
            cells = tr.find_all('td')
            if len(cells) > 0:
                row = []
                for td in cells:
                    row.append(td.text.strip())
                rows.append(row)
        home_price_df = pd.DataFrame(rows, columns=headers)
        return home_price_df

    @staticmethod
    def clean_home_prices(home_price_df: pd.DataFrame) -> pd.DataFrame:
        home_price_df['amount'] = home_price_df['Median home price in US$'].str.replace('$', '',
                                                                                        regex=False)  # Remove dollar sign
        home_price_df['amount'] = home_price_df['amount'].str.replace(',', '', regex=False)
        home_price_df['amount'] = pd.to_numeric(home_price_df['amount'], errors='coerce')
        return home_price_df

    def compile_homeprices(self) -> pd.DataFrame:
        scraped_data = self.scrape_data()
        home_prices = self.clean_home_prices(scraped_data)
        return home_prices