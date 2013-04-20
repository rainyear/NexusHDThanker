#!/usr/bin/python
#-*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests as req
import urllib, re, datetime, time

USER = '***'
PWD = '***'

ROOT = 'http://www.nexushd.org/'
loginPath = 'takelogin.php'
thankPath = 'thanks.php'
torrePath = 'torrents.php?sort=4&type=desc'

def login():
	cont = req.post(ROOT+loginPath, data={'username': USER, 'password': PWD})
	return cont.cookies
def thank(cookie, tid):
	print 'Thanks %s!' % tid
	try:
		req.post(ROOT+thankPath, data={'id': tid}, cookies=cookie)
	except:
		"""
		Max retries exceeded with url error...
		"""
		time.sleep(5)
		print 'pause a while...'
		req.post(ROOT+thankPath, data={'id': tid}, cookies=cookie)
def main():
	"""
	NexusHD thanker
	"""
	cookie = login()
	cont = req.get(ROOT+torrePath, cookies=cookie)
	detIDs = re.findall(r'details\.php\?id=(\d+)[\s\S]*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', cont.text)
	detIDs.sort(key=lambda x: x[0], reverse=True)
	logFile = open('log', 'r')
	loglines = logFile.readlines()
	logFile.close()
	latestID = int(loglines[-1].split('|')[-1])

	print 'Latest thanked ID: %s' % latestID

	log = '%s|%s\n' % (datetime.datetime.now().ctime(), detIDs[0][0])
	print 'Log: %s' % log

	for i in xrange(latestID+1, int(detIDs[0][0])):
		detUrl = ROOT+'details.php?id='+str(i)
		print 'Detail page url: %s' % detUrl
		thank(cookie, i)

	logFile = open('log', 'a')
	logFile.write(log)
	logFile.close()
if __name__ == '__main__':
	login()
	main()
