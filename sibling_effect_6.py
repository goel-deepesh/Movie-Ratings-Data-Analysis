movie_names = cols[:400]
n = len(movie_names)

def test_sibling_effect(movie_name: str):
    sql = f"""
    SELECT "{movie_name}", "{sibs_col}"
    FROM movies WHERE "{sibs_col}" IN (1, 0);
    """
    df = pd.read_sql(sql, con=conn).dropna()
    only_child_watchers = df[df[sibs_col] == 0]
    sibling_watchers = df[df[sibs_col] == 1]
    return stats.mannwhitneyu(only_child_watchers[movie_name], sibling_watchers[movie_name], alternative="greater")

results = {}

for movie_name in movie_names:
    p = test_sibling_effect(movie_name).pvalue
    results[movie_name] = p

sum(list(map(lambda x: x < alpha, results.values())))/n


only_child_movies = {}
sibling_movies = []
for key,val in results.items():
    if val < alpha or val == alpha:
        only_child_movies[key] = val
    else:
        sibling_movies.append([key, val])
