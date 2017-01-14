#!/usr/bin/env python2
import argparse
import time
import pytumblr

import sys

import oauth2
import urlparse

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

SECS_IN_MONTH = 2628000

parser = argparse.ArgumentParser()
parser.add_argument("tumblr_url", help="the url of the tumblr blog you want to process. For example, eternal-glitter.tumblr.com")
parser.add_argument("-y", help="don't ask for confirmation before deleting posts", action="store_true")
parser.add_argument("-a", "--age", type=int, help="maximum age of a post in seconds. By default this is %d s = one month" % (SECS_IN_MONTH), default=SECS_IN_MONTH)
parser.add_argument("-v", help="verbose", action="store_true")

args = parser.parse_args()

# Authenticate via OAuth (we need it to delete)
client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET
)

old_posts = [] # we will store here the posts to be deleted
earliest_date = int(time.time()-args.age)

ofst = 0 # offset from the first post
data = client.posts(args.tumblr_url, offset=ofst)
l = len(data['posts']) # number of posts in the response
total_posts = data['blog']['total_posts']

print 'processing posts...'
while l != 0: # we get a response with 0 posts once we get to the end of the blog.
    data = client.posts(args.tumblr_url, offset=ofst)
    for p in data['posts']:
        if p['timestamp'] < earliest_date:
            old_posts.append(p)
    l = len(data['posts'])
    ofst += l
    if args.v:
        print '%d of %d' % (ofst, total_posts)

if args.v:
    print 'here are all the posts that will be deleted:'
    for p in old_posts:
        print '%s \t %s' % (p['post_url'], p['summary'])
    print '\n'
    
if not args.y:
    sure = query_yes_no('are you sure you want to delete %d posts out of the %d posts from %s ?' % (len(old_posts), total_posts, args.tumblr_url))
    if not sure:
        sys.exit()

print 'deleting %d posts from %s...' % (len(old_posts), args.tumblr_url)
old_posts.reverse()
for p in old_posts:
    if args.v:
        print '\t deleting %d' % p['id']
    response = client.delete_post(args.tumblr_url, p['id'])
    if not 'id' in response:
        print '%d: %d\t%s' % (p['id'], response['meta']['status'], response['meta']['msg']

print 'done'
    
