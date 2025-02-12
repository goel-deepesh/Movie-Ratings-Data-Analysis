alpha = 0.005
sql = f"""
SELECT
  "The Shining (1980)",
  "I like to be surprised even if it startles or scares me"
FROM
  movies
"""
df = pd.read_sql(sql, con=conn).dropna().assign(startle_enjoyer=lambda df: df["I like to be surprised even if it startles or scares me"] >= 4)

thrill_seeker_ratings = df[df.startle_enjoyer]["The Shining (1980)"]
thrill_avoider_ratings = df[~df.startle_enjoyer]["The Shining (1980)"]

stats.mannwhitneyu(thrill_seeker_ratings, thrill_avoider_ratings, alternative="greater").pvalue# < alpha
fig, axs = plt.subplots(ncols=2, dpi=300, figsize=(12, 10))

# axs[0].hist(home_alone_ratings, alpha=0.5, bins=9, label="Home Alone", density=True)
# axs[1].hist(finding_nemo_ratings, alpha=0.5, bins=9, label = "Finding Nemo", density=True, color="red")

sns.ecdfplot(thrill_seeker_ratings, ax=axs[0], label="Yes-responders")
sns.ecdfplot(thrill_avoider_ratings, ax=axs[1], label="No-responders", color="red")
fig.legend(title="Response Category")
fig.suptitle("Rating CDFs: The Shining", fontsize=20)
plt.savefig("./extra_credit.png", dpi=300, bbox_inches="tight", format="png")
plt.show()
