# Extract the rating data for "Shrek (2001)"
shrek_ratings = movie_ratings['Shrek (2001)']

# Extract gender information from the dataset
gender_data = movie_data['Gender identity (1 = female; 2 = male; 3 = self-described)']

# Separate Shrek ratings by male and female viewers (exclude self-described)
shrek_ratings_female = shrek_ratings[gender_data == 1].dropna()
shrek_ratings_male = shrek_ratings[gender_data == 2].dropna()

# Perform the Mann-Whitney U test to compare Shrek ratings by gender
u_statistic_q3, p_value_q3 = stats.mannwhitneyu(shrek_ratings_female, shrek_ratings_male, alternative='two-sided')

# Visualize the ratings distribution for Shrek by gender
plt.figure(figsize=(10, 6))
plt.hist(shrek_ratings_female, bins=5, alpha=0.5, label='Female', color='pink')
plt.hist(shrek_ratings_male, bins=5, alpha=0.5, label='Male', color='blue')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Ratings Distribution for Shrek (2001) by Gender')
plt.legend()
plt.show()

# Calculate Cliff's Delta for effect size
def cliffs_delta(x, y):
    n_x, n_y = len(x), len(y)
    greater, lesser = 0, 0
    for i in x:
        for j in y:
            if i > j:
                greater += 1
            elif i < j:
                lesser += 1
    delta = (greater - lesser) / (n_x * n_y)
    return delta

cliffs_delta_value = cliffs_delta(shrek_ratings_female, shrek_ratings_male)
print(f"Cliff's Delta: {cliffs_delta_value}")

# Bootstrap confidence interval for the median difference in ratings
def median_diff(x, y):
    return np.median(x) - np.median(y)

# Perform bootstrap sampling for confidence interval estimation
bootstrap_results = bootstrap(
    data=(shrek_ratings_female, shrek_ratings_male),
    statistic=median_diff,
    paired=False,
    n_resamples=10000,  # We can increase this for higher accuracy
    method='percentile'
)

ci_low, ci_high = bootstrap_results.confidence_interval
print(f"Bootstrap Confidence Interval for Median Difference: ({ci_low}, {ci_high})")
