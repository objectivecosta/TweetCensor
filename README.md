Create a file named `credentials.py`, as follows

```
import twitter

api = twitter.Api(consumer_key='<consumer_key>',
                  consumer_secret='<consumer_secret>',
                  access_token_key='<access_token>',
                  access_token_secret='<access_token_secret>')
```
                      
Download your Twitter archive and put the ~tweets.csv~ tweet.js file in the root of the project.

Select words to censor as follows:

`python censor.py [word1] [word2] ... [wordn]`

Confirm and voilà.

Cheers! ;)
