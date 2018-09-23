from tweepy import OAuthHandler, Stream, StreamListener
import daiquiri
import logging
import settings

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger()
products = settings.products


def parse_tweet(text):
    """Converts a tweet into data for making a trade.
    """
    if "Buy" in text:
        side = "Buy"
    elif "Sell" in text:
        side = "Sell"
    else:
        return False

    product = False
    for p in products:
        if p in text:
            product = p
            break

    if product:
        return {"side": side, "product": product}
    else:
        return False


class CustomStreamListener(StreamListener):
    def on_status(self, status):
        try:
            text = status.text
            if "trigger" in text:
                data = parse_tweet(text)
                if data:
                    logger.info(
                        f"Received tweet: {data['side']} {data['product']}"
                    )
                else:
                    logger.warning(f"Could not parse tweet: {text}")
        except Exception as e:
            logger.error(e)

    def on_error(self, status_code):
        logger.error(f"Encountered error with status code: {status_code}")
        return True  # Don't kill the stream

    def on_timeout(self):
        logger.warning("Timeout")
        return True  # Don't kill the stream


def build_stream():
    listener = CustomStreamListener()
    auth = OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET)
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    stream = Stream(auth, listener)
    return stream


def main():
    stream = build_stream()
    stream.filter(follow=["960163880768102400"])


if __name__ == "__main__":
    main()
