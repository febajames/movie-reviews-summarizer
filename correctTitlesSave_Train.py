import pandas as pd
import numpy as np
import re
from os import listdir
from os.path import isfile, join

# Load the file
train = pd.read_csv("train_url_titles_genres.csv")
trainDict = {"http://www.imdb.com/title/tt0082436":"Garde a vue (1981)", 
             "http://www.imdb.com/title/tt0756654":"Gota kanal 2 - Kanalkampen (2006)", 
            "http://www.imdb.com/title/tt0243377":"O Lampiao da Estrela (2000)", 
            "http://www.imdb.com/title/tt0313487":"Pokemon 4Ever (2001)", 
            "http://www.imdb.com/title/tt0404259":"Memoires affectives (2004)", 
            "http://www.imdb.com/title/tt0067183":"Hare Rama Hare Krishna (1971)", 
            "http://www.imdb.com/title/tt0085501":"Erendira (1983)",
            "http://www.imdb.com/title/tt0284735":"Il etait une fois... la vie", 
            "http://www.imdb.com/title/tt0422909":"Panaghoy sa suba: The Call of the River (2004)",
            "http://www.imdb.com/title/tt0309832":"Malefique (2002)", 
            "http://www.imdb.com/title/tt0459744":"Ashura-jo no hitomi (2005)",
            "http://www.imdb.com/title/tt0067011":"Adios Companeros (1971)",
            "http://www.imdb.com/title/tt0276951":"Faat Kine (2001)",
            "https://www.imdb.com/title/tt0399877/":"What the Bleep Do We Know!? (2004)",
            "http://www.imdb.com/title/tt0372401":"Sex Sells: The Making of 'Touche' (2005)",
            "http://www.imdb.com/title/tt0266860":"Pokemon 3: The Movie (2000)",
            "http://www.imdb.com/title/tt0412596":"Cafe Lumiere (2003)",
            "http://www.imdb.com/title/tt0841150":"Protege (2007)",
            "http://www.imdb.com/title/tt0798733":"Return to Goree (2007)",
            "http://www.imdb.com/title/tt0086136":"Premiers desirs (1983)",
            "https://www.imdb.com/title/tt0154443/":"8.5 Women (1999)",
            "http://www.imdb.com/title/tt0113828":"Les Miserables (1995)",
            "http://www.imdb.com/title/tt0257001":"Pokemon: The Movie 2000 (1999)",
            "https://www.imdb.com/title/tt0784558/":"Stargate SG-1 (1997–2007)",
            "http://www.imdb.com/title/tt0026725":"Les Miserables (1935)",
            "http://www.imdb.com/title/tt0302882":"L'odyssee d'Alice Tremblay (2002)",
            "http://www.imdb.com/title/tt0164877":"Sexo, pudor y lagrimas (1999)",
            }

# Function to correct titles
def renameDf(df, Dict):
    def rename(row):
        urll = row["url"]
        titlee = row["title"]
        if urll in Dict.keys():
            titlee = Dict[urll]
        return titlee
    return rename
train["title"] = train.apply(renameDf(train, trainDict), axis=1)

# Need to replace some symbols in the titles
symbols1 = [":","/"]
symbols2 = [".","#","?","$","*","+"]

def replaceSym(df, symLst1, symLst2):
    def replace(row):
        titlee = row["title"]
        for i in symbols1:
            if i in titlee:
                titlee = titlee.replace(i, " -")
        for j in symbols2:
            if j in titlee:
                titlee = titlee.replace(j, "")
        return titlee
    return replace

train["title"] = train.apply(replaceSym(train, symbols1, symbols2), axis=1)


# Deselect Unnamed column
train.drop(columns="Unnamed: 0", inplace=True)

# Save this to csv
train.to_csv("train_url_titles_genres_cleaned.csv", columns=train.columns, index=False, encoding="utf8")


# ## Can start renaming the files -- for train

# ### Do for positive first

# Function to get all urls in train/test and pos/neg folders
# folder = train or test
# subfolder = pos or neg
def getUrls(folder, subfolder):
    onlyfiles = [f for f in listdir("{}/{}".format(folder,subfolder)) if isfile(join("{}/{}".format(folder,subfolder), f))]
    onlyfiles.sort(key=lambda x: int(x.split("_")[0]))
    urls = open("{}/urls_{}.txt".format(folder,subfolder)).read().splitlines()
    urls = [i.replace("/usercomments", "") for i in urls]
    return onlyfiles, urls

# Get all positive urls
onlyfiles_pos, urls_pos = getUrls("train", "pos")

# Create a dict between title url and movie title
urlTitleDict = {row["url"]:row["title"] for ind,row in train.iterrows()}

# Create a dict between file index and movie url
indUrlDict = {}
for i in range(len(urls_pos)):
    indUrlDict[i] = urls_pos[i]
    
# List of unique urls
uniqueUrls = set(indUrlDict.values())

# Get a dict of url:file indices
urlIndDict ={}
for urll in uniqueUrls:
    inds = [k for k,v in indUrlDict.items() if v == urll]
    urlIndDict[urll] = inds
    
# Create a dict of title and corresponding file indices
titleIndDict = {}
for i in urlIndDict.keys():
    # Get the corresponding movie title
    titleIndDict[urlTitleDict[i]] = urlIndDict[i]
    
# Create a dictionary of indices to filename
indFilDict = {int(i.split("_")[0]):i for i in onlyfiles_pos}

# Start reading and creating filenames
for title in titleIndDict.keys():
    count = 0
    inds = titleIndDict[title]
    for ind in inds:
        filname = indFilDict[ind]
        with open("train/pos/"+filname) as fil:
            filData = fil.read()
            with open("train/allDocsTrain2/{}_doc{}_positive.txt".format(title, count),"w") as filr: 
                filr.write(filData) 
        count += 1


# ### Do for negative
# Get all negative urls
onlyfiles_neg, urls_neg = getUrls("train", "neg")

# Create a dict between title url and movie title
urlTitleDict = {row["url"]:row["title"] for ind,row in train.iterrows()}

# Create a dict between file index and movie url
indUrlDict = {}
for i in range(len(urls_neg)):
    indUrlDict[i] = urls_neg[i]
    
# List of unique urls
uniqueUrls = set(indUrlDict.values())

# Get a dict of url:file indices
urlIndDict ={}
for urll in uniqueUrls:
    inds = [k for k,v in indUrlDict.items() if v == urll]
    urlIndDict[urll] = inds
    
# Create a dict of title and corresponding file indices
titleIndDict = {}
for i in urlIndDict.keys():
    # Get the corresponding movie title
    titleIndDict[urlTitleDict[i]] = urlIndDict[i]
    
# Create a dictionary of indices to filename
indFilDict = {int(i.split("_")[0]):i for i in onlyfiles_neg}

# Start reading and creating filenames
for title in titleIndDict.keys():
    count = 0
    inds = titleIndDict[title]
    for ind in inds:
        filname = indFilDict[ind]
        with open("train/neg/"+filname) as fil:
            filData = fil.read()
            with open("train/allDocsTrain2/{}_doc{}_negative.txt".format(title, count),"w") as filr: 
                filr.write(filData) 
        count += 1


