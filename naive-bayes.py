import json
import random
import util
import math

class NaiveBayes():
    """
    Any kind of data is just a list of Counters 
    i.e., [(word -> word freq), ... ]
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.k = 1 #smoothing parameter, fine tune in validation step

    def trainAndValidate(self, trainingData, trainingLabels, validationData, validationLabels):
        wordCounts = util.Counter() #counts of fake words, counts of real words
        allWords = set({})
        prior = util.Counter() #starts off being the number of fake and real articles

        #for each word, need to find conditional probability you see that word given label
        conditionalProbs = util.Counter() #starts off being (word,label) -> count
        for i in range(len(trainingData)):
            prior[trainingLabels[i]] += 1

            article = trainingData[i]
            label = trainingLabels[i]
            for word in article:
                allWords.add(word)

                conditionalProbs[(word, label)] += article[word]
                wordCounts[label] += article[word]

        #tweak k based on validation data
        self.validate(trainingData, trainingLabels, validationData, validationLabels, allWords, wordCounts, prior, conditionalProbs)

    def validate(self, trainingData, trainingLabels, validationData, validationLabels, allWords, wordCounts, prior, conditionalProbs):
        possibleKs = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        for k in possibleKs:
            #laplace smoothing based on current value of k
            #update conditional probabilities
            newCondProbs = conditionalProbs.copy()
            
            #get the conditional probs adjusted
            for (word, label) in newCondProbs:
                numerator = (newCondProbs[(word,label)] + k)
                denominator = k*len(allWords) + wordCounts[label]*1.0
                newCondProbs[(word,label)] = numerator/denominator

            #need to smooth prior too?
            newPrior = prior.copy()
            for label in newPrior:
                newPrior[label] += k
            newPrior.normalize()

            self.prior = newPrior
            self.condProbs = newCondProbs

            #try it out on validation set
            bestAcc = -1
            bestPrior = util.Counter()
            bestCondProbs = util.Counter()
            bestK = 0

            classifications = self.classify(validationData)
            acc = [classifications[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)

            print "Performance on validation set for k=%f: (%.1f%%)" % (k, 100.0*acc/len(validationLabels))
            if acc > bestAcc:
                bestPrior = newPrior
                bestCondProbs = newCondProbs
                bestK = k
                bestAcc = acc
        #update with the best stuff
        self.prior = bestPrior
        self.condProbs = bestCondProbs
        self.k = bestK

    def classify(self, data):
        classifications = []
        for i in range(len(data)):
            options = self.calculateLogJointProbabilities(data[i])
            classifiedLabel = options.argMax()
            classifications.append(classifiedLabel)
        return classifications

    def calculateLogJointProbabilities(self, datum):
        logJoint = util.Counter()
        for label in self.legalLabels:
            logProb = math.log(self.prior[label])
            for word in datum:
                #either an article has some occurrences of a word or it doesn't
                if datum[word] > 0:
                    #account for number of times you've seen the word
                    logProb += datum[word]*(math.log(self.condProbs[(word,label)]))
            logJoint[label] = logProb
        return logJoint


with open('data.json') as json_file:  
    data = json.load(json_file)

    allWords = set({})

    trainingData = []
    trainingLabels = []
    validationData = []
    validationLabels = []
    testData = []
    testLabels = []

    #shuffle around the data in a "deterministic" way
    #need more data - naive bayes classifer has an accuracy of 88% (!!!) with seed 5,
    #but signficantly lower accuracies (around 44-66%) with some other seeds i tried out
    random.Random(3).shuffle(data)

    for i in range(len(data)):
        article = data[i]
        wordCounts = util.Counter(article["counts"]) #word -> freq
        label = article["label"]

        #put data/label into training, validation, or testing
        for word in wordCounts:
            allWords.add(word)

        if i <= 0.70*len(data):
            trainingData.append(wordCounts)
            trainingLabels.append(label)
        elif i <= 0.85*len(data):
            validationData.append(wordCounts)
            validationLabels.append(label)
        else:
            testData.append(wordCounts)
            testLabels.append(label)

    #probably a dumb thing, idk how to do a better way
    #words not seen in an article have a freq of 0
    for i in range(len(trainingData)):
        features = trainingData[i]
        for word in allWords:
            if word not in features:
                features[word] = 0
    for i in range(len(validationData)):
        features = validationData[i]
        for word in allWords:
            if word not in features:
                features[word] = 0
    for i in range(len(testData)):
        features = testData[i]
        for word in allWords:
            if word not in features:
                features[word] = 0

    baseline = NaiveBayes(["fake", "real"])

    #run training/validation
    baseline.trainAndValidate(trainingData, trainingLabels, validationData, validationLabels)

    #evaluate performance on test set
    predictions = baseline.classify(testData)
    accuracyCount =  [predictions[i] == testLabels[i] for i in range(len(testLabels))].count(True)
    print "Naive Bayes baseline on test set: ", (1.0*accuracyCount/len(testLabels))*100.0, "%"

