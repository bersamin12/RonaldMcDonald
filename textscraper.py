import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    # Send HTTP request to the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article title (usually in h1 tags)
        title = soup.find('h1').get_text().strip() if soup.find('h1') else "Title not found"

        # Extract article content
        # This part varies greatly depending on the website structure
        # Common approaches:

        # Option 1: Look for article or main content div (common patterns)
        article_content = ""
        article_div = soup.find('article') or soup.find('div', class_='article-content') or soup.find('div', class_='content') or soup.find('main')

        if article_div:
            # Get all paragraphs in the article div
            paragraphs = article_div.find_all('p')
            article_content = '\n\n'.join([p.get_text().strip() for p in paragraphs])
        else:
            # Option 2: If no clear article div, get all paragraphs in the body
            paragraphs = soup.find_all('p')
            article_content = '\n\n'.join([p.get_text().strip() for p in paragraphs])

        return {
            'title': title,
            'content': article_content
        }

        # then call the AI search engine from here
    else:
        return {
            'error': f"Failed to retrieve the webpage. Status code: {response.status_code}"
        }

# Example usage
# url = "https://finance.yahoo.com/news/tsmc-considers-running-intel-us-190303431.html"
# article_data = scrape_article(url)
# print(f"Title: {article_data.get('title', 'N/A')}")
# print("\nContent:")
# print(article_data.get('content', 'Content not found'))
