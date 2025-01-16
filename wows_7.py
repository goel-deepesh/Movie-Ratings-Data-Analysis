# these imports relevant for the rest of the problems
# %matplotlib inline
import operator
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
sns.set_style("whitegrid")

import dataframe_image as dfi

import sqlite3

from subprocess import call
# sets up sqllite database
call(["python", "setup.py"])

alpha = 0.005
conn = sqlite3.connect("movies.db")

sql = "SELECT * FROM movies LIMIT 1;"
cols = pd.read_sql(sql, con=conn).columns
social_col: str = cols[476]
sql = f"""
SELECT "The Wolf of Wall Street (2013)", "{social_col}"
FROM movies WHERE "{social_col}" IN (1, 0);
"""
df = pd.read_sql(sql, con=conn).dropna()
social_watchers = df[df[social_col] == 0]
nonsocial_watchers = df[df[social_col] == 1]

movie_name = "The Wolf of Wall Street (2013)"

res = stats.mannwhitneyu(social_watchers[movie_name], nonsocial_watchers[movie_name], alternative="greater")
res.pvalue

fig, axs = plt.subplots(ncols=2, dpi=300, figsize=(12, 10))

sns.ecdfplot(social_watchers[movie_name], ax=axs[0], label="Social")
sns.ecdfplot(nonsocial_watchers[movie_name], ax=axs[1], label="Non-Social", color="red")

fig.legend(title="Viewing Preference")
fig.suptitle("Rating CDFs: Wolf of Wall Street" , fontsize=20)
plt.savefig("./Q7.png", dpi=300)
plt.show()
