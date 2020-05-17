import pandas as pd
import numpy as np
import re
from os import listdir
from os.path import isfile, join
import nltk
from nltk.stem import WordNetLemmatizer 
import string

# Get all the file names
onlyfiles = [f for f in listdir("./30reviews/") if isfile(join("./30reviews/", f))]

# Get the unique movie titles
movieTitles = np.unique(np.array([fil.split("_")[0] for fil in onlyfiles]))

movieDict = {}

for movie in movieTitles:
    allMovies = list(filter(lambda x: movie in x, onlyfiles))
    pos = list(filter(lambda x: "positive" in x, allMovies))
    neg = list(filter(lambda x: "negative" in x, allMovies))
    movieDict[movie] = {}
    movieDict[movie]["positive"] = pos
    movieDict[movie]["negative"] = neg

# Load the dominant topic distribution
df = pd.read_csv("df_dominant_topic_30reviewsCom.csv")

# Drop rows where document is empty
df = df[df.Text != "[]"]
df.reset_index(drop=True, inplace=True)


# ### Emma(1996)

# Function to get dataframe of DocNo, Original Document Text and Dominant Topic

def getDf(movieName, polarity):
    posMovies = movieDict[movieName][polarity]
    pDomTopic = ', '.join(list(df[df["Movie"]==movieName+"_"+polarity]["Keywords"]))
    ptxtLst = []
    for pos in posMovies:
        ptxt = open("30reviews/"+pos, "r").read()
        ptxt = re.sub("<br />","",ptxt)
        ptxtLst.append(ptxt)
    posDict = {}
    posDict["DocNo"] = posMovies
    posDict["Text"] = ptxtLst
    pTxtDf = pd.DataFrame(posDict)
    pTxtDf["DocNo"] = pTxtDf.DocNo.apply(lambda x: re.findall("(doc.*)_",x)[0])
    pTxtDf["DominantTopic"] = pDomTopic
    return pDomTopic, pTxtDf

# Function to get summaries for given movie name and polarity

def getSum(movieName, polarity):
    posSummary = open("v6_summaryOnlyCue/{}_{}.txt".format(movieName, polarity)).readlines()
    posSummary = [i.replace('\n',"") for i in posSummary]
    posSummary = [i for i in posSummary if i != ""]
    posSummary = [str(i)+": "+j for i,j in enumerate(posSummary)]
    return posSummary

# Function to get dataframe of DocNo, Text, Dominant TOpic, Sentences Picked and TopicWords

def getDfUp(pTxtDf, posSummary):
    lemmatizer = WordNetLemmatizer()
    comSentences = []
    comTopic = []

    for ind,row in pTxtDf.iterrows():
        rowCom = []
        topCom = []
        topDict = {}
        txt = row["Text"]
        for r in posSummary:
            if r.split(": ")[1] in txt:
                rowCom.append(r)
                rWords = r.split()
                rWords = [w.translate(str.maketrans('', '', string.punctuation)) for w in rWords]
                rWords = [w.lower() for w in rWords]
                rWords = [lemmatizer.lemmatize(w) for w in rWords]
                commonWords = list(set(rWords).intersection(set(row["DominantTopic"].split(', '))))
                innerLst = []
                for com in commonWords:
                    x = rWords.count(com)
                    innerLst.extend([com]*x)
                topCom.extend(innerLst)
        if len(topCom) > 0:
            for tc in topCom:
                topDict[tc] = topCom.count(tc)
        comSentences.append(rowCom)
        comTopic.append(topDict)
    pTxtDf2 = pTxtDf.copy()
    pTxtDf2["SentencesPicked"] = comSentences
    pTxtDf2["TopicWords"] = comTopic
    
    return pTxtDf2

# Function to get dataframe of SentencesPicked, Topic Words, Dominant Topic

def getSumDf(posSummary, pDomTopic):
    lemmatizer = WordNetLemmatizer()
    comTopic = []
    count = 0
    for r in posSummary:
        r = r.replace(str(count),"").replace(":","")
        rWords = r.split()
        rWords = [w.translate(str.maketrans('', '', string.punctuation)) for w in rWords]
        rWords = [w.lower() for w in rWords]
        rWords = [lemmatizer.lemmatize(w) for w in rWords]
        commonWords = list(set(rWords).intersection(set(pDomTopic.split(', '))))
        innerLst = []
        topDict = {}
        topCom = []
        for com in commonWords:
            x = rWords.count(com)
            innerLst.extend([com]*x)
        topCom.extend(innerLst)
        if len(topCom) > 0:
            for tc in topCom:
                topDict[tc] = topCom.count(tc)
        comTopic.append(topDict)
        count += 1
    pSumDf = pd.DataFrame()
    pSumDf["SentencesPicked"] = posSummary
    pSumDf["Topic Words"] = comTopic
    pSumDf["Dominant Topic"] = pDomTopic
    return pSumDf

# Do for positive review first

positiveDomTopic, positiveDf = getDf("Emma(1996)", "positive")
positiveSummary = getSum("Emma(1996)", "positive")
positiveDf2 = getDfUp(positiveDf, positiveSummary)
positiveSumDf = getSumDf(positiveSummary, positiveDomTopic)


# Do for negative

negativeDomTopic, negativeDf = getDf("Emma(1996)", "negative")
negativeSummary = getSum("Emma(1996)", "negative")
negativeDf2 = getDfUp(negativeDf, negativeSummary)
negativeSumDf = getSumDf(negativeSummary, negativeDomTopic)


# Save to csv files

positiveDf2.to_csv("Emma(1996)_positiveEvaluation.csv", columns=positiveDf2.columns, index=False, encoding="utf8")
positiveSumDf.to_csv("Emma(1996)_positiveSummaryEvaluation.csv", columns=positiveSumDf.columns, index=False, encoding="utf8")
negativeDf2.to_csv("Emma(1996)_negativeEvaluation.csv", columns=negativeDf2.columns, index=False, encoding="utf8")
negativeSumDf.to_csv("Emma(1996)_negativeSummaryEvaluation.csv", columns=negativeSumDf.columns, index=False, encoding="utf8")

