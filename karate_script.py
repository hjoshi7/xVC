import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABWntQEAAAAAr42yuB39zQps00N6zj%2FyXhK726I%3DVQltH4eved81DnRoaZ4ORVVY77WX78bxqnlVHeAOfS8gXLfB6j"
maxrequests = 10
def get_user_id(username):
    endpoint = "https://api.twitter.com/2/users/by/username/" + username
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        user_id = response.json()["data"]["id"]
        return user_id
    else:
        print(f"Error getting user ID: {response.status_code} - {response.text}")
        return None

username = "getkarate"
user_id = get_user_id(username)

if user_id:
    endpoint = "https://api.twitter.com/2/users"
    params = {
        "ids": user_id,
        "user.fields": "created_at,public_metrics,most_recent_tweet_id"
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(endpoint, params=params, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

""" def get_user_tweets(user_id):
    endpoint = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "tweet.fields": "public_metrics"
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(endpoint, params=params, headers=headers)
    if response.status_code == 200:
        tweets = response.json()
        return tweets
    else:
        print(f"Error getting user tweets: {response.status_code} - {response.text}")
        return None """

def get_user_tweets(user_id):
    endpoint = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "tweet.fields": "public_metrics,created_at",
        "max_results": 100
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    all_tweets = []

    while len(all_tweets) < maxrequests:
        response = requests.get(endpoint, params=params, headers=headers)
        if response.status_code == 200:
            tweets = response.json()
            if "data" in tweets:
                all_tweets.extend(tweets["data"])
            else:
                break
            if "meta" in tweets and "next_token" in tweets["meta"]:
                params["pagination_token"] = tweets["meta"]["next_token"]
            else:
                break
        else:
            print(f"Error getting user tweets: {response.status_code} - {response.text}")
            break

    return all_tweets


if user_id:
    tweets = get_user_tweets(user_id)
    if tweets:
        print("User Tweets:")
        print("-------------")
        for tweet in tweets:
            print(tweet)
    else:
        print("Error fetching tweets.")
else:
    print("Error fetching user ID.")

def get_mentions(user_id):
    endpoint = f"https://api.twitter.com/2/users/{user_id}/mentions"
    params = {
        "tweet.fields": "public_metrics,author_id,created_at"
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(endpoint, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error getting mentions: {response.status_code} - {response.text}")
        return None

def get_followers_count(user_id):
    endpoint = f"https://api.twitter.com/2/users/{user_id}"
    params = {
        "user.fields": "public_metrics"
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.get(endpoint, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["public_metrics"]["followers_count"]
    else:
        print(f"Error getting followers count: {response.status_code} - {response.text}")
        return None

if user_id:
    mentions = get_mentions(user_id)
    if mentions:
        print(f"Tweets mentioning @{username}:")
        for mention in mentions:
            author_id = mention['author_id']
            followers_count = get_followers_count(author_id)
            print(mention)
            print("Followers",followers_count)
    else:
        print("Error fetching mentions.")
else:
    print("Error fetching user ID.")