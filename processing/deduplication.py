import hashlib
import re

def make_fingerprint(rec: dict) -> str:
    source = rec.get("source", "")
    title = rec.get("name_or_title", "")
    author = rec.get("author", "")
    
    if source == "Books to Scrape":
        key = f"{source} {title}"
    else:
        key = f"{source} {author} {title[:50]}"
        
    key = re.sub(r"[^\w\s]", "", key.lower())
    key = " ".join(key.split())
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def find_duplicates(records: list[dict]) -> tuple[list[dict], list[dict]]:
    seen = set()
    unique = []
    dupes = []
    for rec in records:
        fp = make_fingerprint(rec)
        if fp in seen:
            dupes.append(rec)
        else:
            seen.add(fp)
            unique.append(rec)
    return unique, dupes