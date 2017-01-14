# ephemeral-tumblr
ephemeral-tumblr is a small script to delete all posts older than some amount, for example a month. This can be used to have a tumblr blog which beheaves more like Snapchat: your posts are only online for a brief period of time, and then they're gone.

this could also be used if you want to delete your embarrassing posts from 3 years ago, if you use `-a 94610000`.

If you don't want your precious posts to be lost forever, you can use this in conjunction with something like [`tumblr_backup`](https://github.com/bbolli/tumblr-utils/blob/master/tumblr_backup.md), and have a local copy of your blog before deletion.

It uses [pytumblr](https://github.com/tumblr/pytumblr), the official python tumblr API client, so you will need to install it first, and set up the OAuth permissions.

## usage:

```
usage: et.py [-h] [-y] [-a AGE] [-v] tumblr_url

positional arguments:
  tumblr_url         the url of the tumblr blog you want to process. For
                     example, eternal-glitter.tumblr.com

optional arguments:
  -h, --help         show this help message and exit
  -y                 don't ask for confirmation before deleting posts
  -a AGE, --age AGE  maximum age of a post in seconds. By default this is
                     2628000 s = one month
  -v                 verbose
```

