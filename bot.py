from sys import implementation
import tweepy
import logging
import time
import webscraper

# API code was taken from https://realpython.com/twitter-bot-python-tweepy/

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def create_apii():
    
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):

            emotion = [keyword in tweet.text.lower() for keyword in keywords]

            logger.info(f"Answering to {tweet.user.name}")

            quote = webscraper.get_quote(emotion[0])

            api.update_status(
                status=quote,
                in_reply_to_status_id=tweet.id,
            )
        else:

            logger.info(f"Answering to {tweet.user.name}")

            quote = webscraper.get_quote("Sad")

            api.update_status(
                status=quote,
                in_reply_to_status_id=tweet.id,
            )

    return new_since_id


def main():
    api = create_apii()
    since_id = 1
    emotions = ["sad", "happy", "angry", "surprise", "fear"]

    while True:
        since_id = check_mentions(api, emotions, since_id)
        logger.info("Waiting...")
        time.sleep(5)


if __name__ == "__main__":
    main()
