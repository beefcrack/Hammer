#!/usr/bin/python2.7
#coding:utf-8

import os
import urllib2
import socket
from dummy import *

info = {
	'NAME':'Sub-Domain Scanning',
	'AUTHOR':'yangbh',
	'TIME':'20140709',
	'WEB':'',
	'DESCRIPTION':'子域名扫描',
	'VERSION':'1.0',
	'RUNLEVEL':0
}

def generateUrl(hosts=None):
	''''''
	# url redict  hasn't been considered
	urls = []
	tmpurls = []
	if hosts != None:
		for eachhost in hosts:
			url = 'http://' + eachhost
			tmpurls.append(url)
			url = 'https://' + eachhost
			tmpurls.append(url)
	print 'tmpurls:\t',tmpurls

	for url in tmpurls:
		try:
			print 'url=',url
			respone = urllib2.urlopen(url,timeout=10)
			redirected = respone.geturl()
			if redirected == url:
				urls.append(url)
			continue
		except urllib2.URLError,e:
			#print 'urllib2.URLError',e,url
			pass
		except urllib2.HTTPError,e:
			#print 'urllib2.HTTPError',e,url
			pass
		except urllib2.socket.timeout,e:
			#print 'urllib2.socket.timeout',e,url
			pass
		except urllib2.socket.error,e:
			#print 'urllib2.socket.error',e,url
			pass
	print 'urls:\t',urls
	
	return urls

def Audit(services):
	retinfo = {}
	output = ''
	# pprint(locals())
	# pprint(globals())
	if services.has_key('host') and 'issubdomain' not in services.keys():
		output += 'plugin run' + os.linesep
		subdomains = []
		# step1: get host domain
		# pos = services['host'].find('.')+1
		# domain = services['host'][pos:]
		domain = GetFirstLevelDomain(services['host'])
		
		# step2: get subdomains by knock
		if False:
			sb=SubDomain(domain)
			if 	sb.CheckForWildcard(sb.host) != False:
				pass

			sb.checkzone(sb.host)
			sb.subscan(sb.host,sb.wordlist)
			for eachdomain in sb.found:
				subdomains.append(eachdomain[1])
		
		# step3: get subdomains by bing
		# 
		
		# step4: get subdomains by baidu
		# 
		if True:
			try:
				th = TheHarvester(None)
				print 'domain=\t',domain
				tmp = th.getSubDomains(domain,'baidu',2)
				print 'result=\t',tmp
				try:
					for eachdomain in tmp:
						socket.gethostbyname(eachdomain)
						subdomains.append(eachdomain)
				except:
					pass
				print 'subdomains=\t',subdomains
			except:
				pass
		# step5: get subdomains by google
		# 
		
		# step6: get subdomains by sitedossier
		# 
		
		# step : combine subdomains
		tmp = list(set(subdomains))
		subdomains = tmp

		ret = subdomains
		retinfo = {'level':'info','content':ret}
		security_note(str(subdomains))

		if services['host'] not in subdomains:
			subdomains.append(services['host'])
		services['subdomains'] = subdomains

		# add sub scan task
		urls = generateUrl(subdomains)
		for url in urls:
			add_scan_task(url)

	# else:
	# 	output += 'plugin does not run' + os.linesep

	return (retinfo,output)
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
if __name__=='__main__':
	services = {'host':'www.eguan.cn'}
	pprint(Audit(services))
	pprint(services)