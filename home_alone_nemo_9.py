sql = f"""
SELECT "Home Alone (1990)", "Finding Nemo (2003)"
FROM movies
"""
df = pd.read_sql(sql, con=conn).dropna()
home_alone_ratings = df["Home Alone (1990)"]#.dropna()
finding_nemo_ratings = df["Finding Nemo (2003)"]#.dropna()

stats.ks_2samp(home_alone_ratings, finding_nemo_ratings).pvalue
fig, axs = plt.subplots(ncols=2, dpi=300, figsize=(12, 10))

# axs[0].hist(home_alone_ratings, alpha=0.5, bins=9, label="Home Alone", density=True)
# axs[1].hist(finding_nemo_ratings, alpha=0.5, bins=9, label = "Finding Nemo", density=True, color="red")

sns.ecdfplot(home_alone_ratings, ax=axs[0], label="Home Alone")
sns.ecdfplot(finding_nemo_ratings, ax=axs[1], label="Finding Nemo", color="red")

fig.legend(title="Title")
fig.suptitle("Rating CDFs: Home Alone vs. Finding Nemo", fontsize=20)
plt.savefig("./Q9.png", dpi=300)
plt.show()
