#--------------Task 1 data collection -----------------

# Import required modules
import requests
import json
from datetime import datetime
import time
import os

# -----------------------------
# Define API URL
STORIESURL = "https://hacker-news.firebaseio.com/v0/topstories.json"

# -----------------------------
# Expanded category keywords
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global", "un", "politics"],
    "sports": [
        "nfl", "nba", "fifa", "sport", "team", "player", "league", "championship",
        "cricket", "soccer", "tennis", "olympics", "football", "hockey", "baseball",
        "rugby", "golf", "formula 1", "f1", "wimbledon", "world cup", "super bowl",
        "champions league", "nba finals", "ncaa", "mlb", "soccer world cup"
    ],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome", "chemistry"],
    "entertainment": ["movie", "film", "music", "netflix", "book", "show", "award", "streaming", "concert", "series"]
}

# -----------------------------
# Initialize category counters EARLY (important)
category_counts = {cat: 0 for cat in list(CATEGORY_KEYWORDS.keys()) + ["Other"]}
max_per_category = 25
all_story = []

# -----------------------------
# Function to assign category
def assign_category(title):
    if not title:
        return "Other"
    title = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in title for word in keywords):
            return category
    return "Other"

# -----------------------------
# Function to fetch story with retry
def fetch_story(story_id, retries=1):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    headers = {"User-Agent": "TrendPulse/1.0"}

    for attempt in range(retries + 1):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.json()
        except requests.exceptions.RequestException as e:
            print(f"Error for ID {story_id}: {e}, retrying...")
            time.sleep(2)

    return None

# -----------------------------
# Fetch top story IDs
try:
    response = requests.get(STORIESURL, headers={"User-Agent": "TrendPulse/1.0"})
    if response.status_code == 200:
        storyids = response.json()[:500]
        print("Number of story IDs fetched:", len(storyids))
    else:
        print("Error fetching IDs:", response.status_code)
        storyids = []
except Exception as e:
    print("Fatal error:", e)
    storyids = []

# -----------------------------
# Main loop
for id in storyids:
    story = fetch_story(id)

    if not story or story.get("type") != "story":
        continue

    title = story.get("title", "")
    category = assign_category(title)

    if category not in category_counts:
        category = "Other"

    if category_counts[category] < max_per_category:
        story_data = {
            "Post_id": story.get("id"),
            "title": title,
            "author": story.get("by", "unknown"),
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "category": category,
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        all_story.append(story_data)
        category_counts[category] += 1

    # stop if all full
    if all(count >= max_per_category for count in category_counts.values()):
        break

    time.sleep(0.2)

# -----------------------------
# Save files
os.makedirs("data", exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/trends_{timestamp}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_story, f, ensure_ascii=False, indent=2)

latest_file = "data/trends_latest.json"
with open(latest_file, "w", encoding="utf-8") as f:
    json.dump(all_story, f, ensure_ascii=False, indent=2)

# -----------------------------
# Final output (this will NOT error now)
print(f"{filename} created successfully")
print(f"{latest_file} updated successfully")
print(f"Total posts collected: {len(all_story)}")
print("Posts per category:", category_counts)