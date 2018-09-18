#%%
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener

listener = StreamListener()
auth = OAuthHandler(config.API_KEY, config.API_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
stream = Stream(auth, listener)
stream.filter(follow=['3511430425'])