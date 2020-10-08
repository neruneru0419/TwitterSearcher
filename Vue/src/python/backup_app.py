from flask import Flask,redirect, request, jsonify, render_template
from flask_cors import CORS
import tweepy
import ast
import threading
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)
consumer_key = "tCTqrsqbW5ZbvuS2dP0GIMf3X"
consumer_secret = "UsHI1qAN4TkeewaBEhtN8kvR8Lxt3VcCVQNo55C9fB0ZlqJFrn"
oauth_callback = "http://127.0.0.1:8888/getapikey"
auth = ""


@app.route("/oauth")
def oauth_app():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, oauth_callback)
    #try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    return redirect(redirect_url)
    # except tweepy.TweepError:
    #     error_msg = 'Error! Failed to get request token'
    #     print(error_msg)
    #     return redirect(backup_redirect_url)

    
@app.route("/getapikey")
def get_api_key():
    verifier = request.values.get('oauth_verifier')
    auth.get_access_token(verifier)
    key = auth.access_token
    secret = auth.access_token_secret
    auth.set_access_token(key, secret)
    return redirect("http://127.0.0.1:8080/followersearch")

@app.route("/get_timeline")

def get_timeline():
    api = tweepy.API(auth)
    for status in api.home_timeline():
        #見映えのため区切る
        print('-------------------------------------------')
        #ユーザ名表示
        print('name:' + status.user.name)
        #内容表示
        print(status.text)
    return str(api.home_timeline())
def get_tweet_information_by_parallel(i, api, followers_data_list, followers_ids_list):
    print("start")
    for i in api.lookup_users(user_ids=followers_ids_list[i:i+100]):
        followers_data_list.append({"user_name": i.name,
                                    "user_icon": i.profile_image_url_https,
                                    "status": i.statuses_count,
                                    "follower": i.followers_count,
                                    "friends": i.friends_count})
    print("end")
    #print(followers_data_list)
@app.route("/followerdata")
def get_follower():
    user_name = request.args.get('user_name')
    api = tweepy.API(auth,wait_on_rate_limit = True)
    followers_ids = tweepy.Cursor(api.followers_ids, screen_name = user_name, cursor = -1).items()
    followers_ids_list = []
    followers_data_list = []
    tw_error = {}
    threads = []
    try:
        for followers_id in followers_ids:
            followers_ids_list.append(followers_id)
            #print(followers_ids_list)
        for i in range(0, len(followers_ids_list), 100):
            threads.append(threading.Thread(target=get_tweet_information_by_parallel, args=(i,api,followers_data_list,followers_ids_list)))
        for i in threads:
            i.start()
        while True:
            print(threading.active_count())
            if threading.active_count() == 3:
                break
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
    api = tweepy.API(auth,wait_on_rate_limit = True)
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