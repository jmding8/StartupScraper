from bs4 import BeautifulSoup
from selenium import webdriver
import re

def scrapeDomain(domain, maxDepth):
    #navigates to all pages within maxDepth of domain, staying within the domain
    #returns a list of all unique addresses found while navigating

    toVisit = set()
    toVisit.add(domain)
    depths = {}
    depths[domain] = 0
    visited = set()

    addresses = set()

    while len(toVisit) > 0:
        #visit the page
        page = toVisit.pop()
        print("visiting", page + ",", len(toVisit), "remaining")

        depth = depths[page]
        pageSource = getSoup(page)

        #log it as visited
        visited.add(page)

        #add the addresses
        for address in getAddresses(pageSource):
            addresses.add(address)

        #add the links to the queue to visit
        if depth < maxDepth:
            links = getLinks(pageSource)
            for link in links:
                try:
                    if link not in visited and link not in toVisit and inDomain(link, domain):
                        toVisit.add(link)
                        depths[link] = depth + 1
                        print("adding", link, "to queue at depth", depth + 1)
                except:
                    print("adding link", link, "failed")

    return list(addresses)

def getSoup(url):
    #returns the BeautifulSoup for url
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return BeautifulSoup(html, 'html.parser')

def getLinks(soup):
    #returns a list of links found in a soup that begin with domain
    ret = []
    for link in soup.find_all('a'):
        ret.append(link.get('href'))
    return ret

def inDomain(url, domain):
    #print("inDomain:", url, domain)
    return url[0:len(domain)] == domain

def getAddresses(soup):
    #takes as input a soup that represents the source of a page
    #returns a list of possible addresses

    ptrn = '([0-9]+ [a-zA-Z0-9].{,100} [0-9]{5})[^0-9]'
    return re.findall(ptrn, str(soup.prettify), re.DOTALL)




#url = 'https://www.crunchbase.com/hub/united-states-companies-founded-in-the-last-year'
url = input('starting domain?')
addresses = scrapeDomain(url, 3)
for address in addresses:
    print(address)
