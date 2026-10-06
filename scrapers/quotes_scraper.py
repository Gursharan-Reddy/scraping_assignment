from datetime import datetime
import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class QuotesScraper:
    BASE_URL = "https://quotes.toscrape.com/"

    def __init__(self, session: requests.Session):
        self.session = session

    def scrape(self) -> list[dict]:
        url = self.BASE_URL
        page = 1
        records = []

        while url:
            logger.info(f"Scraping Quotes page {page}: {url}")
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = "utf-8"
            except requests.RequestException as exc:
                logger.error(f"Failed to fetch Quotes page {url}: {exc}")
                break

            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.select("div.quote")

            for q in quotes:
                try:
                    text_elem = q.select_one("span.text")
                    author_elem = q.select_one("small.author")
                    tag_elems = q.select("div.tags > a.tag")
                    author_link_elem = q.select_one("span > a[href]")

                    quote_text = text_elem.get_text() if text_elem else None
                    author_name = author_elem.get_text() if author_elem else None
                    tags = [t.get_text() for t in tag_elems] if tag_elems else []
                    
                    source_url = urljoin(url, author_link_elem.get("href")) if author_link_elem else url

                    record = {
                        "source": "Quotes to Scrape",
                        "source_url": source_url,
                        "name_or_title": quote_text,
                        "category": "Quotes",
                        "price": None,
                        "rating": None,
                        "author": author_name,
                        "tags": ";".join(tags) if tags else None,
                        "description": None,
                        "scraped_at": datetime.utcnow().isoformat() + "Z"
                    }
                    records.append(record)
                except Exception as e:
                    logger.warning(f"Error parsing individual quote record: {e}")

            next_link = soup.select_one("li.next > a")
            url = urljoin(url, next_link["href"]) if next_link else None
            page += 1
            time.sleep(0.5)

        return records