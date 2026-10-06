# Multi-Source Web Scraping & Data Consolidation Pipeline

A robust, production-ready Python web scraping and ETL (Extract, Transform, Load) pipeline that extracts data from two different public practice websites, cleans and standardizes the records, performs deduplication and validation, and outputs a single consolidated dataset along with a detailed summary report.

---

## 1. Project Overview & Objectives

Real-world web data is frequently messy, unstructured, and distributed across disparate layouts. This project simulates an industry-level data engineering workflow by:

* Scraping multi-page data from **Books to Scrape** (~1,000 books across 50 pages) and **Quotes to Scrape** (100 quotes across 10 pages).
* Implementing **dynamic pagination** via the "next" link rather than hardcoding page numbers.
* Consolidating heterogeneous data schemas into a single shared table layout.
* Cleaning messy text, converting prices to real numbers, standardizing ratings, and handling missing elements gracefully without crashing.
* Detecting duplicates using cryptographic hashing and fuzzy fingerprinting.
* Generating tidy output files (`final_dataset.csv` and `summary_report.json`) alongside execution logs (`scraper.log`).

---

## 2. Python Version & System Prerequisites

* **Python Version**: Python 3.10, 3.11, 3.12, or 3.13
* **Operating System**: Windows, macOS, or Linux
* **Dependencies**: `requests`, `beautifulsoup4`, `lxml`, `pytest`

---

## 3. Project Directory Structure

```text
scraping_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py       # Shared resilient HTTP session with exponential backoff retries
│   ├── books_scraper.py      # Selectors & dynamic pagination for Books to Scrape
│   └── quotes_scraper.py     # Selectors & dynamic pagination for Quotes to Scrape
├── processing/
│   ├── __init__.py
│   ├── cleaning.py           # Pure functions for text, price, rating, tag, and URL normalization
│   ├── validation.py         # Record-level validation checks returning specific failure reasons
│   └── deduplication.py      # Hashing & fingerprinting logic for duplicate detection
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py      # Unit tests for cleaning functions
│   ├── test_validation.py    # Unit tests for validation logic
│   └── test_deduplication.py # Unit tests for case-insensitive/whitespace-agnostic deduplication
├── output/
│   ├── final_dataset.csv     # Consolidated output table
│   └── summary_report.json   # Run metrics and reconciliation summary
├── logs/
│   └── scraper.log           # Time-stamped execution logs
├── main.py                   # Entry point orchestrating the full ETL pipeline
├── requirements.txt          # Locked dependency versions
├── README.md                 # Project documentation
└── AI_USAGE.md               # AI assistance disclosure and verification log
```

---

## 4. Installation & Setup Instructions

Open your terminal (PowerShell on Windows) and run the following commands:

```powershell
# Clone or open the project folder
cd scraping_assignment

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
# source venv/bin/activate

# Install dependencies from requirements.txt (or install manually)
pip install -r requirements.txt
```

---

## 5. How to Run

### Run Unit Tests

To verify the cleaning, validation, and deduplication logic without hitting the internet:

```powershell
pytest tests/ -v
```

### Run the Full Pipeline

To execute the complete web scraping and consolidation job:

```powershell
python main.py
```

---

## 6. Technical Implementation Details

### Pagination Approach

Both scrapers start at their respective home pages and dynamically locate the pagination element (`li.next > a`). Using `urllib.parse.urljoin`, the scraper follows the relative link to the subsequent page automatically, halting gracefully when no "next" button is found. This ensures robustness if pages are added or removed on the target sites.

### Standardized Data Model

Both sources are mapped into a unified schema to enable side-by-side analysis without data corruption or fake default values:

* `source`: Origin name ("Books to Scrape" or "Quotes to Scrape")
* `source_url`: Full URL of the specific record page
* `name_or_title`: Book title or quote text
* `category`: Book category or fixed tag label
* `price`: Float value representing the book price (empty for quotes)
* `rating`: Integer from 1 to 5 representing star ratings (empty for quotes)
* `author`: Author name (empty for books)
* `tags`: Semicolon-separated sorted lowercase tags (empty for books)
* `description`: Detailed description field
* `scraped_at`: UTC ISO timestamp

### Cleaning & Standardization

* **Text**: Strips non-breaking spaces (`\xa0`), tabs, and extraneous whitespace. Quotes are stripped of curly quotation marks.
* **Prices**: Regex matching extracts numeric values from currency symbols (e.g., converting `£51.77` to `51.77`).
* **Ratings**: Maps word-based ratings (e.g., `Three`) to integer values (`3`).

### Deduplication Strategy

A fingerprint is generated for each record by combining source-identifying fields (source + title for books; source + author + first 50 characters of quote text for quotes), normalizing case, stripping punctuation, collapsing whitespace, and hashing the resulting string with SHA-256. Duplicate entries are automatically filtered out during processing.

---

## 7. Output Description

* **`output/final_dataset.csv`**: Contains all unique, valid records from both websites in a uniform column structure.
* **`output/summary_report.json`**: Contains run metrics including total records collected per source, cleaning counts, rejections by reason, duplicates detected, final record count, start/end timestamps, and duration in seconds.
* **`logs/scraper.log`**: A time-stamped log recording page navigations, warnings, and error exceptions.