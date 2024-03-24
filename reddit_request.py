import pandas as pd
import requests
 
subreddit = 'programming'
limit = 1
timeframe = 'hour' #hour, day, week, month, year, all
listing = 'new' # controversial, best, hot, new, random, rising, top
class reddit():
    def get_reddit(subreddit,listing,limit,timeframe):
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
            request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        except:
            print('An Error Occured')
        return request.json()

    def get_post_titles(r):
        '''
        Get a List of post titles
        '''
        posts = []
        for post in r['data']['children']:
            x = post['data']['title']
            posts.append(x)
        return posts

    def get_results(r):
        '''
        Create a DataFrame Showing Title, URL, Score and Number of Comments.
        '''
        myDict = {}
        #for post in r['data']['children']:
        #    myDict[post['data']['title']] = {'url':post['data']['url'],'score':post['data']['score']}
        return r['data']['children'][0]['data']['title'] #gets the first post title in the list of children data