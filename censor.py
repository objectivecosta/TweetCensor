import csv
import json
import sys
from datetime import datetime
from credentials import api

input_file = open("tweet.js").read()
input_file = input_file.replace("window.YTD.tweet.part0 = ", "")
input_file = json.loads(input_file)

words = []
tweets_to_censor = []

before_date = None
retweets_only = False
dry_run = False

skip_next_argument = False
spare_like_count = 4_000_000_000
spare_retweet_count = 4_000_000_000
below_id = None

arguments = sys.argv[1:]
for (index, argument) in enumerate(arguments):
    if skip_next_argument:
        skip_next_argument = False
        continue

    if "--before" == argument:
        date_str = arguments[index + 1]
        before_date = datetime.strptime(date_str, "%Y-%m-%d")
        skip_next_argument = True
    elif "--retweets" == argument:
        retweets_only = True
    elif "--dry-run" == argument:
        dry_run = True
    elif "--spare-with-likes" == argument:
        count_str = arguments[index + 1]
        spare_like_count = int(count_str)
        skip_next_argument = True
    elif "--spare-with-retweets" == argument:
        count_str = arguments[index + 1]
        spare_retweet_count = int(count_str)
        skip_next_argument = True
    elif "--below_id" == argument:
        below_id = arguments[index + 1]
        skip_next_argument = True
    else:
        words.append(argument.lower())

print("""Properties:

Below ID: {};

Before: {};
Retweets Only: {};
Dry Run: {};

Spare if has at least {} likes;
(or)
Spare if has at least {} retweets;

Words: {};
""".format(below_id, before_date, retweets_only, dry_run, spare_like_count, spare_retweet_count, ",".join(words)))

exit()

for tweet in input_file:
    text = tweet["full_text"].lower()
    for word in words:
        if word in text:
            tweet_id = tweet["id"]
            if below_id is not None and tweet_id < below_id:
                tweets_to_censor.append(tweet_id)
            elif below_id is None:
                tweets_to_censor.append(tweet_id)

print("Tweets to censor: {}".format(len(tweets_to_censor)))

print("")
print("This will delete {} tweets. Do you want to continue?".format(len(tweets_to_censor)), end = '')
variable = input(" [Y/n]\n")

if variable == "Y":
    for tweet_id in tweets_to_censor:
        print("Deleting tweet with ID: {}".format(tweet_id))

        if dry_run == True:
            print("[DRY RUN] Would have deleted {}, but didn't because --dry-run".format(tweet_id))
        else:
            try:
                api.DestroyStatus(tweet_id)
            except:
                print("Failed to delete {}".format(tweet_id))

print("Deleted {} tweets".format(len(tweets_to_censor)))
