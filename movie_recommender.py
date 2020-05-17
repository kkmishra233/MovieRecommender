import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return movie_list[movie_list.index == index]["title"].values[0]

def get_index_from_title(title):
	return movie_list[movie_list.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
movie_list = pd.read_csv('movie_dataset.csv')
print(movie_list.head())
#print(movie_list.columns)
##Step 2: Select Features
features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
    movie_list[feature] = movie_list[feature].fillna('')

def combine_features(row):
    try:
        return row["keywords"]+" "+row["cast"]+" "+row["genres"]+" "+row["director"]
    except:
        print(row)

movie_list["combined_features"] = movie_list.apply(combine_features,axis=1)
print(movie_list["combined_features"].head())
##Step 4: Create count matrix from this new combined column
createcountvector = CountVectorizer()
count_matrix = createcountvector.fit_transform(movie_list["combined_features"])
##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)
print(cosine_sim)
movie_user_likes = input("Enter a movie Name you like most : ")
## Step 6: Get index of this movie from its title
movie_index = get_index_from_title(movie_user_likes)
similar_movies = list(enumerate(cosine_sim[movie_index]))
## Step 7: Get a list of similar movies in descending order of similarity score
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
## Step 8: Print titles of first 50 movies
i = 0
for movie in sorted_similar_movies:
    print(get_title_from_index(movie[0]))
    i = i+1
    if i > 10:
        break;