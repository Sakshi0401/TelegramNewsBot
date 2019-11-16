import praw #Python Reddit API Wrapper
import pprint #data pretty printer
import requests #for handling http requests 
from newspaper import Article 
import time
import schedule


def telegram_bot_sendtext(bot_message):
	bot_token = '906577902:AAH6Om6rpTes0PKUzGDlVtYBQtRAg5B73sc'
	bot_chatID = '-342736590'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
	response = requests.get(send_text)
	return response.json()

def telegram_message(author, upvotes, title, summary, url):
	title = '*'+title+'* \n\n'
	author = '_News sourced from r/news. \nAuthor: '+author.name+' \nNumber of Upvotes: '+str(upvotes)+'_'
	url = '\n\nClick here to read the whole article: '+url+'\n\n'
	
	return title + summary + url + author
	
def report():
	reddit = praw.Reddit(client_id='snkttga2QvG1Pg',client_secret='eTxtI098QqWOj0kRjJZm_iyGt0s',grant_type='client_credentials',user_agent='mytestscript/1.0')
	subs = reddit.subreddit('worldnews').hot(limit=5) #can extract the top 'limit' number of reddit posts
	subs = [sub for sub in subs if not sub.domain.startswith('self.')]#convert from object to a list of submission objects 

	for sub in subs:
		url = sub.url 
		print(sub.url+'\n')
		article = Article(url, language="en") # en for English 
		article.download() 
		article.parse() 
		article.nlp() 
		  
		title = article.title
		text = article.text
		summary = article.summary
		
		telegram_bot_sendtext(telegram_message(sub.author,sub.score, title, summary, url))
		
		time.sleep(60)

def main():
	schedule.every().day.at("14:00").do(report)

	while True:
		schedule.run_pending()
		time.sleep(1)
	
if __name__== "__main__":
  main()	
	
#https://api.telegram.org/bot906577902:AAH6Om6rpTes0PKUzGDlVtYBQtRAg5B73sc/getUpdates
