import praw
from time import sleep

cid = '4ru65rgvVEUzVg'
csecret = '20VKZGg_k3Kr7rF96ObO4jU49X4'
uagent = '1DSYB5fkfpAm6yYsA9TA5z9s32oQj5uGr2a4alpnBdw help me invest tool'
investment = '!invest {val}%'
authors = {'organic_crystal_meth', 'SlothySurprise', 'bleach_tastes_bad', 'lukenamop'}

class Investor(object):

  def __repr__(self):
    return "Name: {}\nInvesting amount: {}%".format(self.name, self.amount)

  def __init__(self, username, passwd, amount, replied=None):
    self.replied = replied
    self.name = username
    self.reddit = praw.Reddit(client_id=cid, client_secret=csecret, user_agent=uagent, username=username, password=passwd)
    self.amount = amount

  def find_posts(self):
    '''Finds posts posted by top MemeEconomists'''
    sub = self.reddit.subreddit("MemeEconomy")
    print 'Investor {} searching for posts...'.format(self.name)
    for submission in sub.new(limit=15):
      if submission.id not in self.replied:
        if submission.author in authors:
          print 'Investor {} found post by {}'.format(self.name, submission.author)
          self.replied.add(submission.id)
          return submission.id
    return None

  def invest(self, postID):
    '''Invests in posts that have the potential to go hot'''

    def find_comment_id(post):
      '''Inner function for finding the comment ID that the bot posts'''
      for comment in post.comments:
        if comment.author == "MemeInvestor_bot":
          return comment.id

    print 'Investing in post with id {}'.format(postID)
    post = self.reddit.submission(postID)
    post.downvote()
    bot_comment = find_comment_id(post)
    comment = self.reddit.comment(id=bot_comment)
    comment.reply(investment.format(val=self.amount))
    sleep(600)
    post.upvote()
