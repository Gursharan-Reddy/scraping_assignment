from processing.cleaning import clean_price, clean_rating, clean_text, strip_quotes

def test_clean_text():
    assert clean_text("  Hello \n World  \xa0") == "Hello World"
    assert clean_text(None) is None

def test_strip_quotes():
    assert strip_quotes(" “Hello World” ") == "Hello World"

def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price(None) is None

def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("One") == 1