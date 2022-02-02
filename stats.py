import requests, time, sched
import logging, logging.handlers, sys, os
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	datefmt="%d/%m/%y %H:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists("./logs"):
	os.makedirs("./logs")

fileHandler = logging.FileHandler(filename='logs/latest.log', encoding='utf-8')
fileHandler.setLevel(logging.INFO)
fileFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)

class Player:
	def __init__(self, name, url):
		self.name = name
		self.url = url

clan = "https://statsroyale.com/clan/L8CQVJGV"

def make_request(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': '*/*',
		'Accept-Language': 'fr,fr-FR;q=0.5',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': url,
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'TE': 'trailers',
	}
	return requests.get(url, headers=headers)

def refresh_profile(player):
	request = make_request(player.url + "/refresh")
	requestJson = request.json()
	success = requestJson['success']
	if(success):
		logger.info("✅  Refreshed {0} successfully".format(player.name))
	else:
		logger.error("⛔  Error occured during {0} refresh. Here's the request response: \n{1}".format(player.name, requestJson))

s = sched.scheduler(time.time, time.sleep)
def refresh_stats(): 
	logger.info("🕓  Refreshing statistics...")
	
	try:
		#refreshing clan
		refresh_profile(Player("Clan", clan))

		#refreshing players
		request = make_request(clan)
		soup = BeautifulSoup(request.content, 'html.parser')
		for element in soup.select('body > div.layout__page > div.layout__container > div > div.clan__table > div > div > a'):
			player = Player(element.getText(), element.get('href'))
			refresh_profile(player)
			time.sleep(3)
		logger.info("🕓  Done refreshing statistics. Next refresh in 30 minutes.")
		s.enter(60*30, 1, refresh_stats)
	except Exception as e:
		logger.exception(str(e))

s.enter(5, 1, refresh_stats)
logger.info("📢  Started!")
s.run()
