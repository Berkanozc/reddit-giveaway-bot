import time
import praw
from praw.exceptions import RedditAPIException
from praw.models import MoreComments

from config import REDDIT_CLIENT_ID, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_CLIENT_SECRET, META_MASK_WALLET_ADDRESS

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent="USERAGENT"
)


def reply_to_submission(given_submission):
    if "giveaway" in submission.title.strip().lower():
        # Check if we have a comment already on this submission
        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue
            if comment.author == REDDIT_USERNAME:
                break

        # Add message if not
        try:
            submission.reply(META_MASK_WALLET_ADDRESS)
            print("Comment placed on" + submission.title)
        except RedditAPIException:
            # Wait for timeout to finish and try again
            print("Limit reached waiting 10 minutes for next try")
            time.sleep(600)
            reply_to_submission(given_submission)
            print("Comment placed on" + submission.title)


subreddit = reddit.subreddit("NFTsMarketplace").controversial(time_filter="day")
for submission in subreddit:
    reply_to_submission(submission)
    time.sleep(0)
