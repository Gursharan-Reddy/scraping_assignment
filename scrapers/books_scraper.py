from datetime import datetime
import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class BooksScraper:
    BASE_URL = "https://books.toscrape.com/"

    def __init__(self, session: requests.Session):
        self.session = session

    def scrape(self) -> list[dict]:
        url = self.BASE_URL
        page = 1
        records = []
        
        while url:
            logger.info(f"Scraping Books page {page}: {url}")
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = "utf-8"
            except requests.RequestException as exc:
                logger.error(f"Failed to fetch Books page {url}: {exc}")
                break

            soup = BeautifulSoup(response.text, "lxml")
            articles = soup.select("article.product_pod")
            
            for article in articles:
                try:
                    link_elem = article.select_one("h3 > a")
                    price_elem = article.select_one("p.price_color")
                    rating_elem = article.select_one("p.star-rating")
                    
                    title = link_elem.get("title") if link_elem else None
                    href = urljoin(url, link_elem.get("href")) if link_elem and link_elem.get("href") else None
                    price_raw = price_elem.get_text() if price_elem else None
                    rating_raw = " ".join(rating_elem.get("class", [])) if rating_elem else None

                    record = {
                        "source": "Books to Scrape",
                        "source_url": href,
                        "name_or_title": title,
                        "category": None,  # Can be expanded by visiting detail pages if desired
                        "price": price_raw,
                        "rating": rating_raw,
                        "author": None,
                        "tags": None,
                        "description": None,
                        "scraped_at": datetime.utcnow().isoformat() + "Z"
                    }
                    records.append(record)
                except Exception as e:
                    logger.warning(f"Error parsing individual book record: {e}")

            next_link = soup.select_one("li.next > a")
            url = urljoin(url, next_link["href"]) if next_link else None
            page += 1
            time.sleep(0.5)

        return records