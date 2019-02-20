from parser import *

link = "data/labeled_corpus.tsv"


# Create counts of each relevant word being in a category
def create_counts(relevant_words, data):
    probs = {}
    tweets = open(data)

    for row in tweets:
        arr = row.rstrip().split("\t")

        tweet = clean_tweet(arr[0], emo_repl_order, emo_repl, re_repl)
        label = arr[1]

        for word in tweet.split():
            if word[0] == "#":
                word = word[1:]

            if word in relevant_words:
                if word not in probs:
                    # Initialize all counts to 0
                    probs[word] = [0, 0, 0, 0]

                # Increment the corresponding index by 1
                # Label won't be in labels if there is a formatting error in the tsv
                if label in labels:
                    probs[word][labels[label]] += 1

    tweets.close()

    return probs


# Convert counts to probabilities
def convert(probs):
    for (word, counts) in probs.items():
        total = sum(counts)

        for i in range(len(counts)):
            counts[i] = float(counts[i])/total


def main():
    relevant_words = generate_set(link)
    probs = create_counts(relevant_words, link)
    print(probs)
    convert(probs)
    print(probs)


if __name__ == "__main__":
    main()
