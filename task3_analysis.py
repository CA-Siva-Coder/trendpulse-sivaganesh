## Task 3 — Analysis with Pandas & NumPy
### TrendPulse: What’s Actually Trending Right Now
"""

# import required Library
import pandas as pd
import numpy as np
import os
from datetime import datetime

"""### 1 — Load and Explore"""
import pandas as pd
import os
# Load data/trends_clean.csv into a Pandas DataFrame
story_clean = "data/story_list_clean_latest.csv"
story_df = pd.read_csv(story_clean)
story_df

# Print the first 5 rows
story_df.head()

# Print the shape of the DataFrame (rows and columns)
print("No of rows:",story_df.shape[0])
print("No of columns:",story_df.shape[1])

# Print the average score across all stories
avg_score = story_df['score'].mean()
print("The Average score across all stories : ",round(avg_score,2))

# Print the average num_comments across all stories
avg_comment = story_df['num_comments'].mean()
print("The Average num_comments across all stories : ",round(avg_comment,2))

"""### 2 — Basic Analysis with NumPy"""

# What is the mean, median, and standard deviation of score?
score_mean = round(story_df['score'].mean(),2)
score_median = round(story_df['score'].median(),2)
score_std = round(story_df['score'].std(),2)
print("Mean of Score  :",score_mean)
print("Median of Score  :",score_median)
print("standard deviation of Score  :",score_std)

# What is the highest score and lowest score?
high_score = story_df['score'].max()
low_score = story_df['score'].min()
print("Highest score  :",high_score)
print("Lowest score   :",low_score)

# Which category has the most stories?
most_story_category  =  story_df.groupby('category')['Post_id'].count()
print(f" The category {most_story_category.idxmax() } has the most story : {most_story_category.max()}")

# Which story has the most comments? Print its title and comment count.
most_comment_story = story_df.loc[story_df['num_comments'].idxmax()]
most_comment_story
print(f"{most_comment_story['title']}   has the most comments  {most_comment_story['num_comments']} ")
# Print title and comment count
print("Title:", most_comment_story['title'])
print("Number of comments:", most_comment_story['num_comments'])

"""### 3 — Add New Columns

* Add these two new columns to your DataFrame:

 * Engagement : num_comments / (score + 1) — how much discussion a story gets per upvote
 * Is_popular : True if score > average score, else False
"""

# Add Engagement column :
# how much discussion a story gets per upvote
story_df['Engagement'] = story_df['num_comments']/(story_df['score'] +1)
story_df['Engagement'] = story_df['Engagement'].round(2)
story_df['Engagement']

# Is_popular True if score > average score, else False
story_df['Is_popular'] = story_df['score'] > avg_score
story_df['Is_popular']

story_df.head()

"""### 4 — Save the Result"""

# Create folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save the updated DataFrame
filename = "data/trends_analysed.csv"
story_df.to_csv(filename, index=False)

# Print confirmation message
print(f"{filename} saved successfully with {story_df.shape[0]} rows and {story_df.shape[1]} columns")