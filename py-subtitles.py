#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import urllib
from socket import error as SocketError
import errno
import time
import os
import sys
import getopt

website_url = 'https://www.subscene.com'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def main(argv):
	print(argv)

	def usage():
		print(('usage: %s [-b movieName] ...' % argv[0]))
		return 100
	try:
	    (opts, args) = getopt.getopt(argv[1:], 'b:h')
	except getopt.GetoptError:
		return usage()


	for (k, v) in opts:

		if k == '-b': 
			movie_name = v

		else:
			return usage()

	if len(argv) < 2:
		print('Please Provide Movie Name')
		return usage()

	movie_name = ''

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

	movie_name = ''
	if '.' in movie_name:
		movie_name = movie_name.replace('.', ' ')

	driver = webdriver.Firefox() # user need to install geckodrive.
	#driver = webdriver.PhantomJS() # user can use PhantomJs also if they don't want firefox to run everytime.
	driver.get(website_url)

	elem_link = driver.find_element_by_name("q")
	elem_link.clear()
	elem_link.send_keys(movie_name)

	elem_link.send_keys(Keys.RETURN)

	while True:
		try:
			WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "search-result")))
			print('Page is processed Successfully....')
			break
		except TimeoutException:
			print ('Page is being Processed.....')

	html_page = driver.page_source
	driver.quit()

	title = ''
	priority_list = ['axxo','YIFY','RARBG','FXG','DIAMOND','iNTERNAL'] # In case your exact subtiles are not present, it will download the priority list
	subtiles_language = '/english'

	priority_item = ''
	for item in range(len(priority_list)):
		if priority_list[item] in movie_name:
			priority_item = priority_list[item]

	soup = BeautifulSoup(html_page,'lxml')
	#print(soup.prettify())

	search_tag = soup.find_all('div', class_='search-result')

	search_results = {}  # {'link', total_subtitles}

	li = search_tag[0].find_all('li')

	for result in range(len(li)):
		link_strings = li[result].find('a')
		link = ''
		count = ''

		if '(' in link_strings.contents[0]:
			link_strings.contents[0] = link_strings.contents[0].replace('(','')
		if ')' in link_strings.contents[0]:
			link_strings.contents[0] = link_strings.contents[0].replace(')','')

		# print(movie_name)
		# print(link_strings.contents[0])
		# print(link_strings)
		if link_strings.contents[0] in movie_name or link_strings.contents[0] == movie_name:

			link = link_strings['href']

			count_strings = li[result].find('div',class_=re.compile('subtle'))

			for string in count_strings.stripped_strings:
				if(len(string) > 4):
					count = string

			search_results[link] = count

	print('Search Result: ', search_results)
	present_priority_items = {}

	for key in search_results:

		soup= BeautifulSoup(get_url_response(website_url+key+subtiles_language),'lxml')

		subtitles_class= soup.find_all('div',class_=re.compile('subtitles'))
		tr_class = subtitles_class[0].find_all('table')[0].find_all('tbody')[0].find_all('tr')

		matched_subttile = 0

		for tr in range(len(tr_class)):
		#or tr in range(1):

			if tr_class[tr].find('div',class_='banner') == None: # sometimes subtitles website has banner in between so we need to check them
				#print('Length: ',len(tr_class[tr]))
				subtitle_title = tr_class[tr].find('span').find_next_sibling('span').string.strip()
				#print(subtitle_title)

				if (subtitle_title == movie_name): 
					print('YES: ',subtitle_title)
					href_link = tr_class[tr].find('a').get('href')
					#print('Subtitles Page: ', website_url+href_link)

					subtitle_title = tr_class[tr].find('span').find_next_sibling('span').string.strip()
					print(subtitle_title)

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

					with open(subtitle_title + ".zip", "wb") as fo:
						fo.write(get_url_response(link_to_download))
					matched_subttile = matched_subttile + 1
				else:
					for item in range(len(priority_list)):
						if priority_list[item] in subtitle_title and tr_class[tr].find('span',class_=re.compile('positive')):
							present_priority_items[subtitle_title] = tr_class[tr].find('a').get('href')

					print('------------No',subtitle_title)
			else:
				pass
				#print('*'*30 + 'Banner')

		print('Present: ',present_priority_items)
		#downloading from the priority list

		if matched_subttile == 0:

			for present_subtitles in present_priority_items:
				soup_download = BeautifulSoup(get_url_response(website_url+present_priority_items[present_subtitles]),'lxml')


				link_to_download = website_url + soup_download.find(id='downloadButton')['href']

				with open(present_subtitles + ".zip", "wb") as fo:
					fo.write(get_url_response(link_to_download))
			

if __name__ == '__main__':
    sys.exit(main(sys.argv))
