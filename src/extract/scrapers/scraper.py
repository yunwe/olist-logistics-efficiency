import os
import requests
from bs4 import BeautifulSoup
import time
import logging
import pandas as pd

# 1. Base Class (The Blueprint)
class BaseScraper:
    def __init__(self, url, file_name):
        self.url = url
        self.raw_dir = "data/raw"
        self.save_path = os.path.join(self.raw_dir, file_name)
        
        USER_AGENT = "MyEducationalBot/1.0 (contact: syn@aungthuya.dev)"
        self.headers = {
            'User-Agent': USER_AGENT
        }
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, endpoint):
        """Handles the HTTP request and basic error handling."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status() # Raises error for 4xx or 5xx codes
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch {self.url}: {e}")
            return None
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        os.makedirs(self.raw_dir, exist_ok=True)
        df.to_csv(self.save_path, index=False)

# 2. Implementation Class (The Specific Logic)
class TableScraper(BaseScraper):
    def scrape_table(self, index: int, force_scrape=False):
        if os.path.exists(self.save_path) and not force_scrape:
            return 
        
        """Specific logic to extract table from HTML and save to Disk."""
        html = self.fetch_page(self.url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        all_tables = soup.find_all('table')
        if len(all_tables) > index:
            table = all_tables[index]
            df = self._to_df(table)
            self._save_to_disk(df)
        else:
            self.logger.error(f"Error: Table index out of bound at {url}")

    def _to_df(self, table) -> pd.DataFrame:
        data = []
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())
            
        for tr in table.find_all('tr'):
            cells = tr.find_all('td')
            if len(cells) == 0:
                continue
            row = []
            for cell in cells:
                row.append(cell.text.strip())
            data.append(row)
        
        return pd.DataFrame(data, columns=headers if headers else None)
