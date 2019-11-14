import praw #Python Reddit API Wrapper
import pprint #data pretty printer
from bs4 import BeautifulSoup #for webscrapping
import requests #for handling http requests 
import html5lib

class message: # object we'll use to store all the info a submission can give us along with the scrapped info
	
	def __init__(self, sub):
		self.title = sub.title
		self.url = sub.url
		self.score = sub.score
		self.author = sub.author
		
		
		
		

reddit = praw.Reddit(client_id='snkttga2QvG1Pg',client_secret='eTxtI098QqWOj0kRjJZm_iyGt0s',grant_type='client_credentials',user_agent='mytestscript/1.0')
subs = reddit.subreddit('news').hot(limit=1) #can extract the top 'limit' number of reddit posts; for now, 1

subs = [sub for sub in subs if not sub.domain.startswith('self.')] #convert from object to a list of submission objects 
sub = subs[0]

sub #submission object of a post on reddit
msg = message(sub)
url = msg.url

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib') 
print(soup.prettify().encode("utf-8")) 



'''
pprint.pprint([(s.score, s.title) for s in subs])
subs = [sub for sub in subs if not sub.domain.startswith('self.')]

for sub in subs:
	res = requests.get(sub.url)
	if (res.status_code == 200 and 'content-type' in res.headers and res.headers.get('content-type').startswith('text/html')):
		html = res.text
	
	#web-scrapping
	
	soup = BeautifulSoup(res.text, 'html.parser')# find the article title
	h1 = soup.body.find('h1')# find the common parent for <h1> and all <p>s.
	root = h1
	while root.name != 'body' and len(root.find_all('p')) < 5:
		root = root.parent 
		if len(root.find_all('p')) < 5: break# find all the content elements.
	ps = root.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre'])
	ps.insert(0, h1)    # add the title
	content = [tag2md(p) for p in ps]
	
	def tag2md(tag):
		if tag.name == 'p':
			return tag.text
		elif tag.name == 'h1':
			return f'{tag.text}\n{"=" * len(tag.text)}'
		elif tag.name == 'h2':
			return f'{tag.text}\n{"-" * len(tag.text)}'
		elif tag.name in ['h3', 'h4', 'h5', 'h6']:
			return f'{"#" * int(tag.name[1:])} {tag.text}'
		elif tag.name == 'pre':
			return f'```\n{tag.text}\n```
'''