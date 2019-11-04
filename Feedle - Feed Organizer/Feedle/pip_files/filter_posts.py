import requests
from bs4 import BeautifulSoup
import tweepy

# import user keys for twitter
from pip_files.twitter_keys import *


def get_filt_posts(user_priority):

    if user_priority == []:
        return ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    # website URLS
    twitter_base_url = 'http://ethans_fake_twitter_site.surge.sh/'
    quote_base_url = 'http://quotes.toscrape.com/'

    # scrapping data from quote website
    quote_url = quote_base_url
    # to store all posts from quotes
    quote_posts_db = []

    # for scrapping data from all pages
    for i in range(100):

        # request to quote page
        quote_page = requests.get(quote_url, headers=headers)

        # scrap data from quote page
        quote_data = BeautifulSoup(quote_page.content, 'html.parser')

        # to store data of all posts in desired format
        for posts in quote_data.findAll('div', attrs={"class": "quote"}):
            post_object = {
                "content": posts.find('span', attrs={"class": "text"}).text.encode('utf-8'),
                "author": posts.find('small', attrs={"class": "author"}).text.encode('utf-8')
            }
            quote_posts_db.append(post_object)

        # find next page
        next_url = quote_data.find('li', attrs={"class": "next"})
        if (next_url == None):
            break
        next_url = next_url.findAll('a')
        next_url = next_url[0].get('href')

        quote_url = quote_base_url+next_url

    # scrapping of data from fake twitter

    # scrapping data from quote website
    twitter_url = twitter_base_url
    # to store all posts from twitter
    twitter_posts_db = []

    # for scrapping data from all pages
    for i in range(100):

        # request to twitter page
        twitter_page = requests.get(twitter_url, headers=headers)

        # scrap data from twitter page
        twitter_data = BeautifulSoup(twitter_page.content, 'html.parser')

        # to store data of all posts in desired format
        for posts in twitter_data.findAll('div', attrs={"class": "tweetcontainer"}):
            post_object = {
                "author":  posts.find('h2', attrs={"class": "author"}).text.encode('utf-8'),
                "date":  posts.find('h5', attrs={"class": "dateTime"}).text.encode('utf-8'),
                "content":  posts.find('p', attrs={"class": "content"}).text.encode('utf-8'),
            }
            twitter_posts_db.append(post_object)

        # find next page
        next_url = twitter_data.find('li', attrs={"class": "next"})
        # to check there is next page
        if (next_url == None):
            break
        next_url = next_url.findAll('a')
        next_url = next_url[0].get('href')

        twitter_url = twitter_base_url+next_url

    filt_post = {'ftwitter': [], 'quote': [], 'twitter': []}
    # to filter twitter post
    for post in twitter_posts_db:
            # to check is post is in user priority list
        for user in user_priority:
            if user.lower() in str(post['content']).lower():
                # to store all filtered posts
                temp = {
                    'website': 'F_Twitter',
                    'user': user,
                    'content': str(post['content'])[2:],
                }
                filt_post['ftwitter'].append(temp)

    # to filter quote post
    for post in quote_posts_db:
        # to check is post is in user priority list
        for user in user_priority:
            if user.lower() in str(post['author']).lower():
                # to store all filtered posts
                temp = {
                    'website': 'Quote',
                    'user': user,
                    'content': str(post['content'])[14:-13]
                }
                filt_post['quote'].append(temp)

    # to scrap data from twitter

    # funtion to convert user name

    def conv_twt_uname(str):
        ret = ''
        for char in str:
            if char != ' ':
                ret += char
        return ret

    # authentication of twitter app
    class auth_twitter_app():

        def auth_app(self):
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_tkn_secret)
            return auth

    # making a twitter cilent
    class twitter_client():
        def __init__(self):
            self.auth = auth_twitter_app().auth_app()
            # to set the request limit so twitter dont reject scrapping
            self.twitter_client = tweepy.API(
                self.auth, wait_on_rate_limit=True)

        def get_home_timeline(self, num_tweets):

            # to check posts/tweets from user home timeline
            for tweet in tweepy.Cursor(self.twitter_client.home_timeline, screen_name='text').items(num_tweets):

                # to check the post acc to user priority
                for user in user_priority:
                    if tweet.user.screen_name.lower() == conv_twt_uname(user).lower():
                        temp = {
                            'website': 'Twitter',
                            'user': user,
                            'content': tweet.text
                        }
                        filt_post['twitter'].append(temp)

    limit = 10

    #to store posts

    #twitter_client.get_home_timeline(limit)     # <---uncomment this line to activate twitter features
    #twitter_client = twitter_client()           # <---uncomment this line to activate twitter features

    return filt_post
