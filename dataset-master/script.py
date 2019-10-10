import tweepy
import time
import db

consumer_key = 'CHIGwr0G6BuTtyeXr0EB2NvrT'
consumer_secret = 'mAnVx1sPebBBNttE8zzHyyHGkuP6rmJSkbCbjjGJXrL3Wj24YJ'
token_key = '873261601641639936-2Cl8Ir1PPcBSDFZcRAIbki990mxyNpx'
token_secret = '0k7nU6BWtPHJMlHtUBaTNdl4qlLpxRSduUlqVIUw3Gnpk'


def download_tweets(id_file, sentiment):
    with open(id_file) as infile:
        for tweet_id in infile:
            tweet_id = tweet_id.strip()

            if db.exist_tweet(tweet_id):
                print("tweet com id: ", tweet_id, "já foi capturado")
                continue

            try:
                tweet = api.get_status(tweet_id)
                db.add_tweet(tweet, sentiment)
            except tweepy.error.TweepError:
                print("tweet com id: ", tweet_id, "não está disponível")

            time.sleep(1)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token_key, token_secret)
api = tweepy.API(auth)


print("Capturando tweets negativos ...")
download_tweets("negativos.txt", 0)

print("Capturando tweets positivos ...")
download_tweets("positivos.txt", 1)


print("Fim.")
