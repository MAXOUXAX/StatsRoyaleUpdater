import requests, time, sched
import logging, logging.handlers, sys, os

logging.basicConfig(level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	datefmt="%d/%m/%y %H:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.ERROR)
consoleFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d/%m/%y %H:%M:%S")
consoleHandler.setFormatter(consoleFormatter)
logger.addHandler(consoleHandler)

if not os.path.exists("./logs"):
	os.makedirs("./logs")

fileHandler = logging.FileHandler(filename='logs/latest.log')
fileHandler.setLevel(logging.INFO)
fileFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)

class Player:
	def __init__(self, name, url):
		self.name = name
		self.url = url

players = [
	Player("Clan", "https://statsroyale.com/clan/L8CQVJGV"),
	Player("Garius912", "https://statsroyale.com/profile/2RQUC0U0"),
	Player("MAXOUXAX", "https://statsroyale.com/profile/LLRVUVPG"),
	Player("HunterGamer", "https://statsroyale.com/profile/PP0RPVUQ"),
	Player("Dj nast", "https://statsroyale.com/profile/LVL8JG2Y"),
	Player("Dj nast 2.0", "https://statsroyale.com/profile/2G8YL9QY9"),
	Player("KTelineSama", "https://statsroyale.com/profile/2R2R8GY2"),
	Player("BoZeY", "https://statsroyale.com/profile/Y8CY0RQPR"),
	Player("Nzosim", "https://statsroyale.com/profile/2G0UJ9L2"),
]

s = sched.scheduler(time.time, time.sleep)
def refresh_stats(): 
	logger.info("🕓  Refreshing statistics...")
	
	for player in players:
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
			'Accept': '*/*',
			'Accept-Language': 'fr,fr-FR;q=0.5',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
			'Referer': player.url,
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'TE': 'trailers',
		}
		request = requests.get(player.url + '/refresh', headers=headers)
		requestJson = request.json()
		success = requestJson['success']
		if(success):
			logger.info("✅  Refreshed {0} successfully".format(player.name))
		else:
			logger.error("⛔  Error occured during {0} refresh. Here's the request response: \n{1}".format(player.name, requestJson))
	logger.info("🕓  Done refreshing statistics. Next refresh in 30 minutes.")
	s.enter(60*30, 1, refresh_stats)

s.enter(5, 1, refresh_stats)
logger.info("📢  Started!")
s.run()
