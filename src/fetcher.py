"""
RSS and News Fetcher module.
Fetches articles from Google News RSS and other curated feeds.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import time
from datetime import datetime


def clean_html(raw_html: str) -> str:
    """Removes HTML tags and unescapes entities."""
    if not raw_html:
        return ""
    cleanr = re.compile(r"<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    cleantext = cleantext.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", "\"").replace("&#39;", "'")
    return " ".join(cleantext.split())


def fetch_feed_items(url: str, max_items: int = 5, timeout: int = 10) -> list:
    """Fetches and parses RSS/Atom feed items."""
    items = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()

        root = ET.fromstring(content)

        # Standard RSS channel/item
        for item in root.findall(".//item")[: max_items * 2]:
            title_elem = item.find("title")
            link_elem = item.find("link")
            desc_elem = item.find("description")
            pubdate_elem = item.find("pubDate")

            title = title_elem.text if title_elem is not None and title_elem.text else ""
            link = link_elem.text if link_elem is not None and link_elem.text else ""
            desc = clean_html(desc_elem.text) if desc_elem is not None and desc_elem.text else ""
            pub_date = pubdate_elem.text if pubdate_elem is not None and pubdate_elem.text else ""

            if title:
                items.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "description": desc.strip(),
                    "pub_date": pub_date.strip()
                })

            if len(items) >= max_items:
                break

    except Exception as e:
        print(f"Warning: Failed to fetch feed {url}: {e}")

    return items


def fetch_all_categories(categories_config: dict) -> dict:
    """Fetches articles across all configured categories and removes duplicates."""
    collected_data = {}

    for cat_key, cat_info in categories_config.items():
        if not cat_info.get("enabled", True):
            continue

        cat_title = cat_info.get("display_name", cat_key.replace("_", " ").title())
        sources = cat_info.get("sources", [])
        max_items = cat_info.get("max_items", 4)

        seen_titles = set()
        cat_articles = []

        for source in sources:
            source_items = fetch_feed_items(source, max_items=max_items)
            time.sleep(0.6)
            for item in source_items:
                normalized_title = item["title"].lower()
                if normalized_title not in seen_titles:
                    seen_titles.add(normalized_title)
                    cat_articles.append(item)
                if len(cat_articles) >= max_items:
                    break
            if len(cat_articles) >= max_items:
                break

        collected_data[cat_key] = {
            "display_name": cat_title,
            "articles": cat_articles
        }

    return collected_data
