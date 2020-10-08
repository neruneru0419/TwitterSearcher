from flask import Flask,redirect, request, jsonify, render_template
from flask_cors import CORS
import tweepy
import ast
import os
from queue import Queue
import threading

class TwitterAuth():
    def __init__(self, ck, cs, oc):
        self.consumer_key = ck
        self.consumer_secret = cs
        self.oauth_callback = oc
        self.auth = ""
    def oauth(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.oauth_callback)
    def get_authorization_url(self):
        redirect_url = self.auth.get_authorization_url()
        return redirect_url
    def set_access_token(self, verifier):
        self.auth.get_access_token(verifier)
        key = self.auth.access_token
        secret = self.auth.access_token_secret
        self.auth.set_access_token(key, secret)
    def get_API(self, wait_on_rate_limit = False):
        return tweepy.API(self.auth)


def get_tweet_worker(i, api, followers_data_list, followers_ids_list, queue):
    print("start")
    for i in api.lookup_users(user_ids=followers_ids_list[i:i+100]):
        followers_data_list.append({"user_name": i.name,
                                    "user_icon": i.profile_image_url_https,
                                    "status": i.statuses_count,
                                    "follower": i.followers_count,
                                    "friends": i.friends_count})
    queue.get()
    queue.task_done()
    print("end")
    
    #print(followers_data_list)
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
oauth_callback = "http://127.0.0.1:8888/getapikey"
twitter_auth = TwitterAuth(consumer_key, consumer_secret, oauth_callback)

@app.route("/oauth")
def oauth_app():
    twitter_auth.oauth()
    redirect_url = twitter_auth.get_authorization_url()
    print(redirect_url)
    return redirect(redirect_url)

@app.route("/getapikey")
def get_api_key():
    verifier = request.values.get('oauth_verifier')
    twitter_auth.set_access_token(verifier)
    return redirect("http://127.0.0.1:8080/followersearch")



@app.route("/followerdata")
def get_follower():
    user_name = request.args.get('user_name')
    api = twitter_auth.get_API(wait_on_rate_limit = True)
    followers_ids = tweepy.Cursor(api.followers_ids, screen_name = user_name, cursor = -1).items()
    followers_ids_list = []
    followers_data_list = []
    tw_error = {}
    queue = Queue()
    try:
        for followers_id in followers_ids:
            followers_ids_list.append(followers_id)
        for i in range(0, len(followers_ids_list), 100):
            queue.put(i)
            thread = threading.Thread(target=get_tweet_worker, 
                                            args=(i,api,followers_data_list,followers_ids_list, queue))
            thread.start()
        while True:
            if queue.empty():
                break
        print(len(followers_data_list))
    except tweepy.error.TweepError as e:
        print (type(e.reason))
        tw_error = ast.literal_eval(e.reason)
        print(tw_error)
        print(type(tw_error))
    if tw_error:
        return jsonify({"tw_data": tw_error})
    else:
        return jsonify({"tw_data": followers_data_list})

@app.route("/tweetdata")
def get_tweet():
    api = twitter_auth.get_API(wait_on_rate_limit=True)
    user_name = request.args.get('user_name')
    if request.args.get('tweet_count'):
        tweet_count = int(request.args.get('tweet_count'))
    else:
        tweet_count = 200
    if request.args.get('search_word'):
        search_word = request.args.get('search_word')
    else:
        search_word = None
    print(type(user_name))
    print(type(tweet_count))
    followers_timeline = tweepy.Cursor(api.user_timeline,
                                        include_rts = True,
                                        screen_name = user_name,
                                        cursor = -1).items()
    tweet_list = []
    try:
        for followers_tweet in followers_timeline:
            if (not search_word) or (search_word in followers_tweet.text):
                tweet_list.append({"tweet": followers_tweet.text})
            #print(len(tweet_list))
            if len(tweet_list) == tweet_count:
                break
    except tweepy.error.TweepError as e:
        print (e.reason)


    return jsonify({"tw_data": tweet_list})

def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8888)