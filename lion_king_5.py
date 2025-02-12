sql = "SELECT * FROM movies LIMIT 1;"
cols = pd.read_sql(sql, con=conn).columns
sibs_col: str = cols[475] # (1: Yes; 0: No; -1: Did not respond)
sibs_col

sql = f"""
SELECT "The Lion King (1994)", "{sibs_col}"
FROM movies WHERE "{sibs_col}" IN (1, 0);
"""
df = pd.read_sql(sql, con=conn).dropna()
df.head()

only_child = df[df[sibs_col] == 1]
has_siblings = df[df[sibs_col] == 0]

movie_name = "The Lion King (1994)"

res = stats.mannwhitneyu(only_child[movie_name], has_siblings[movie_name], alternative="greater")
res.pvalue

# %matplotlib inline
fig, axs = plt.subplots(nrows=2, dpi=150, figsize=(10, 10))
axs[1].hist(only_child[movie_name], alpha=0.5, bins=9, label="only child", density=True)
axs[0].hist(has_siblings[movie_name], alpha=0.5, bins=9, label = "has siblings", density=True, color="red")
fig.legend(title="Sibling Status")
fig.suptitle("Rating CDFs: The Lion King" , fontsize=20)
plt.savefig("./ratings_distribution_lion_king.png", dpi=150)
plt.show()
