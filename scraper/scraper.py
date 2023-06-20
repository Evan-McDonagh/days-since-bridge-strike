import os
import dotenv
import requests
import bs4
from dataclasses import dataclass
from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

dotenv.load_dotenv()

URL = "https://nitter.it/IrishRail"
cred = credentials.Certificate(os.environ["FIREBASE_CONFIG"]);
firebase_admin.initialize_app(cred)
db = firestore.client()

@dataclass
class Tweet:
    link: str
    text: str
    time: datetime

    def is_bridge(self):
        return "bridge" in self.text.lower().split(" ")
    
    def to_dict(self):
        return {
            "link": self.link,
            "text": self.text,
            "time": self.time,
        }

def get_tweets() -> list[Tweet]:
    result = []
    page = requests.get(URL)
    soup = bs4.BeautifulSoup(page.text,"html.parser")
    items = soup.find_all(class_="timeline-item")
    for item in items:
        result += [create_tweet(item)]
    return result

def create_tweet(item: bs4.BeautifulSoup) -> Tweet:
    link = twitter_link(item.find(class_="tweet-link",href=True)["href"])
    text = item.find(class_="tweet-content media-body").text
    time = parse_time(item.find(class_="tweet-date").find("a")["title"])
    return Tweet(link,text,time)

def parse_time(time: str):
    return datetime.strptime(time,"%b %d, %Y · %I:%M %p %Z").astimezone(timezone.utc)

def get_first_bridge_tweet(tweets: list[Tweet]):
    for tweet in tweets:
        if tweet.is_bridge():
            return tweet
    return None

def twitter_link(href: str):
    return f"https://twitter.com{href}"

def get_last_bridge_strike():
    query = db.collection("tweets").order_by("time",direction=firestore.Query.DESCENDING).limit(1)
    for doc in query.stream():
        doc_dict = doc.to_dict()
        result = Tweet(doc_dict['link'],doc_dict['text'],doc_dict['time'])
        return result
    
def upload_bridge_strike(tweet: Tweet):
    db.collection("tweets").document().set(tweet.to_dict())
    

def main():
    tweets = get_tweets()
    latest = get_first_bridge_tweet(tweets)
    last = get_last_bridge_strike()
    print(latest.time.timestamp())
    print(last.time.timestamp())
    if latest.time.timestamp() > last.time.timestamp():
        upload_bridge_strike(latest)