from twitter_specials import *


# Remove # and ignore @
def special(tweet):
    new = ""

    for word in tweet.split():
        if word[0] == "#":
            word = word[1:]
        elif word[0] == "@":
            continue

        new += word + " "

    return new[:-1]


# Returns a set of relevant words from a tweet
def get_set(tweet, relevant_words):
    tweet = special(clean_tweet(tweet, emo_repl_order, emo_repl, re_repl))
    words = set()

    for word in tweet.split():
        if word in relevant_words:
            words.add(word)

    return words


# Generate a set of words with frequency >= 2
def generate_set(data):
    word_dict = {}
    relevant_words = set()
    tweets = open(data)

    for row in tweets:
        arr = row.split("   ")

        tweet = clean_tweet(arr[0], emo_repl_order, emo_repl, re_repl)

        for word in tweet.split():
            if word[0] == "#":
                word = word[1:]

            if "@" not in word:
                if word not in word_dict:
                    word_dict[word] = 0

                word_dict[word] += 1

    # Iterate over dictionary and add to the set everything with frequency >= 2
    for (word, freq) in word_dict.items():
        if freq >= 2 and word != '':
            relevant_words.add(word)

    return relevant_words


if __name__ == "__main__":
    relevant = generate_set("data/labeled_corpus.tsv")
    print(relevant)
    print(get_set("#hello all these #words are relevant except for relevant", relevant))