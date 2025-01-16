alpha = 0.005
movie_names = cols[:400]
n = len(movie_names)

def test_sociality(movie_name: str):
    sql = f"""
    SELECT "{movie_name}", "{social_col}"
    FROM movies WHERE "{social_col}" IN (1, 0);
    """
    df = pd.read_sql(sql, con=conn).dropna()
    social_watchers = df[df[social_col] == 0]
    nonsocial_watchers = df[df[social_col] == 1]
    return stats.mannwhitneyu(social_watchers[movie_name], nonsocial_watchers[movie_name], alternative="greater")

results = {}

for movie_name in movie_names:
    p = test_sociality(movie_name).pvalue
    results[movie_name] = p

# proportion of significant results
sum(list(map(lambda x: x < alpha, results.values())))/n

social_movies = list(filter(lambda x: x[1] < alpha, results.items()))
table_df = pd.DataFrame(
    {"Title": [*map(lambda x: x[0], social_movies)],
     "P-value": [*map(lambda x: round(x[1], 5), social_movies)],}
)
styled = table_df.style
dfi.export(styled, "problem_8.png")
