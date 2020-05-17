import pandas as pd
import numpy as np
import re
from os import listdir
from os.path import isfile, join

# Get all the file names
onlyfiles = [f for f in listdir("./30reviews/") if isfile(join("./30reviews/", f))]

# Get the unique movie titles
movieTitles = np.unique(np.array([fil.split("_")[0] for fil in onlyfiles]))

moviePos = {}
movieNeg = {}

for movie in movieTitles:
    allMovies = list(filter(lambda x: movie in x, onlyfiles))
    pos = list(filter(lambda x: "positive" in x, allMovies))
    neg = list(filter(lambda x: "negative" in x, allMovies))
    moviePos[movie] = pos
    movieNeg[movie] = neg

movieDict = {}

for movie in movieTitles:
    allMovies = list(filter(lambda x: movie in x, onlyfiles))
    pos = list(filter(lambda x: "positive" in x, allMovies))
    neg = list(filter(lambda x: "negative" in x, allMovies))
    movieDict[movie] = {}
    movieDict[movie]["positive"] = pos
    movieDict[movie]["negative"] = neg

movieParas = {}
for movie in movieTitles:
    pos = movieDict[movie]["positive"]
    neg = movieDict[movie]["negative"]
    movieParas[movie] = {}
    
    ptext = []
    ntext = []
    for p in pos:
        ptxt = open("30reviews/"+p, "r").read()
        ptxt = re.sub("<br />","",ptxt)
        ptxt = ptxt.split(".")
        ptxt = [p.strip() for p in ptxt]
        ptxt[-1] = ptxt[-1] + "."
        ptxt = '. '.join(ptxt)
        ptext.append(ptxt)
    for n in neg:
        ntxt = open("30reviews/"+n, "r").read()
        ntxt = re.sub("<br />","",ntxt)
        ntxt = ntxt.split(".")
        ntxt = [n.strip() for n in ntxt]
        ntxt[-1] = ntxt[-1] + "."
        ntxt = '. '.join(ntxt)
        ntext.append(ntxt)
        
    movieParas[movie]["positive"] = ptext
    movieParas[movie]["negative"] = ntext

movieParas2 = {}

for movie in movieParas.keys():
    movieParas2[movie] = {}
    pos = ' '.join(movieParas[movie]["positive"])
    neg = ' '.join(movieParas[movie]["negative"])
    
    movieParas2[movie]["positive"] = pos
    movieParas2[movie]["negative"] = neg

# Save the files to new folder
for movie in movieParas2.keys():
    with open("30reviewsCom/"+movie+"_positive.txt", "w") as filr: 
        filr.write(movieParas2[movie]["positive"])
    with open("30reviewsCom/"+movie+"_negative.txt", "w") as filr: 
        filr.write(movieParas2[movie]["negative"])


