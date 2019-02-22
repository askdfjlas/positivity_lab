from naive_bayes import *
import math
import json

label_array = ["positive", "negative", "neutral", "irrelevant"]


def classify(tweet, probs, total_counts):
    tweet = special(clean_tweet(tweet, emo_repl_order, emo_repl, re_repl))
    scores = [0, 0, 0, 0]

    for i in range(len(labels)):
        scores[i] += math.log(total_counts[i], 2)

        for word in tweet.split():
            duplicates = set()

            if word in probs and word not in duplicates:
                try:
                    scores[i] += math.log(probs[word][i], 2)
                except:
                    pass

            duplicates.add(word)

    max_index = 0
    for i in range(len(scores)):
        if scores[i] > scores[max_index]:
            max_index = i

    return label_array[max_index]


def output_data():
    inp = open("data/locations_classified.tsv")

    c = 0
    t = 0
    g = 0

    data = []
    current = {"score": 0, "g": 0, "t": 0}
    current_count = 0
    for row in inp:
        arr = row.rstrip().split("\t")

        if (float(arr[0]) != t or float(arr[1]) != g) and c > 0:
            current["score"] = (current["score"]/float(current_count) + 1)/2
            current["g"] = round((g + 0.025)*1000)/float(1000)
            current["t"] = round((t + 0.025)*1000)/float(1000)
            data.append(current)

            current = {"score": 0, "g": 0, "t": 0}
            current_count = 0

        if arr[-1] == "positive":
            current["score"] += 1
        elif arr[-1] == "negative":
            current["score"] -= 1

        t = float(arr[0])
        g = float(arr[1])

        current_count += 1
        c += 1

    inp.close()

    return data


def main():
    relevant_words = generate_set("data/labeled_corpus.tsv")
    probs, total_counts = create_counts(relevant_words, "data/labeled_corpus.tsv")
    convert(probs, total_counts)

    input_set = open("data/geo_twits_squares.tsv")
    output = open("data/locations_classified.tsv", "w")

    for row in input_set:
        arr = row.rstrip().split("\t")
        c = classify(arr[-1], probs, total_counts)

        output.write(arr[0] + "\t" + arr[1] + "\t" + c + "\n")

    input_set.close()
    output.close()

    js = open("data.js", "w")
    js.write("data = " + json.dumps(output_data()))
    js.close()


if __name__ == "__main__":
    main()
