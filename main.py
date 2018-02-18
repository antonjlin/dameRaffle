import requests
from random import randint
import random
import names
from utils import *
import time
import threading
class OutOfProxies(Exception):
	''' Raised when the program runs out of proxies to use. '''

formattedProxies =  []

sizes = ["228556",
		"228557",
		"228558",
		"228559",
		"228560",
		"228561",
		"228562",
		"228563",
		"228564",
		"228565",
		"228566",
		"228567",
		"228568",
		"228569",
		"228570",
		"228571",
		"228572",
		"228573",
		"228574"]
def chooseProxy(tasknum):
	if tasknum + 1 <= len(proxieslines):
		proxy = proxieslines[tasknum].rstrip()
	if tasknum + 1 > len(proxieslines):
		if len(proxieslines) > 1:
			a = randint(1, len(proxieslines) - 1)
		if len(proxieslines) == 1:
			a = 0
		proxy = proxieslines[a].rstrip()
	try:
		proxytest = proxy.split(":")[2]
		userpass = True
	except IndexError:
		userpass = False
	if userpass == False:
		proxyedit = proxy
	if userpass == True:
		ip = proxy.split(":")[0]
		port = proxy.split(":")[1]
		userpassproxy = ip + ':' + port
		proxyedit = userpassproxy
		proxyuser = proxy.split(":")[2]
		proxyuser = proxyuser.rstrip()
		proxypass = proxy.split(":")[3]
		proxyuser = proxyuser.rstrip()
	if userpass == True:
		proxies = {'http': 'http://' + proxyuser + ':' + proxypass + '@' + userpassproxy,
				   'https': 'https://' + proxyuser + ':' + proxypass + '@' + userpassproxy}
	if userpass == False:
		proxies = {'http': 'http://' + proxy,
				   'https': 'https://' + proxy}
	global formattedProxies
	formattedProxies.append(proxies)

def importProxies():
	proxyfile = 'proxies.txt'
	p = open(proxyfile)
	global proxieslines
	proxieslines = p.readlines()
	numproxies = len(proxieslines)
	global formattedProxies
	if numproxies > 0:
		formattedProxies = []
		for i in range (0,len(proxieslines)):
			chooseProxy(i)
	if numproxies == 0:
		formattedProxies = [None]
	log(formattedProxies)
	log('{} proxies loaded'.format(numproxies))

class draw(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def enter_draw(self,first_name,last_name,email,password):
		'''
		Given an email <email>, an account is created on www.norsestore.com and
		the raffle for the adidas Dame 4 x BAPE is entered.
		'''

		# Sign up the account
		log("Signing up with email <" + str(email) + ">.")
		self.s = requests.session()

		self.link = "https://www.norsestore.com/account"

		self.headers = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US,en;q=0.9",
			"Cache-Control": "max-age=0",
			"Connection": "keep-alive",
			"Content-Length": "112",
			"Content-Type": "application/x-www-form-urlencoded",
			"DNT": "1",
			"Host": "www.norsestore.com",
			"Origin": "https://www.norsestore.com",
			"Referer": "https://www.norsestore.com/account?-return-url=https%3A%2F%2Fwww.norsestore.com%2Fdraw%2Fadidas-dame-4-x-a-bathing-apea",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
			}

		self.payload = {
			"formid": "register",
			"first_name": first_name,
			"surname": last_name,
			"email": str(email),
			"password": password,
			"password_repeat": password
		}

		try:
			self.random_proxy = random.choice(formattedProxies)
			# log(random_proxy)
		except:
			log("Ran out of proxies!")
			raise OutOfProxies

		# proxy= {
		# 	"http": random_proxy,
		# 	"https": random_proxy
		# 	}

		try:
			self.r = self.s.post(self.link, data=self.payload, headers=self.headers, proxies=self.random_proxy, timeout=15, verify=False)
		except Exception as e:
			# formattedProxies.remove(self.random_proxy)
			log(str(e))
			return

		# Enter the raffle
		log("Entering raffle with email <" + str(email) + ">.")
		self.link = "https://www.norsestore.com/draw/adidas-dame-4-x-a-bathing-apea"

		self.payload = {
			"formid": "draw",
			"item_pid": random.choice(sizes),
			"option:7": "on"
			}

		try:
			self.r = self.s.post(self.link, data=self.payload, headers=self.headers, proxies=self.random_proxy, timeout=15, verify=False)
		except Exception as e:
			# formattedProxies.remove(self.random_proxy)
			log(str(e))
			return

		# Check to see if the entry was successful
		flag = "You are participating in this draw." in self.r.text

		# Return whether or not the entry was successful
		return flag

	def run(self):
		self.first_name = names.get_first_name()
		self.last_name = names.get_last_name()
		self.email = self.first_name + "-" + self.last_name + domain
		self.success = self.enter_draw(self.first_name,self.last_name,self.email,password)
		if (self.success):
			global success
			success += 1
			cLog("Entry under email <" + self.email + "> succeeded.",'green')
		else:
			cLog("Entry under email <" + self.email + "> failed.",'red')
		global tries
		tries +=1
		cLog('[{}/{}] attempts succesfully entered'.format(success,tries),'yellow')
		global delay
		global successRate
		successRate = success/tries
		cLog('[Success rate: {} - Target rate: {} - Delay: {}] '.format(successRate,targetRate,delay),'yellow')
		# if successRate < targetRate:
		# 	delay+=1
		# else:
		# 	delay += -1


if(__name__ == "__main__"):
	# Ignore insecure messages
	requests.packages.urllib3.disable_warnings()

	password = input('password to create norse store accounts with: ')
	domain = input('domain: (include the @): ')
	entries = int(input('# of entries: '))
	importProxies()

	success = 0
	tries = 0
	delay = 1
	targetRate = 0.75
	successRate = 0.75
	for count in range(0, entries):
		# first_name = names.get_first_name()
		# last_name = names.get_last_name()
		# email = first_name + "-" + last_name + domain
		# for count in range(0,len(formattedProxies)):
		t= draw()
		t.start()
		time.sleep(delay)
		# log('{} threads started'.format(len(formattedProxies)))
		# time.sleep(1)
		# success = enter_draw(first_name, last_name, email, password)
		# if (success):
		# 	cLog("Entry under email <" + email + "> succeeded.", 'green')
		# else:
		# 	cLog("Entry under email <" + email + "> failed.", 'red')

		# enterOnce()
