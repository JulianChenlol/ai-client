import praw
import json

# Create a Reddit instance
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
)

# Get the "mbti" subreddit
subreddit = reddit.subreddit("mbti")
# Filter posts with flair_name = "Survey/Poll"
filtered_posts = subreddit.search(query='flair_name:"Survey/Poll"', sort="new", time_filter="all")

polls = []
post = filtered_posts.__next__()
# print(post.title)
# print(post.poll_data)
# print(post.poll_data.options)
# print(post.poll_data.options[0].text)
# # Iterate over the filtered posts
for post in filtered_posts:
    poll = {}
    poll.setdefault("title", post.title)
    if not hasattr(post, "poll_data"):
        continue
    poll_data = post.poll_data
    options = poll.setdefault("options", [])
    for option in poll_data.options:
        options.append({"text": option.text, "votes": 0})
    polls.append(poll)
print(polls)
# Save the polls to a JSON file
with open("polls.json", "w") as f:
    json.dump(polls, f)
