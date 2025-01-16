import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import re
from scipy.stats import mannwhitneyu, bootstrap
from sklearn.utils import resample

# Load the dataset
file_path = '/content/movieReplicationSet.csv'
movie_data = pd.read_csv(file_path)

# AFYD Output
afyd_output = {}

# Select only the movie rating columns (first 400 columns)
movie_ratings = movie_data.iloc[:, :400]

# Calculate popularity by counting non-missing ratings for each movie
movie_popularity = movie_ratings.notna().sum()  # Count of non-NaN values (number of ratings) for each movie

# Perform a median split on popularity to categorize movies as high or low popularity
median_popularity = movie_popularity.median()
high_popularity_movies = movie_popularity[movie_popularity >= median_popularity].index
low_popularity_movies = movie_popularity[movie_popularity < median_popularity].index

# Extract ratings for high and low popularity movies and remove NaN values
high_popularity_ratings = movie_ratings[high_popularity_movies].stack().values  # Stack to remove NaNs
low_popularity_ratings = movie_ratings[low_popularity_movies].stack().values

# Perform the Mann-Whitney U test to compare the ratings of high and low popularity movies
u_statistic, p_value = stats.mannwhitneyu(high_popularity_ratings, low_popularity_ratings, alternative='two-sided')

# Visualize the ratings distribution for high and low popularity movies
plt.figure(figsize=(10, 6))
plt.hist(high_popularity_ratings, bins=5, alpha=0.5, label='High Popularity', color='blue')
plt.hist(low_popularity_ratings, bins=5, alpha=0.5, label='Low Popularity', color='orange')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Ratings Distribution for High vs. Low Popularity Movies')
plt.legend()
plt.show()
