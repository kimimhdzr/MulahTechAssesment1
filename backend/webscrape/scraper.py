import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse as parse_date

def scrape_the_verge():
    urls = ["https://www.theverge.com/"] + [
    f"https://www.theverge.com/archives/{i}" for i in range(2, 16)
]

    target_classes = [
        "_1lkmsmo1",
        "_1lkmsmo1 _1lkmsmo2",
        "yy0d3l8",
    ]

    articles = []

    for url in urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            continue

        for cls in target_classes:
            found_links = soup.find_all('a', class_=cls)
            for a in found_links:
                title = a.get_text(strip=True)
                link = a.get('href')
                time_tag = (
                    a.find('time') or
                    a.find_next('time') or
                    a.find_previous('time')
                )

                pub_time = None
                if time_tag:
                    if time_tag.has_attr('datetime'):
                        pub_time = time_tag['datetime']
                    else:
                        pub_time = time_tag.get_text(strip=True)

                if link and title and not any(x['link'] == link for x in articles):
                    articles.append({
                        'title': title,
                        'link': link,
                        'published': pub_time
                    })

    # Filter and convert date to datetime object
    filtered = []
    for article in articles:
        pub_str = article.get('published')
        try:
            if pub_str:
                dt = parse_date(pub_str, fuzzy=True)
                if dt >= datetime(2022, 1, 1):
                    article['published'] = dt
                    filtered.append(article)
        except Exception as e:
            continue

    # Sort by latest first
    filtered.sort(key=lambda x: x['published'], reverse=True)
    return articles
