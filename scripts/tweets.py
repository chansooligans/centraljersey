import requests
import base64

# replace with your Twitter API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"

# encode the consumer key and secret
bearer_token = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

# request the bearer token
r = requests.post(
    "https://api.twitter.com/oauth2/token",
    headers={
        "Authorization": f"Basic {bearer_token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    },
    data={
        "grant_type": "client_credentials"
    }
)

# extract the bearer token from the response
access_token = r.json()["access_token"]

# define the latitude and longitude
latitude = 37.788022
longitude = -122.399797

# search for tweets near the latitude and longitude
r = requests.get(
    "https://api.twitter.com/1.1/search/tweets.json",
    headers={
        "Authorization": f"Bearer {access_token}"
    },
    params={
        "geocode": f"{latitude},{longitude},1km",
        "tweet_mode": "extended",
        "count": 100
    }
)

# print the text of the tweets
for tweet in r.json()["statuses"]:
    print(tweet["full_text"])
