#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name      : subtitle downloader
# Purpose   : One step subtitle download
#
# Authors   : Rao Saifullah
# Edited by : Rao Saifullah
# Created   :
# Copyright : (c) raosaif
# Licence   : GPL v3
#--------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib.request
import re
import urllib
from socket import error as SocketError
import errno
import time
import os
import sys
import getopt
import logging
import zipfile
from pathlib import Path

website_url = 'https://www.subscene.com'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def main(argv):
	# root, _ = os.path.splitext(sys.argv[0])
	# logging.basicConfig(filename=root + '.log', level=logging.INFO)
	# logging.info("Started with params " + str(sys.argv))

	def usage():
		print(('usage: %s [-b movieName] [-l language] [-h help] ...' % argv[0]))
		return 100
	try:
	    (opts, args) = getopt.getopt(argv[1:], 'b:l:h')
	except getopt.GetoptError:
		return usage()

	movie_name = ''
	subtitle_language = 'English'

	for (k, v) in opts:
		if k == '-b': 
			movie_name = v
		
		elif k =='-l':
			subtitle_language = v

		elif k == '-h':
			return usage()


	if len(argv) < 2:
		logging.error("Please Provide Movie Name.")
		print('Please Provide Movie Name')
		return usage()



	def get_url_response(url):

		html = ''
		try:
			req = urllib.request.Request(url, None, hdr)
			with urllib.request.urlopen(req) as response:
				html = response.read()
			return html

		except SocketError as e:
		    if e.errno != errno.ECONNRESET:
		        raise # Not error we are looking for
		    time.sleep(5) # Handle error here.

	# if '.' in movie_name:
	# 	movie_name = movie_name.replace('.', ' ')

	#print ('Movie Name: ', movie_name)
	#print ('Subtitle Language: ', subtitle_language)


	root, extension = os.path.splitext(movie_name)

	movie_formats = [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",".3g2"]
	if extension not in movie_formats:
		logging.error("File Extension is not supported.")
		logging.info("Supported File Formats: ")
		return  

	if os.path.exists(root + ".srt"):
		logging.info("Subtitles already available in the path. ")
		return

	j=-1
	root2=root
	for i in range(0,len(root)):
		if(root[i]=="\\" or root[i] =="/"):
			j=i
			break
	movie_name=root2[j+1:]
	root2=root2[:j+1]

	priority_list = ['aXXo','YIFY','RARBG','FXG','DIAMOND','iNTERNAL'] # In case your exact subtiles are not present, it will download the priority list

	priority_item = ''
	for item in range(len(priority_list)):
		if priority_list[item] in movie_name:
			priority_item = priority_list[item]

	movie_name_temp = ''
	if '.' in movie_name:
		movie_name_temp = movie_name.replace('.',' ')

	movie_name_split = movie_name_temp.split()
	#print('Split Text: ', movie_name_temp)

	html = get_url_response('http://subscene.com/subtitles/release?q='+movie_name)

	soup = BeautifulSoup(html,'lxml')

	subtitles_class= soup.find_all('div',class_=re.compile('subtitles'))
	tr_class = subtitles_class[0].find_all('table')[0].find_all('tbody')[0].find_all('tr')

	matched_subttile = 0
	present_priority_items = {}

	for tr in range(len(tr_class)):

		if tr_class[tr].find('div',class_='banner') == None: # sometimes subtitles website has banner in between so we need to check them
			#print('Length: ',len(tr_class[tr]))
			subtitle_title = tr_class[tr].find('span').find_next_sibling('span').string.strip()
			#print(subtitle_title)

			if (subtitle_title == movie_name): 
				href_link = tr_class[tr].find('a').get('href')
				#print('Subtitles Page: ', website_url+href_link)

				subtitle_title = tr_class[tr].find('span').find_next_sibling('span').string.strip()
				#print(subtitle_title)

				number_of_files = tr_class[tr].find('td',class_='a3')
				#print('Num Of Files: ',len(number_of_files.string.strip()))

				owner = tr_class[tr].find('td',class_='a5')
				if len(owner.contents) > 1:
					for content in range(len(owner.contents)):
						#print ('Owner-Log: ',repr(owner.contents[content]))
						if len(owner.contents[content]) > 1:
							pass
							#print(owner.contents[content].strip())
				else:
					pass
					#print('Owner Name: ',owner.string.strip())

				comments = tr_class[tr].find('td',class_='a6')
				#print('Comments: ',comments.div.string.strip())

				# Going to the download page
				soup_download = BeautifulSoup(get_url_response(website_url+href_link),'lxml')

				#print(soup_download.select('a[href^="/subtitle/download"]'))  #searching by css selecter

				link_to_download = website_url + soup_download.find(id='downloadButton')['href']

				#print('Link To download: ',link_to_download)
				logging.info("Priority List will be used " + tr_class[tr].find('a').get('href'))

				with open(subtitle_title + ".zip", "wb") as fo:
					fo.write(get_url_response(link_to_download))
				matched_subttile = matched_subttile + 1

			else:
				for item in range(len(priority_list)):
					if movie_name_split[0] in subtitle_title and movie_name_split[1]  in subtitle_title:
						if priority_list[item] in subtitle_title and tr_class[tr].find('span',class_=re.compile('positive')) and tr_class[tr].find('span',class_=re.compile('positive')).get_text().strip() == subtitle_language:
							present_priority_items[subtitle_title] = tr_class[tr].find('a').get('href')
							logging.warning("Priority List will be used " + tr_class[tr].find('a').get('href'))
		else:
			pass

	#print('Present: ',present_priority_items)

	#downloading from the priority list

	if matched_subttile == 0:

		for present_subtitles in present_priority_items:
			soup_download = BeautifulSoup(get_url_response(website_url+present_priority_items[present_subtitles]),'lxml')

			matched_subttile = matched_subttile + 1
			link_to_download = website_url + soup_download.find(id='downloadButton')['href']

			logging.warning("Priority List will be used " + present_subtitles)

			fileName = present_subtitles + ".zip"

			with open(fileName, "wb") as fo:
				fo.write(get_url_response(link_to_download))

			zip_ref = zipfile.ZipFile(fileName, 'r')
			zip_ref.extractall()
			zip_ref.close()
	
	if matched_subttile == 0:
		logging.error("Error in fetching subtitle for " + movie_name)		

if __name__ == '__main__':


	root, _ = os.path.splitext(sys.argv[2])
	
	fileName = root + '.log'

	logfile = Path(fileName)
	if logfile.is_file():
		os.remove(fileName)

	logging.basicConfig(filename=fileName, level=logging.INFO)
	logging.info("Started with params " + str(sys.argv))

	sys.exit(main(sys.argv))
