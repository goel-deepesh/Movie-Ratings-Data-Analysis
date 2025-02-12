# Extract release years from the movie titles in the first 400 columns
release_years = [int(re.search(r'\((\d{4})\)', col).group(1)) for col in movie_ratings.columns]

# Determine the median release year to categorize movies as 'new' and 'old'
median_year = np.median(release_years)
new_movies = [i for i, year in enumerate(release_years) if year >= median_year]
old_movies = [i for i, year in enumerate(release_years) if year < median_year]

# Extract ratings for new and old movies and remove NaN values
new_movie_ratings = movie_ratings.iloc[:, new_movies].stack().values
old_movie_ratings = movie_ratings.iloc[:, old_movies].stack().values

# Perform the Mann-Whitney U test for comparing ratings of new vs. old movies
u_statistic_q2, p_value_q2 = stats.mannwhitneyu(new_movie_ratings, old_movie_ratings, alternative='two-sided')

# Visualize the ratings distribution for new vs. old movies
plt.figure(figsize=(10, 6))
plt.hist(new_movie_ratings, bins=5, alpha=0.5, label='New Movies', color='green')
plt.hist(old_movie_ratings, bins=5, alpha=0.5, label='Old Movies', color='purple')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Ratings Distribution for New vs. Old Movies')
plt.legend()
plt.show()
