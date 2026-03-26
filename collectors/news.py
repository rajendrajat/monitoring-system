import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import time


def get_news():
    """
    Fetch latest news from Google News RSS with cache-busting
    Forces fresh data every fetch to ensure latest headlines
    """
    try:
        # Add timestamp parameter to force fresh data and avoid caching
        timestamp = int(time.time())
        url = f"https://news.google.com/rss/search?q=india+inflation+war+oil+gold&hl=en-IN&gl=IN&ceid=IN:en&t={timestamp}"

        # Add headers to prevent caching
        headers = {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        root = ET.fromstring(response.content)

        headlines = []
        # Fetch top 10 for more variety
        for item in root.findall(".//item")[:10]:
            title_elem = item.find("title")
            pub_date_elem = item.find("pubDate")

            if title_elem is not None:
                title = title_elem.text
                pub_date = pub_date_elem.text if pub_date_elem is not None else "Recent"

                # Store both title and publish date for freshness tracking
                headline_info = {
                    "title": title,
                    "date": pub_date,
                    "fresh": True  # Mark as freshly fetched
                }
                headlines.append(headline_info)

        if headlines:
            print(
                f"[NEWS INFO] Fetched {len(headlines)} fresh headlines at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return headlines
        else:
            print("[NEWS ERROR] No headlines found in RSS feed")
            return []

    except requests.exceptions.RequestException as e:
        print(f"[NEWS ERROR] Network issue: {e}")
        return []
    except ET.ParseError as e:
        print(f"[NEWS ERROR] RSS parsing failed: {e}")
        return []
    except Exception as e:
        print(f"[NEWS ERROR] {e}")
        return []
