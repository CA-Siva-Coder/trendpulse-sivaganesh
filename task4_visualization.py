# Task 4 — Visualizations
# TrendPulse: What's Actually Trending Right Now
"""

# Import required library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""### 1 — Setup"""
import pandas as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sns   

# Load data
csv_path = "Data/trends_analysed.csv"
story_data = pd.read_csv(csv_path)
story_data.head()

# Make sure outputs folder exists
os.makedirs("outputs", exist_ok=True)

"""### 2 — Chart 1: Top 10 Stories by Score"""

import seaborn as sns
import matplotlib.pyplot as plt
#Create a horizontal bar chart showing the top 10 stories by score
top_story = story_data.sort_values(by='score' , ascending = False ).head(10)
# Shorten titles longer than 50 characters
top_story['short_title'] = top_story['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
# Set figure size
plt.figure(figsize=(10,6))
# Create horizontal bar chart
sns.barplot(data=top_story, x='score', y='short_title', palette='dark',hue = 'short_title' )
# Add title and labels
plt.title('Top 10 HackerNews Stories by Score', fontsize=16)
plt.xlabel('Score', fontsize=12)
plt.ylabel('Story Title', fontsize=12)
# Adjust layout for readability
plt.tight_layout()
# Save chart to file
plt.savefig('outputs/chart1_top_stories.png', dpi=300)
# Show the plot
plt.show()

"""### 3 — Chart 2: Stories per Category

"""

#Create a bar chart showing how many stories came from each category
category_story  = story_data['category'].value_counts().sort_values(ascending = False).reset_index()
category_story.columns = ['category', 'count']
# Set figure size
plt.figure(figsize=(6,3))
# Create bar chart with different colors
sns.barplot(data=category_story, x='category', y='count', palette='bright',hue = 'category' )
# Add title and labels
plt.title('Number of Stories per Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Number of Stories', fontsize=12)
# Adjust layout
plt.tight_layout()
# Save chart
plt.savefig('outputs/chart2_categories.png', dpi=300)
# Show plot
plt.show()

"""### 4 — Chart 3: Score vs Comments (6 marks)

"""

# Create a scatter plot with score on the x-axis and num_comments on the y-axis
# Define colors for popular vs non-popular
plt.figure(figsize=(8,4))
# Scatter plot: score vs num_comments, colored by Is_popular
sns.scatterplot(
    data=story_data,
    x='score',
    y='num_comments',
    hue='Is_popular',
    palette={True:'green', False:'red'}
)
# Labels, title, legend
plt.xlabel('Score', fontsize=12)
plt.ylabel('Number of Comments', fontsize=12)
plt.title('Story Popularity: Score vs Comments', fontsize=14)
# Save as outputs/chart3_scatter.png
# Save and show
plt.savefig('outputs/chart3_scatter.png', dpi=300, bbox_inches='tight')
plt.show()

"""### Bonus — Dashboard  
* Combine all 3 charts into one figure:

"""

# Shorten long titles for readability
story_data['short_title'] = story_data['title'].str[:50] + '...'

# Create dashboard layout: 2 rows, 2 columns
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle("TrendPulse Dashboard", fontsize=22, fontweight='bold')

# ----------------------------
# Top-left: Top 10 stories by score
top_story = story_data.sort_values(by='score', ascending=False).head(10)
sns.barplot(data=top_story, x='score', y='short_title', palette='viridis', ax=axes[0,0] , hue = 'score')
axes[0,0].set_title('Top 10 Stories by Score', fontsize=14)
axes[0,0].set_xlabel('Score')
axes[0,0].set_ylabel('Title')

# ----------------------------
# Top-right: Stories per category
category_story = story_data['category'].value_counts().sort_values(ascending=False).reset_index()
category_story.columns = ['category','count']
sns.barplot(data=category_story, x='category', y='count', palette='Set2', ax=axes[0,1],hue ='category' )
axes[0,1].set_title('Stories per Category', fontsize=14)
axes[0,1].set_xlabel('Category')
axes[0,1].set_ylabel('Count')

# ----------------------------
# Bottom: Scatter plot score vs num_comments
sns.scatterplot(
    data=story_data,
    x='score', y='num_comments',
    hue='Is_popular',
    palette={True:'orange', False:'skyblue'},
    ax=axes[1,0],
    s=100
)
axes[1,0].set_title('Score vs Comments by Popularity', fontsize=14)
axes[1,0].set_xlabel('Score')
axes[1,0].set_ylabel('Number of Comments')
axes[1,0].legend(title='Is Popular')

# ----------------------------
# Hide bottom-right subplot (empty)
axes[1,1].axis('off')

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save dashboard
plt.savefig('outputs/dashboard.png', dpi=300)
plt.show()