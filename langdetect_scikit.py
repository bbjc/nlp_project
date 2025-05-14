import numpy as np
from sklearn.metrics import f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# =============================================================================
# Language detection using scikit's Naïve Bayes implementation
# =============================================================================

N = 3   # N-gram size
trainFile = "easy-train.tsv"
#trainFile = "challenging-train.tsv"
evalFile = "easy-eval.tsv"
#evalFile = "challenging-eval.tsv"

def readData(fileName):
    data = []
    labels = []
    f = open(fileName, "r", encoding="utf-8")
    for line in f.readlines():
        line = line[:-1]
        lang, txt = line.split("\t")
        data.append(txt)
        labels.append(lang)
    f.close()
    return data, labels

vectorizer = CountVectorizer(encoding = "utf-8", \
                             strip_accents = None, \
                             lowercase = True, \
                             tokenizer = None, \
                             ngram_range=(N, N), \
                             analyzer="char" \
                             )
naiveBayes = MultinomialNB(alpha = 0.0001)

trainData, trainLabels = readData(trainFile)
trainFeatures = vectorizer.fit_transform(trainData)
naiveBayes.fit(trainFeatures, trainLabels)

evalData, evalLabels = readData(evalFile)
evalFeatures = vectorizer.transform(evalData)
predictions = naiveBayes.predict(evalFeatures)

# Compute the predicition accuracy:
# the correct predictions over the total predictions
total = 0
correct = 0
for i in range(0, len(predictions)):
    if predictions[i] == evalLabels[i]:
        correct = correct + 1
    total = total + 1
print("Accuracy of scikit's classifier:" + str(correct / total))