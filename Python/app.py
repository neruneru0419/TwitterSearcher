from flask import Flask,redirect, request, jsonify, render_template
from flask_cors import CORS
import tweepy
import ast
import os
from queue import Queue
import threading

from twitter_oauth import TwitterOAuth



def get_userdata_worker(i, api, followers_data_list, followers_ids_list, queue):
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
            static_folder = "../Vue/dist/static",
            template_folder = "../Vue/dist")

app.secret_key = os.urandom(12)
CORS(app)
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
oauth_callback = "https://neruneru-twirrer-searcher.herokuapp.com/getapikey"
tw_oauth = TwitterOAuth(consumer_key, consumer_secret, oauth_callback)
@app.route("/oauth")
def oauth_app():
    tw_oauth.oauth()
    redirect_url = tw_oauth.get_authorization_url()
    print(redirect_url)
    return redirect(redirect_url)

@app.route("/setapikey")
def set_apikey():
    verifier = request.values.get('oauth_verifier')
    tw_oauth.set_access_token(verifier)

@app.route("/followerdata")
def get_follower():
    user_name = request.values.get('user_name')
    verifier = request.values.get('oauth_verifier')
    print(verifier)
    tw_oauth.oauth()
    tw_oauth.search_set_access_token(verifier)

    api = tw_oauth.get_API(wait_on_rate_limit = True)
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
            thread = threading.Thread(target=get_userdata_worker, 
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
        return jsonify({"tw_data": followers_data_list[0:100]})

@app.route("/tweetdata")
def get_tweet():
    user_name = request.values.get('user_name')
    verifier = request.values.get('oauth_verifier')
    tw_oauth.oauth()
    tw_oauth.search_set_access_token(verifier)

    api = tw_oauth.get_API(wait_on_rate_limit=True)
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
                tweet_list.append({"tweet": followers_tweet.text,
                                   "retweet_count": followers_tweet.retweet_count,
                                   "favorite_count": followers_tweet.favorite_count})
            if len(tweet_list) == tweet_count:
                break
    except tweepy.error.TweepError as e:
        print (e.reason)


    return jsonify({"tw_data": tweet_list})
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)