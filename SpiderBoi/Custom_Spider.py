import requests
import re
import urllib.parse as urlparse
import argparse
import threading
import logging
from bs4 import BeautifulSoup as bs4

target_links = []


def get_arg():
    """ Takes nothing
Purpose: Gets arguments from command line
Returns: Argument's values
"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug",dest="debug",action="store_true",help="Turn on debugging",default=False)
    parser.add_argument("-u","--url",dest="url",help="Single URL to spider")    
    parser.add_argument("-U","--urls",dest="urls",help="Name of file of urls to spider")
    parser.add_argument("-O","--output",dest="output",help="Name of file to output results")
    parser.add_argument("-r","--regex",dest="regex", action="append", nargs="*", help="Custom regex to look for (You can add as many as you'd like)")
    # parser.add_argument("-s","--sensor" dest="sensor" help="Sensor for core remover")
    # parser.add_argument("-x","--extra" dest="extra" action="store_true" help="Extra flag for extended options" default=False)
    options = parser.parse_args()
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return options


def extract_links(url):
    logging.debug("Crawling on {}".format(url))
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64;rv:78.0) Gecko/20100101 Firefox/78.0'
    }

    response = requests.get(url, headers=headers)

    if response:
        logging.debug("[+] {}".format(bs4(response.content)))
    return re.findall('(?:href=")(.*?)"',response.content.decode(errors="ignore"))


def crawl(url):
	logging.debug("Starting to crawl on {}".format(url))
	href_links = extract_links(url)
	for link in href_links:
		link = urlparse.urljoin(url, link)
		if "#" in link:
			link = link.split("#")[0]

		if url in link and link not in target_links:
			target_links.append(link)
			print("[+] " + str(link))
			crawl(link)


def main():
    options = get_arg()
    if options.url:
        crawl(options.url)
    elif options.urls:
        f = open("options.urls", "r")
        urls = f.read()
        for url in urls:
             t1 = threading.Thread(target=crawl, args=(url))
             t1.start()
             t1.join()
        logging.debug("Complete!")
    else:
        logging.fatal("Url(s) not given. Please add -u or -U to give me a target")


if __name__ == "__main__":
    main()
