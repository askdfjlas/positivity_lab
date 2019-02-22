from parser import *


# Create counts of each relevant word being in a category
def create_counts(relevant_words, data):
    probs = {}
    counts = [0, 0, 0, 0]
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

        if label in labels:
            counts[labels[label]] += 1

    tweets.close()

    return probs, counts


# Convert counts to probabilities
def convert(probs, total):
    for (word, counts) in probs.items():
        # Laplace correction, then divide by total count of label
        for i in range(len(counts)):
            counts[i] = float(counts[i])/(total[i])

    # Convert totals to probabilities as well
    total_counts = sum(total)
    for i in range(len(total)):
        total[i] /= float(total_counts)


if __name__ == "__main__":
    words = generate_set("data/labeled_corpus.tsv")
    probabilities, totals = create_counts(words, "data/labeled_corpus.tsv")
    convert(probabilities, totals)
    print(probabilities["dien"])
    print(totals)
