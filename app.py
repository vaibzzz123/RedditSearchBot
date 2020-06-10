import os
import praw
from string import Template
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

def generateHtmlForEmail(submission):
    templateString = Template('<h2><a href="$url">$title</a> <span style="color: #FF8C00;">↑$ups</span> <span style="color: #6495ED;">↓$downs:</span></h2><p style="text-overflow: ellipsis;">$body</p>\n')
    bodyTruncated = ""
    if len(submission.selftext) > 1000:
        bodyTruncated = submission.selftext[:1000] + "..."
    else:
        bodyTruncated = submission.selftext
    templateString = templateString.substitute(url="http://reddit.com" + submission.permalink, title=submission.title, ups=submission.ups, downs=submission.downs, body=bodyTruncated)
    return templateString


emailTemplate='<h1>Search results for "PS TV" in "GameSale" subreddit sorted by "New":</h1>\n'

reddit=praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                   client_secret=os.getenv("CLIENT_SECRET"),
                   username=os.getenv("USERNAME"),
                   user_agent="Reddit search bot script",
                   password=os.getenv("PASSWORD"))

subreddit=reddit.subreddit("GameSale")
results = subreddit.search("PS TV", sort="new")
max = 10
i = 1
for submission in results: # key details: title, permalink, shortlink, selftext, ups, downs
    emailTemplate += generateHtmlForEmail(submission)
    if i >= max:
        break
    i += 1

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
      "TextPart": "",
      "HTMLPart": emailTemplate,
      "CustomID": "RedditSearchBot"
    }
  ]
}

result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
