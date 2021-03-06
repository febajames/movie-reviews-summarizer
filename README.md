# movie-reviews-summarizer

Data Source: Kaggle<br/>
IMDB movie reviews dataset consisting of equally distributed positive and negative reviews. Positive reviews are reviews with a user graded score of between 7-10 while negative reviews have a user graded score of 0-4; there are no neutral reviews in the dataset.<br/>
Applied aspect-based text summarization on movie reviews, and transforming them into an easy-to-read and structured information deck through the use of Python dash. The two major NLP techniques used to achieve the objective are (i) topic modelling and (ii) multi-document extractive summarization. The main attributes of each movie have been identified through the topic words. These topic words have then been fed into the summarizer as inputs for sentence extractions which are then used to produce summaries. 

**webscraping.py**: scrape movie titles and genres for movies from IMDB

**correctTitlesSaveTrain.py**: rename problematic movie names. Rename all documents based on movie name and sentiment. Save to a folder

**getCountofMovies.py**: get the number of reviews per movie name. Select only those with 30 reviews and save them to a new folder

**movieDict.py**: combine all the positive reviews for 1 movie into a single document and all the negative reviews for 1 movie into a single document. Save files to a new folder 

**Project_30reviewsCom_Mallet.ipynb**: complete project code using Mallet LDA model. Generate the summaries for each movie using the dominant topic. Use only the Cue method of Edmundson Summarizer for generating the summaries

**Edmundson Summarizer Source Code.ipynb**: open source code - edmundson summarizer from sumy package for extractive summarization (Edmundson, 1969). Utilized it's cue method which uses bonus words (we passed the top 10 topic words from each topic of lda) to score sentences and produce the summaries for the movies

**sumEvalEmmaNew.py**: summary evaluation script for Emma (1996)
