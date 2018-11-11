from bs4 import BeautifulSoup
from selenium import webdriver
import re

def scrapeSite(domain, maxDepth):
    #navigates to all pages within depth of url
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
        print("visiting", page)

        depth = depths[page]
        pageSource = getSoup(page)

        #log it as visited
        visited.add(page)

        #add the addresses
        for address in getAddresses(pageSource):
            addresses.add(address)

        #add the links to the queue to visit
        if depth < maxDepth:
            links = getLinks(pageSource, domain)
            for link in links:
                if link not in visited and link not in toVisit:
                    toVisit.add(link)
                    depths[link] = depth + 1
                    print("adding", link, "to queue at depth", depth + 1)

    return list(addresses)

def getSoup(url):
    #returns the BeautifulSoup for url
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.close()
    return BeautifulSoup(html, 'html.parser')

def getLinks(soup, domain):
    #returns a list of links found in a soup that begin with domain
    ret = []
    for link in soup.find_all('a'):
        linkStr = link.get('href')
        if linkStr[0:len(domain)] == domain:
            ret.append(linkStr)
    return ret

def getAddresses(soup):
    #takes as input a soup that represents the source of a page
    #returns a list of possible addresses

    #soup.prettify()
    #soup =
    ptrn = '([0-9]+ [a-zA-Z0-9].{,100} [0-9]{5})[^0-9]'
    #re.findall(ptrn, soup)

    text_file = open("output.txt", "w", encoding="utf-8")
    text_file.write(soup.prettify())
    text_file.close()

    return re.findall(ptrn, str(soup.prettify), re.DOTALL)





#url = 'https://www.crunchbase.com/hub/san-francisco-seed-stage-companies/top/org_top_rank_delta_d30_list#section-leaderboard'
#url = 'https://www.crunchbase.com'
#url = 'https://www.crunchbase.com/hub/united-states-companies-founded-in-the-last-year'

#driver = webdriver.Chrome()
#driver.get(url)
#html = driver.page_source
#driver.close()

#soup = BeautifulSoup(html)
#outputString = soup.prettify()

#addresses = scrapeSite('https://www.brightmachines.com/', 3)

addresses = getAddresses(getSoup('https://www.brightmachines.com/contact-us-2/'))
for address in addresses:
    print(address)


#text_file = open("output.txt", "w", encoding="utf-8")
#text_file.write(outputString)
#text_file.close()
