import csv
import sys
from credentials import api

input_file = csv.DictReader(open("tweets.csv"))

words = []
tweets_to_censor = []

for argument in sys.argv[1:]:
    words.append(argument.lower())

print("Word count: {}".format(len(words)))

for tweet in input_file:
    text = tweet["text"].lower()
    for word in words:
        if word in text:
            tweets_to_censor.append(tweet["tweet_id"])

print("Tweets to censor: {}".format(len(tweets_to_censor)))

print("")
print("This will delete {} tweets. Do you want to continue?".format(len(tweets_to_censor)), end = '')
variable = input(" [Y/n]\n")

if variable == "Y":
    for tweet_id in tweets_to_censor:
        print("Deleting tweet with ID: {}".format(tweet_id))
        try:
            api.DestroyStatus(tweet_id)
        except:
            print("Failed to delete {}".format(tweet_id))

print("Deleted {} tweets".format(len(tweets_to_censor)))
