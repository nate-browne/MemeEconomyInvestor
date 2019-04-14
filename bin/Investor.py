import praw
from time import sleep
from random import randint

class Investor(object):

  investment = '!invest {val}%'

  def __repr__(self):
    return "Name: {}\nInvesting amount: {}%".format(self.name, self.amount)

  def __init__(self, username, passwd, amount, cid, csecret, uagent):
    self.replied = list()
    self.name = username
    self.reddit = praw.Reddit(client_id=cid, client_secret=csecret, user_agent=uagent, username=username, password=passwd)
    self.sub = self.reddit.subreddit("MemeEconomy")
    self.amount = amount
    self.authors = [ # change the next line to add/remove authors
    'organic_crystal_meth', 'SlothySurprise', 'bleach_tastes_bad', 'lukenamop'
    ]

  def find_posts(self):
    '''Finds posts posted by top MemeEconomists'''

    print 'Investor {} searching for posts...'.format(self.name)

    for submission in self.sub.new(limit=5):
      if submission.id not in self.replied:
        if submission.author in self.authors:
          print 'Investor {} found post by {}'.format(self.name, submission.author)
          self.replied.append(submission.id)
          return submission.id
    return None

  def invest(self, postID):
    '''Invests in posts that have the potential to go hot'''

    def find_comment_id(post):
      '''Inner function for finding the comment ID that the bot posts'''
      for comment in post.comments:
        if comment.author == "MemeInvestor_bot":
          return comment.id

    print 'Investor {} investing in post with id {}'.format(self.name, postID)
    try:
      post = self.reddit.submission(postID)
      post.downvote()
      sleep(randint(1, 10)) # Sleep for a random period of time between 1 and 10 seconds
      bot_comment = find_comment_id(post)
      comment = self.reddit.comment(id=bot_comment)
      comment.reply(Investor.investment.format(val=self.amount))
      post.upvote()
    except TypeError:
      print 'Investor {} missed investment with id {} (type error)'.format(self.name, postID)