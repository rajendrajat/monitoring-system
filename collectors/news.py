import requests
import xml.etree.ElementTree as ET


def get_news():
    try:
        url = "https://news.google.com/rss/search?q=war+oil+inflation&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=10)

        root = ET.fromstring(response.content)

        headlines = []
        for item in root.findall(".//item")[:5]:
            title = item.find("title").text
            headlines.append(title)

        return headlines

    except Exception as e:
        print(f"[NEWS ERROR] {e}")
        return []
