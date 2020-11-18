from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS
import tweepy
import os
from queue import Queue
import threading

from twitter_oauth import TwitterOAuth


def get_userdata_worker(i, api, followers_data_list, followers_ids_list, queue):
    print("start")
    for user_data in api.lookup_users(user_ids=followers_ids_list[i:i+100]):
        followers_data_list.append({"user_name": user_data.name,
                                    "user_icon": user_data.profile_image_url_https,
                                    "status": user_data.statuses_count,
                                    "follower": user_data.followers_count,
                                    "friends": user_data.friends_count,
                                    "screen_name": user_data.screen_name})
    queue.get()
    queue.task_done()
    print("end")


    # print(followers_data_list)
app = Flask(__name__,
            static_folder="../Vue/dist/static",
            template_folder="../Vue/dist")

app.secret_key = os.urandom(12)
CORS(app)
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
oauth_callback = "https://neruneru-twitter-searcher.herokuapp.com/getapikey"
#oauth_callback = "http://127.0.0.1:8888/getapikey"
oauth_redirectURL = "/followersearch"
tw_oauth = TwitterOAuth(consumer_key, consumer_secret, oauth_callback)


@app.route("/oauth")
def oauth_app():
    global oauth_redirectURL
    tw_oauth.oauth()
    redirect_url = tw_oauth.get_authorization_url()
    oauth_redirectURL = request.values.get('redirectURL')
    return redirect(redirect_url)


@app.route("/setapikey")
def set_apikey():
    verifier = request.values.get('oauth_verifier')
    print(verifier)
    print(type(verifier))
    tw_oauth.set_access_token(verifier)
    return oauth_redirectURL


@app.route("/followerdata")
def get_follower():
    user_name = request.values.get('user_name')
    verifier = request.values.get('oauth_verifier')
    print(verifier)
    tw_oauth.oauth()
    tw_oauth.search_set_access_token(verifier)
    statuscode = 200
    api = tw_oauth.get_API(wait_on_rate_limit=True)
    followers_ids = tweepy.Cursor(
        api.followers_ids, screen_name=user_name, cursor=-1).items()
    followers_ids_list = []
    followers_data_list = []
    queue = Queue()

    try:
        for followers_id in followers_ids:
            followers_ids_list.append(followers_id)

        for i in range(0, len(followers_ids_list), 100):
            queue.put(i)
            thread = threading.Thread(target=get_userdata_worker,
                                      args=(i, api, followers_data_list, followers_ids_list, queue))
            thread.start()
        while True:
            if queue.empty():
                break
        print(len(followers_data_list))
    except tweepy.error.TweepError as e:
        print(e.response.status_code)
        followers_data_list = []
        statuscode = e.response.status_code
    return jsonify({"tw_data": followers_data_list}), statuscode


@app.route("/tweetdata")
def get_tweet():
    user_name = request.values.get('user_name')
    verifier = request.values.get('oauth_verifier')
    tw_oauth.oauth()
    tw_oauth.search_set_access_token(verifier)
    api = tw_oauth.get_API(wait_on_rate_limit=True)
    statuscode = 200
    if request.args.get('tweet_count'):
        tweet_count = int(request.args.get('tweet_count'))
    else:
        tweet_count = 200
    if request.args.get('search_word'):
        search_word = request.args.get('search_word')
    else:
        search_word = None
    followers_timeline = tweepy.Cursor(api.user_timeline,
                                       screen_name=user_name,
                                       cursor=-1,
                                       include_rts=False,
                                       exclude_replies=False).items()
    tweet_list = []
    try:
        for followers_tweet in followers_timeline:
            if (not search_word) or search_word in followers_tweet.text:
                tweet_list.append({"tweet": followers_tweet.text,
                                   "retweet_count": followers_tweet.retweet_count,
                                   "favorite_count": followers_tweet.favorite_count,
                                   "user_icon": followers_tweet.user.profile_image_url_https,
                                   "user_name": followers_tweet.user.name,
                                   "screen_name": followers_tweet.user.screen_name,
                                   "created_at": followers_tweet.created_at})
            if len(tweet_list) == tweet_count:
                break
    except tweepy.error.TweepError as e:
        print(e.response.status_code)
        statuscode = e.response.status_code
    return jsonify({"tw_data": tweet_list}), statuscode


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")


if __name__ == "__main__":
    #app.run(debug=True, host='127.0.0.1', port=8888)
    app.run(debug=True, host='0.0.0.0', port=80)
