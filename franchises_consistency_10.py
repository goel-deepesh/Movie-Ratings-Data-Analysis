alpha = 0.005
franchises = ["Star Wars", "Harry Potter", "The Matrix", "Indiana Jones", "Jurassic Park", "Pirates of the Caribbean", "Toy Story", "Batman"]
filter_fun = lambda x: any([franchise in x for franchise in franchises])
cat_fun = lambda x: [franchise for franchise in franchises if franchise in x][0]
all_franchise_titles = [*filter(filter_fun, cols)]
franchises_mapped = [*map(cat_fun, all_franchise_titles)]
titles_with_franchises = [*zip(all_franchise_titles, franchises_mapped)]

results = {}
for franchise in franchises:
    fun = lambda x: x[1] == franchise
    titles_with_franchises_subset = [*filter(fun, titles_with_franchises)]
    titles_subset = [*map(operator.itemgetter(0), titles_with_franchises_subset)]
    select_cols = "\"" + "\", \"".join(titles_subset) + "\""
    sql = f"""
    SELECT {select_cols} FROM movies
    """
    df = pd.read_sql(sql, con=conn).dropna()
    series_list = []

    for title in titles_subset:
        series_list.append(df[title].dropna())
    results[franchise] = stats.kruskal(*series_list).pvalue
table_df = pd.DataFrame(
    {"Title": [*map(lambda x: x[0], results.items())],
     "P-value": [*map(lambda x: round(x[1], 5), results.items())],
     "Significant": [*map(lambda x: x[1] < alpha, results.items())]
     }
)
styled = table_df.style
dfi.export(styled, "./Q10.png")
