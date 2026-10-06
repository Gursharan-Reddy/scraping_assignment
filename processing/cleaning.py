import re

RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = " ".join(value.replace("\xa0", " ").split())
    return text or None

def strip_quotes(value: str | None) -> str | None:
    cleaned = clean_text(value)
    if cleaned and cleaned.startswith("“") and cleaned.endswith("”"):
        return cleaned[1:-1].strip()
    return cleaned

def clean_price(raw: str | None) -> float | None:
    if not raw:
        return None
    match = re.search(r"\d+(?:\.\d+)?", raw.replace(",", ""))
    return float(match.group()) if match else None

def clean_rating(raw: str | None) -> int | None:
    if not raw:
        return None
    for word in raw.lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]
    return None

def clean_tags(raw: str | None) -> str | None:
    if not raw:
        return None
    tags = [clean_text(t).lower() for t in raw.split(";") if clean_text(t)]
    tags = sorted(list(set(tags)))
    return ";".join(tags) if tags else None

def normalize_url(url: str | None) -> str | None:
    cleaned = clean_text(url)
    if cleaned and cleaned.startswith(("http://", "https://")):
        return cleaned
    return None