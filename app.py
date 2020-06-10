import os
import praw
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

def generateHtmlForEmail(submission):


mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_API_SECRET")), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "vaib.kapoor15@gmail.com",
        "Name": "Vab"
      },
      "To": [
        {
          "Email": "vaib.kapoor15@gmail.com",
          "Name": "Vab"
        }
      ],
      "Subject": "Reddit search bot results",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "RedditSearchBot"
    }
  ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())

# reddit=praw.Reddit(client_id=os.getenv("CLIENT_ID"),
#                    client_secret=os.getenv("CLIENT_SECRET"),
#                    username=os.getenv("USERNAME"),
#                    user_agent="Reddit search bot script",
#                    password=os.getenv("PASSWORD"))

# subreddit=reddit.subreddit("GameSale")
# results = subreddit.search("PS TV", sort="new")
# max = 10
# i = 1
# for submission in results: # key details: title, permalink, shortlink, selftext, ups, downs
#     print(submission.title)
#     print(submission.permalink)
#     print(submission.shortlink)
#     print(submission.selftext)
#     print(submission.ups)
#     print(submission.downs)
#     if i >= max:
#         break
#     i += 1
