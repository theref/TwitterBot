from tweepy import OAuthHandler, Stream, StreamListener
import settings


products = ["XBT", "ETH", "EOS", "ADA"]


def parse_tweet(text):
    """Converts a tweet into data for making a trade.
    """
    if "Buy" in text:
        side = "Buy"
    else:
        side = "Sell"

    for p in products:
        if p in text:
            product = p
            break

    return {"side": side, "product": product}


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            text = status.text
            if "trigger" in text:
                data = parse_tweet(text)
                print(data)
        except Exception as e:
            # log exception
            pass

    def on_error(self, status_code):
        # print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        # print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


def main():
    listener = CustomStreamListener()
    auth = OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    stream = Stream(auth, listener)
    stream.filter(follow=["960163880768102400"])


if __name__ == "__main__":
    main()
