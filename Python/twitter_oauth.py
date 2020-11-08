import tweepy
from account_data import AccountData


class TwitterOAuth():
    def __init__(self, ck: str, cs: str, oc: str):
        self.consumer_key = ck
        self.consumer_secret = cs
        self.oauth_callback = oc
        self.auth = ""

        self.account_data = AccountData("postgres")

    def oauth(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret, self.oauth_callback)

    def get_authorization_url(self) -> str:
        redirect_url = self.auth.get_authorization_url(
            signin_with_twitter=True)
        return redirect_url

    def set_access_token(self, verifier: str):
        self.auth.get_access_token(verifier)
        token = self.auth.access_token
        secret_token = self.auth.access_token_secret
        self.account_data.insert_verifier(verifier, token, secret_token)
        self.auth.set_access_token(token, secret_token)

    def search_set_access_token(self, verifier: str):
        account_data_list = self.account_data.select_verifier(verifier)
        print(account_data_list)
        token = account_data_list[1]
        secret_token = account_data_list[2]
        self.auth.set_access_token(token, secret_token)

    def get_API(self, wait_on_rate_limit=False) -> tweepy.API:
        return tweepy.API(self.auth)
