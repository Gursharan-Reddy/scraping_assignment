from collections import defaultdict
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import csv

from scrapers.base_scraper import create_session
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.cleaning import clean_text, strip_quotes, clean_price, clean_rating, clean_tags, normalize_url
from processing.validation import validate_record
from processing.deduplication import find_duplicates

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "scraper.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger("main")
    start_time = datetime.now(timezone.utc)
    
    session = create_session()
    
    logger.info("Starting extraction phase...")
    books_raw = BooksScraper(session).scrape()
    quotes_raw = QuotesScraper(session).scrape()
    
    collected_counts = {
        "Books to Scrape": len(books_raw),
        "Quotes to Scrape": len(quotes_raw)
    }
    
    all_raw = books_raw + quotes_raw
    logger.info(f"Extracted {len(books_raw)} books and {len(quotes_raw)} quotes.")

    logger.info("Starting cleaning phase...")
    cleaned_records = []
    cleaned_counts = defaultdict(int)
    
    for rec in all_raw:
        source = rec.get("source")
        if source == "Books to Scrape":
            rec["name_or_title"] = clean_text(rec.get("name_or_title"))
            rec["price"] = clean_price(rec.get("price"))
            rec["rating"] = clean_rating(rec.get("rating"))
        elif source == "Quotes to Scrape":
            rec["name_or_title"] = strip_quotes(rec.get("name_or_title"))
            rec["author"] = clean_text(rec.get("author"))
            rec["tags"] = clean_tags(rec.get("tags"))
        
        rec["source_url"] = normalize_url(rec.get("source_url"))
        cleaned_records.append(rec)
        cleaned_counts[source] += 1

    logger.info("Starting validation phase...")
    valid_records = []
    rejected_by_reason = defaultdict(int)
    
    for rec in cleaned_records:
        problems = validate_record(rec)
        if problems:
            for p in problems:
                rejected_by_reason[p] += 1
            logger.warning(f"Rejected record from {rec.get('source')}: {problems} -> {rec.get('name_or_title')}")
        else:
            valid_records.append(rec)

    logger.info("Starting deduplication phase...")
    unique_records, duplicate_records = find_duplicates(valid_records)
    duplicates_count = len(duplicate_records)
    if duplicates_count > 0:
        logger.info(f"Detected and filtered out {duplicates_count} duplicates.")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    csv_path = output_dir / "final_dataset.csv"
    fieldnames = [
        "source", "source_url", "name_or_title", "category",
        "price", "rating", "author", "tags", "description", "scraped_at"
    ]
    
    logger.info(f"Writing dataset to {csv_path}...")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in unique_records:
            writer.writerow(r)

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    summary = {
        "collected_per_source": collected_counts,
        "cleaned_per_source": dict(cleaned_counts),
        "rejected_by_reason": dict(rejected_by_reason),
        "duplicates_detected": duplicates_count,
        "final_record_count": len(unique_records),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": round(duration, 2)
    }

    json_path = output_dir / "summary_report.json"
    logger.info(f"Writing summary report to {json_path}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    logger.info("Pipeline execution completed successfully!")

if __name__ == "__main__":
    main()