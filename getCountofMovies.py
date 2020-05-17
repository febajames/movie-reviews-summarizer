import pandas as pd
import numpy as np
import re
from os import listdir
from os.path import isfile, join
from operator import itemgetter 
from pprint import pprint

# Get a list of all the movie review names we have
onlyfiles = [f for f in listdir("train/allDocsTrain2/") if isfile(join("train/allDocsTrain2/", f))]

# Extract out just the movie titlw
filnames = [fil.split("_")[0] for fil in onlyfiles]

# Make it into a df
movies = pd.DataFrame(filnames, columns=["title"])

# Get the number of reviews per Movie
movieDf  = movies["title"].value_counts()
movieDf = pd.DataFrame(movieDf)
movieDf.reset_index(inplace=True)
movieDf.columns = ["title", "Count"]

# Load the file with the genre information
movieGenre = pd.read_csv("train_url_titles_genres_cleaned.csv")
movieGenre2 = movieGenre.drop(["url"], axis=1)

# Merge with the movieDf
movieDf2 = movieDf.merge(movieGenre2, on="title")

# Save to csv file
movieDf2.to_csv("movieCounts.csv", columns=movieDf2.columns, index=False, encoding="utf8")

# Count of the number of movies for each count
movieCount = movieDf.groupby("Count").count()
movieCount.reset_index(inplace=True)
movieCount.columns = ["Count", "Number of Movies"]

# Save to csv file
movieCount.to_csv("Number_of_movies_per_Count.csv", columns=movieCount.columns, index=False, encoding="utf8")

# ### Save all movies with 30 reviews to a new folder

# Extract out the movies with 30 reviews 
movie30 = movieDf2[movieDf2["Count"]==30]
movie30Lst = list(movie30["title"])

# Make a dictionary of movie names with 30 reviews with its corresponding indices
filnamesArr = np.array(filnames)
movie30Dict = {movie:list(np.where(filnamesArr==movie)[0]) for movie in movie30Lst}

# Get all the complete file names
movie30FilInd = [mov for movie in movie30Dict.values() for mov in movie]
movie30FilName = [onlyfiles[movie] for movie in movie30FilInd]

# Open these files and save to new folder
for movie in movie30FilName:
    with open("train/allDocsTrain2/"+movie) as fil:
        filData = fil.read()
        with open("30reviews/"+movie, "w") as filr: 
                filr.write(filData) 


