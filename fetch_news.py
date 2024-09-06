import requests

def fetch_news(api_key, country='no'):
    """
    Fetch news articles from the API.
    
    Args:
        api_key (str): API key for News API.
        country (str): Country code for the news source.
    
    Returns:
        list: List of news articles with title, description, url, and source.
    """
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return []

    articles = data.get('articles', [])

    news_data = [
        {
            'title': article['title'],
            'summary': article.get('description', 'No description available.'),
            'url': article['url'],
            'source': article['source']['name']
        }
        for article in articles
    ]

    return news_data
