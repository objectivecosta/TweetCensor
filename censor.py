import csv
import json
import sys
from datetime import datetime
from venv import create
from credentials import api

input_file = open("tweet.js").read()
input_file = input_file.replace("window.YTD.tweet.part0 = ", "")
input_file = json.loads(input_file)

words = []
tweets_to_censor = []

before_date = None
retweets_only = False
excl_retweets = False
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
    elif "--excl-retweets" == argument:
        excl_retweets = True
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
Excl. Retweets: {};
Dry Run: {};

Spare if has at least {} likes;
(or)
Spare if has at least {} retweets;

Words: {};
""".format(below_id, before_date, retweets_only, excl_retweets, dry_run, spare_like_count, spare_retweet_count, ",".join(words)))

for entry in input_file:
    tweet = entry["tweet"]

    like_count = int(tweet["favorite_count"])
    retweet_count = int(tweet["retweet_count"])

    text = tweet["full_text"].lower()
    created_at = datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
    tweet_id = tweet["id"]

    if like_count >= spare_like_count:
        print("Skipping tweet {} because it has enough likes!".format(tweet_id))
        continue

    if retweet_count >= spare_retweet_count:
        print("Skipping tweet {} because it has enough retweets!".format(tweet_id))
        continue

    if created_at > before_date:
        print("Skipping tweet {} because it made after {}!".format(tweet_id, before_date))
        continue

    if retweets_only == True and text.startswith("rt ") == False:
        print("Skipping tweet {} because it is NOT RT!".format(tweet_id))
        continue

    if excl_retweets == True and text.startswith("rt ") == True:
        print("Skipping tweet {} because it is RT!".format(tweet_id))
        continue
    
    if len(words) > 0:
        for word in words:
            if word in text:
                if below_id is not None and tweet_id < below_id:
                    tweets_to_censor.append(tweet_id)
                elif below_id is None:
                    tweets_to_censor.append(tweet_id)
    else:
        tweets_to_censor.append(tweet_id)

print("Tweets to censor: {}".format(len(tweets_to_censor)))

print("")
print("This will delete {} tweets. Do you want to continue?".format(len(tweets_to_censor)), end = '')
variable = input(" [Y/n]\n")

if variable == "Y":
    for tweet_id in tweets_to_censor:

        if dry_run == True:
            print("[DRY RUN] Would have deleted {}, but didn't because --dry-run".format(tweet_id))
        else:
            print("Deleting tweet with ID: {}".format(tweet_id))
            try:
                api.DestroyStatus(tweet_id)
            except:
                print("Failed to delete {}".format(tweet_id))
    print("Deleted {} tweets".format(len(tweets_to_censor)))
else:
    print("Operation cancelled")
