from processing.validation import validate_record

def test_validate_record_valid():
    rec = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book.html",
        "name_or_title": "Test Book",
        "price": 10.99,
        "rating": 4
    }
    assert validate_record(rec) == []

def test_validate_record_invalid():
    rec = {
        "source": "Unknown",
        "source_url": "ftp://bad-url.com",
        "name_or_title": "",
        "price": -5,
        "rating": 6
    }
    problems = validate_record(rec)
    assert "unknown_source" in problems
    assert "missing_name" in problems
    assert "invalid_url" in problems
    assert "invalid_price" in problems
    assert "invalid_rating" in problems