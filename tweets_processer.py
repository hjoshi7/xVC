from flask import Flask
from markupsafe import escape
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import requests
import json
import scipy
import nltk
from datetime import datetime as DT
import calendar, datetime, time
from scipy.ndimage import uniform_filter1d
from flask_cors import CORS

import asyncio
import sys
import xai_sdk
import os

os.environ['XAI_API_KEY'] = "Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ"


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/profile/<handle>/')
def get_metadata(handle):

    url = f"https://api.twitter.com/2/users/by/username/{escape(handle)}/?user.fields=id,name,description,location,profile_image_url,public_metrics"

    # payload = {'user.fields': 'id,name,description,location,profile_image_url,public_metrics'}
    headers = {
        # 'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFaftQEAAAAAH2lZuiXgXWWnuy5waKE6wVwJ3KU%3DGnjCvp9nSdoVGFPGPSJE1oamZekzpXuHjfTW6xki5smQPrRx9F',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFaftQEAAAAAUr3EGxh5WaOzfmsX5ENeRBF1NEE%3D4eJgcXrXpW6jivcaFztpRFOHwfT6ZQqF7aqoeA1T6gssOwVwba',
        'Cookie': 'guest_id=v1%3A171365002967644094; guest_id_ads=v1%3A171365002967644094; guest_id_marketing=v1%3A171365002967644094; personalization_id="v1_cV6az1AN3jp0p6es5D/QRg=="'
    }

    response = requests.request("GET", url, headers=headers)
    return response.json()


@app.route('/data/<handle>/')
def process_tweets(handle):
    username = escape(handle)
    tweets = return_tweets(username)
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFaftQEAAAAAH2lZuiXgXWWnuy5waKE6wVwJ3KU%3DGnjCvp9nSdoVGFPGPSJE1oamZekzpXuHjfTW6xki5smQPrRx9F"

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

    user_id = get_user_id(username)
    mentions = get_mentions(user_id)
    data = extract_numpy_data(tweets)
    mentions_data = extract_numpy_data(mentions)

    scores = geometric_mean(data)
    mentions_scores = geometric_mean(mentions_data)

    final_data = np.concatenate((data, mentions_data), axis=0)
    final_data = final_data[final_data[:, 0].argsort()]

    final_scores = geometric_mean(final_data)

    start_index = (final_data[:, 4]!=0).argmax()

    moving_average = uniform_filter1d(final_scores[start_index:], size=50)

    top_mention_ids = [mention["id"] for mention in get_top_tweets(mentions)]

    desc = get_description(tweets, handle)
    times = []

    for timestamp in final_data[start_index:, 0]:
        date = datetime.datetime.fromtimestamp(timestamp)
        # date = date[4:11] + date[-4:]
        date = date.strftime("%Y-%m-%d")
        times.append(date)

    counts_data = return_final_counts_data(username)
    return [times, moving_average[:].tolist(), top_mention_ids, desc, counts_data[0], counts_data[1].tolist()]

def return_final_counts_data(username):
    def return_counts(username):
        counts = []
        next_token = None
        while True:
            url = f"https://api.twitter.com/2/tweets/counts/all?query=@{username}&granularity=day&start_time=2022-01-01T00:00:00Z"
            params = {
            #     "query": f"from:{username} -is:retweet",
            #     "start_time": "2016-01-01T00:00:00Z",
            #     "tweet.fields": "public_metrics,created_at",
            #     "max_results": 500
            }
            if next_token:
                params["next_token"] = next_token

            headers = {
                'Authorization': f'Bearer AAAAAAAAAAAAAAAAAAAAAFaftQEAAAAAH2lZuiXgXWWnuy5waKE6wVwJ3KU%3DGnjCvp9nSdoVGFPGPSJE1oamZekzpXuHjfTW6xki5smQPrRx9F',
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                counts.extend(data["data"])
                if "meta" in data and "next_token" in data["meta"]:
                    next_token = data["meta"]["next_token"]
                else:
                    break
            else:
                print(f"Error: {response.status_code} - {response.text}")
                break
        return counts
    
    counts = return_counts(username)
    # print(counts)
    def process_counts_time(counts):
        num_counts = [count['tweet_count'] for count in counts]
        num_counts = np.array(num_counts)

        utc_dts = [tweet['end'].replace("Z","UTC") for tweet in counts]
        dts = [DT.strptime(utc_dt, "%Y-%m-%dT%H:%M:%S.%f%Z") for utc_dt in utc_dts]
        epochs = np.array([calendar.timegm(dt.utctimetuple()) for dt in dts])
        num_counts = num_counts[np.argsort(epochs)]
        epochs = epochs[np.argsort(epochs)]
        times = []
        for timestamp in epochs:
            date = datetime.datetime.fromtimestamp(timestamp)
            date = date.strftime("%Y-%m-%d")
            times.append(date)
        
        
        moving_average = uniform_filter1d(num_counts, size=20)
        return (times, moving_average)
    
    data = process_counts_time(counts)

    return (data[0], data[1].cumsum())




def get_description(tweets, handle):
    user_data = get_metadata(handle)["data"]
    company, bio = user_data["name"], user_data["description"]
    top_tweets_text = [tweet["text"] for tweet in get_top_tweets(tweets)]

    text = "#Company" + "\n" + company + "\n"
    text += "#Bio"  + "\n" + bio + "\n"
    for i in range(5):
        if i >= len(top_tweets_text):
            break
        text += f"#Tweet {i}" + "\n" + top_tweets_text[i]
    desc = []
    async def main():
        client = xai_sdk.Client()
        sampler = client.sampler

        PREAMBLE = """\
Fill in a comprehensive but informative description of a startup based on Tweets and Bio. Use an unbiased and journalistic tone. Combine information from Tweets and Bio together into a coherent answer. DO NOT repeat text. DO NOT use any emojis. The first word of your description should be the company name.

Human:
#Company
Artisan AI
#Bio 
AI Employees called Artisans and consolidated SaaS for them and humans to work together in. Hire Ava to 10x your BDRs & AEs productivity. @ycombinator 🧑‍🎨
#Tweet 0
A new era is upon us, with AI employees and humans working in symbiosis.

We've just released Ava, The Sales Rep Artisan. She's an AI BDR on steroids, and she's available to hire now.

The best part? Manage everything by chatting to her.

Learn more: https://artisan.co/ava-sales-rep/
#Tweet 1
More functional, beautiful & automated - meet V2 of Artisan Sales: https://youtu.be/w7pQ386j2ls
#Tweet 2
We're Artisan AI, and we are creating the next generation of digital workers, called Artisans, who look and act like human colleagues.
This is the next Industrial Revolution.
This is Artisan.
#Tweet 3
We just launched on @ycombinator's Launch YC!

Ava, The Sales Rep Artisan is an AI employee that works alongside your human sales team, and she's the world's fastest BDR, pouring rocket fuel on your PMF.

Check us out:
#Tweet 4
A new era is upon us, with AI employees and humans working in symbiosis.

We've just released Ava, The Sales Rep Artisan. She's an AI BDR on steroids, and she's available to hire now.

The best part? Manage everything by chatting to her.

Learn more: https://artisan.co/ava-sales-rep/<|separator|>

Assistant:
#DESCRIPTION
Artisan AI creates digital workers, called Artisans. The company's first Artisan, Ava, automates the entire outbound sales process and can be set up with a 10-minute conversation. Ava creates TCPs, and prospects with her database of over 270,000,000 contacts, crafts and sends highly bespoke email sequences, and books meetings into the user's calendar. The user can manage all features and settings by talking to Ava via Slack.<|separator|>

Human:
#Company
Yubo
#Bio
Here when we're not live
#Tweet 0
Discover how Yubo, the live social discovery app, is revolutionizing social media for Gen Z in 2023! With 99% of its users belonging to Gen Z, Yubo offers a refreshing take on online connection without likes or follows.

Read more about its impact on Gen Z's socializing habits and its commitment to safety and innovation. #Yubo #GenZ #SocialMediaRevolution

https://businesscasestudies.co.uk/yubo-and-gen-zs-social-media-usage-in-2023/
#Tweet 1
“Yubo, a live social discovery platform, is a major player in this Gen Z social media arena. The company prioritizes online user safety.” It's not us saying it, it's @EGTmedia

Thank you for this article outlining our efforts to make the internet safer and anti-bullying initiatives.

It also highlights the invaluable work of @Alexholmes through the Diana Award and our Safety Board.

https://eglobaltravelmedia.com.au/2024/02/19/major-social-platform-yubo-strongly-supports-safer-internet-day-and-anti-bullying-initiatives/…

#Yubo #OnlineSafety #SaferInternetDay #SafetyBoard
#Tweet 2
Exploring Yubo: The ultimate app for Gen Z to connect with new friends worldwide! Don’t worry about likes or followers - just be yourself and make authentic connections. Discover how it works, and what it's all about

#Yubo #GenZ #YuboPeople
Tweet 3
Yubo is a digital playground where young people can showcase their creativity through cool challenges and fun filters. 

Join the digital celebration on Yubo as we transform screens into dynamic windows of connection
Let's set the stage for a positive 2024!

Read more on the Yubo blog: https://yubo.live/blog/yubo-rolling-into-2024-with-the-gen-z…

#NewYear #GenZ #YuboVibes #Yubo
#Tweet 4
To kick-off this takeover, @SachaLaz  Yubo's co-founder, is sharing his podcast with Thomas for @40nuancesdeNext !

A big thank you to Thomas for this enriching experience.

https://linkedin.com/posts/thomasbenzazon_107-la-plateforme-sociale-de-la-gen-z-qui-activity-7138467231184670720-by7S?utm_source=share&utm_medium=member_desktop…

#YuboTakeover #40ShadesOfNext #PodcastTime<|separator|>

Assistant:
#DESCRIPTION
Yubo, the social platform where Generation Z creates communities of friends around the world. Yubo lets users create live video discussion spaces where both streamers and viewers interact through a live chat. Relying on cutting-edge technology and tools specifically designed to protect the app users, Yubo provides a secure discussion platform built to widen their circle of friends. The social network favors sociability, sharing, and authenticity rather than the approval mechanisms and influencers systems of traditional social networks.
"""
        prompt = PREAMBLE + f"\nHuman: \n{text}<|separator|>\n\nAssistant:#DESCRIPTION"
        # print(prompt)
        async for token in sampler.sample(
            prompt=prompt,
            max_len=1024,
            stop_tokens=["<|separator|>"],
            temperature=0.8,
            nucleus_p=0.95):
            desc.append(token.token_str)

    asyncio.run(main())
    return "".join(desc)

def get_top_tweets(tweets):
    impressions = np.array([item["public_metrics"]["impression_count"] for item in tweets])
    return [tweet for tweet in np.array(tweets)[np.argsort(impressions)[-5:]]] 


def geometric_mean(tweets):
    gmean = scipy.stats.mstats.gmean
    # weights = np.array([0.1, 0.3, 0.1, 0.5])
    # replies, likes, quote_count, impressions
    weights = np.array([0.1, 0.5, 0.1, 0.3])
    #weights = np.array([0.25, 0.25, 0.25, 0.25])
    # tweets[:, 4] = tweets[:, 4] / 10
    return gmean(tweets[:, 1:] + 1, axis=1, weights=weights)


def extract_numpy_data(tweets):
    data = np.zeros((len(tweets), 5))
    for i in range(len(tweets)):
        tmp = np.zeros(5)
        indices = {"reply_count" : 1, "like_count": 2, "quote_count": 3, "impression_count": 4}
        for metric in tweets[i]['public_metrics']:
            if metric in indices:
                tmp[indices[metric]] = tweets[i]['public_metrics'][metric]
        
        utc_dt = tweets[i]['created_at'].replace("Z","UTC")
        dt = DT.strptime(utc_dt, "%Y-%m-%dT%H:%M:%S.%f%Z")
        epoch = calendar.timegm(dt.utctimetuple())
        tmp[0] = epoch
        data[i] = tmp
    return data



def return_tweets(username):
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABWntQEAAAAAr42yuB39zQps00N6zj%2FyXhK726I%3DVQltH4eved81DnRoaZ4ORVVY77WX78bxqnlVHeAOfS8gXLfB6j"
    tweets = []

    next_token = None
    while True:
        url = f"https://api.twitter.com/2/tweets/search/all"
        params = {
            "query": f"from:{username} -is:retweet",
            "start_time": "2016-01-01T00:00:00Z",
            "tweet.fields": "public_metrics,created_at",
            "max_results": 500
        }
        if next_token:
            params["next_token"] = next_token

        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            tweets.extend(data["data"])
            if "meta" in data and "next_token" in data["meta"]:
                next_token = data["meta"]["next_token"]
            else:
                break
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

    print(f"Total tweets fetched: {len(tweets)}")
    return tweets

def get_mentions(user_id, max_results=100):
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABWntQEAAAAAr42yuB39zQps00N6zj%2FyXhK726I%3DVQltH4eved81DnRoaZ4ORVVY77WX78bxqnlVHeAOfS8gXLfB6j"
    endpoint = f"https://api.twitter.com/2/users/{user_id}/mentions"
    params = {
        "tweet.fields": "public_metrics,author_id,created_at",
        "user.fields": "username",
        "max_results": max_results
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    mentions = []
    next_token = None
    while True:
        if next_token:
            params["pagination_token"] = next_token
        response = requests.get(endpoint, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            mentions.extend(data)
            if "meta" in response.json() and "next_token" in response.json()["meta"]:
                next_token = response.json()["meta"]["next_token"]
            else:
                break
        else:
            print(f"Error getting mentions: {response.status_code} - {response.text}")
            return None

    return mentions


if __name__ == "__main__":
    app.run(port=8080)