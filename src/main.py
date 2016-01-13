import tweepy, random

def main():
    CONSUMER_KEY = 'consumer_key'
    CONSUMER_SECRET = 'consumer_secret'
    ACCESS_KEY = 'access_key'
    ACCESS_SECRET = 'access_secret'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    typo_file = open('typos/typos.txt', 'r')
    typos = typo_file.read().split('\n')
    typo_file.close()

    word_results = []

    for line in typos:
        try:
            if line == "":
                continue

            split_line = line.split(' - ', 1)

            correct = split_line[0].strip();
            wrong_words = split_line[1].split(',')

            for wrong in wrong_words:
                word_results.append((wrong.strip(), correct))
        except:
            print "Failed to parse line: %s" % line
            pass

    wrong_word, correct_word = random.choice(word_results)

    wrong_tweets = api.search(wrong_word, lang="en", result_type="recent", count=1)

    correct_answers = [
        "Your tweet is wrong. It's actually spelt \"%s,\" not \"%s.\"" % (correct_word, wrong_word),
        "You know it's \"%s\" and not \"%s,\" right?" % (correct_word, wrong_word),
        "You're a little bit off in this tweet, though. It's \"%s\" and not \"%s.\"" % (correct_word, wrong_word),
        "Uhm, you know it is \"%s\" and not \"%s,\" right? :-)" % (correct_word, wrong_word)
    ]

    if not wrong_tweets:
        print "Empty, skipping"
    else:
        for wrong_tweet in wrong_tweets:
            screen_name = wrong_tweet.user.screen_name
            correct_tweet = ".@%s %s" % (screen_name, random.choice(correct_answers))
            api.update_status(status=correct_tweet, in_reply_to_status_id=wrong_tweet.id)
            print "Posted reply to the tweet with %s and the correct version of that was %s" % (wrong_word, correct_word)

if __name__ == '__main__':
    main()
