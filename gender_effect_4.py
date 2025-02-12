sql = "SELECT * FROM movies LIMIT 1;"
cols = pd.read_sql(sql, con=conn).columns
gender_col: str = cols[474] # (1 = female, 2 = male)
gender_col

movie_names = cols[:400]
n = len(movie_names)

def test_gender_effect(movie_name: str):
    sql = f"""
    SELECT "{movie_name}", "{gender_col}"
    FROM movies WHERE "{gender_col}" IN (1, 2);
    """
    df = pd.read_sql(sql, con=conn).dropna()
    female_watchers = df[df[gender_col] == 1]
    male_watchers = df[df[gender_col] == 2]
    return stats.mannwhitneyu(female_watchers[movie_name], male_watchers[movie_name], alternative="greater")

results = {}

for movie_name in movie_names:
    p = test_gender_effect(movie_name).pvalue
    results[movie_name] = p

sum(list(map(lambda x: x < alpha, results.values())))/n
