import requests
import re
import urllib.parse as urlparse
import argparse
import threading
import logging


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
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"',response.content.decode(errors="ignore"))


def crawl(url):
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
    if options.urls:
        f = open("options.urls", "r")
        urls = f.read()
        for url in urls:
             t1 = threading.Thread(target=crawl, args=(url))
             t1.start()
             t1.join()
        logging.debug("Complete!")


if __name__ == "__main__":
    main()
