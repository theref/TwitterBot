import sys
import tweepy
import webbrowser
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener

Q = sys.argv[1:] 
auth = OAuthHandler(config.API_KEY, config.API_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)


class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        
        # We'll simply print some values in a tab-delimited format
        # suitable for capturing to a flat file but you could opt 
        # store them elsewhere, retweet select statuses, etc.



        try:
            print "%s\t%s\t%s\t%s" % (status.text, 
                                      status.author.screen_name, 
                                      status.created_at, 
                                      status.source,)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# Create a streaming API and set a timeout value of 60 seconds.

streaming_api = Stream(auth, CustomStreamListener(), timeout=60)

# Optionally filter the statuses you want to track by providing a list
# of users to "follow".

print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)

streaming_api.filter(follow=None, track=Q)