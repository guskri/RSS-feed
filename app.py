from flask import Flask, render_template, request
import feedparser  # For parsing RSS feeds
from bs4 import BeautifulSoup  # For stripping HTML tags
from urllib.parse import urlparse  # For parsing URLs
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# List of RSS feed URLs from various Norwegian news sources
RSS_FEEDS = [
    "https://www.nrk.no/toppsaker.rss",  # NRK Nyheter
    "https://www.vg.no/rss/feed",  # VG Forsiden
    "https://www.dagbladet.no/?lab_viewport=rss",  # Dagbladet
    "https://www.aftenposten.no/rss",  # Aftenposten
    "https://www.tv2.no/rss/nyheter",  # TV2 Nyheter
    "https://www.bt.no/rss",  # Bergens Tidende
    "https://www.adressa.no/rss",  # Adresseavisen
    "https://www.aftenbladet.no/rss",  # Stavanger Aftenblad
    "https://www.fvn.no/rss",  # Fædrelandsvennen
    "https://www.vl.no/rss",         # Vårt Land

]


@app.route('/')
def home():
    selected_sources = request.args.getlist('source')
    news = fetch_news_summaries(selected_sources)
    sources = list(set([extract_source(feed) for feed in RSS_FEEDS]))  # Get unique sources for checkboxes

    return render_template('index.html', news=news, sources=sources, selected_sources=selected_sources)

def fetch_news_summaries(selected_sources):
    all_news = []

    for feed_url in RSS_FEEDS:
        try:
            parsed_feed = feedparser.parse(feed_url)
            
            if parsed_feed.bozo:
                logging.warning(f"Failed to parse feed: {feed_url} - {parsed_feed.bozo_exception}")
                continue

            for entry in parsed_feed.entries[:5]:  # Fetch top 5 entries per feed
                source = extract_source(entry.link)
                
                if selected_sources and source not in selected_sources:
                    continue  # Skip articles that do not match the selected sources
                
                content = entry.get('summary') or entry.get('description') or "No summary available."
                clean_content = strip_html(content)
                truncated_content = truncate_text(clean_content, 200)
                image_url = extract_image(entry)

                all_news.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': truncated_content,
                    'image': image_url,
                    'source': source
                })
        
        except Exception as e:
            logging.error(f"Error processing feed {feed_url}: {e}")
            continue  # Skip to the next feed if there's an error
    # Shuffle the articles to create a random order
    random.shuffle(all_news)

    return all_news

def extract_image(entry):
    """
    Extract an image URL from the RSS feed entry.
    Checks for 'media:content', 'enclosure', or images embedded in 'description'.
    """
    # Check for media content or enclosure
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    elif 'media_thumbnail' in entry and len(entry.media_thumbnail) > 0:
        return entry.media_thumbnail[0]['url']
    elif 'enclosures' in entry and len(entry.enclosures) > 0:
        return entry.enclosures[0]['url']
    else:
        # Check for image in description
        if 'description' in entry:
            soup = BeautifulSoup(entry.description, "html.parser")
            img = soup.find('img')
            if img and 'src' in img.attrs:
                return img['src']
    return None  # Return None if no image is found

def strip_html(text):
    """
    Remove HTML tags from the provided text.
    """
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def truncate_text(text, max_length):
    """
    Truncate text to a specified maximum length, adding ellipsis if it exceeds.
    """
    if len(text) > max_length:
        return text[:max_length].rstrip() + '...'
    return text

def extract_source(url):
    """
    Extract the source website name from a URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
