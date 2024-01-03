import os
import praw
import feedparser
import datetime


def lambda_handler(event, context):
    # Access the RSS Feed
    keyword = os.environ['YOUR_SEARCH_QUERY']
    articles = get_articles(keyword)

    # Post articles to Reddit
    if articles:
        post_to_reddit(articles)
        return {
            'statusCode': 200,
            'body': 'Articles posted to Reddit successfully.'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'No articles found for today.'
        }

def get_articles(keyword):
    feed = feedparser.parse('https://news.google.com/news/rss/search?q=' + keyword + '&hl=en')
    today = datetime.date.today()

    # Filtering articles for today's date
    filtered_articles = [{'title': entry.title, 'link': entry.link} for entry in feed.entries if parse_date(entry.published) == today]
    return filtered_articles

def parse_date(date_string):
    # Function to extract date from string
    return datetime.datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z").date()

def post_to_reddit(articles):
    reddit = praw.Reddit(
        client_id=os.environ['YOUR_CLIENT_ID'],
        client_secret=os.environ['YOUR_CLIENT_SECRET'],
        user_agent=os.environ['YOUR_USER_AGENT'],
        username=os.environ['YOUR_REDDIT_USERNAME'],
        password=os.environ['YOUR_REDDIT_PASSWORD']
    )

    subreddit = reddit.subreddit(os.environ['YOUR_SUBREDDIT_NAME'])
    for article in articles:
        subreddit.submit(title=article['title'], url=article['link'])
