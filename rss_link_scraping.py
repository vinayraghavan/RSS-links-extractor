import re
from bs4 import BeautifulSoup
import urllib2



def main_program(link_to_source, link_to_destination):
    all_urls = get_urls(link_to_source)
    for i in all_urls:
	rss_links = get_rss_links(i)
        write_to_file(rss_links, link_to_destination)


# extracts the all the urls from the specified file
def get_urls(input_path):    
    url_file = open(input_path)
    all_urls = []
    for lines in url_file:
        words = lines.split()
        for j in words:
            all_urls.append(j.replace(" ",""))
    return all_urls


# opens the specified urls and looks for RSS links
def get_rss_links(url):
    # the following 3 lines must be included incase of a WiFi proxy(e.g. college WiFi proxy)
    #proxy = urllib2.ProxyHandler({'http': '192.168.12.2:4480'}) #replace this with your own proxy settings
    #opener = urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)

    try:    
        raw_content = urllib2.urlopen(url)
    except:
        print "error in  opening link "+str(url)+"check your internet connection"
        return []

    html_content = raw_content.read()
    soup = BeautifulSoup(html_content)
    all_links = []; rss_links = []; plain_url = ""
    
    for raw_link in soup.find_all('a'):
        if check_rss_link(str(raw_link.get('href')), url) and raw_link.get('href') not in rss_links:
            rss_links.append(raw_link.get('href'))
    

    for raw_link in soup.find_all('link'):
        if check_rss_link(str(raw_link.get('href')), url) and raw_link.get('href') not in rss_links:
            rss_links.append(raw_link.get('href'))
        
    return rss_links


# checks if a link is a RSS link or not    
def check_rss_link(raw_link , url):
    plain_url1 = re.compile(r'(http[:][/][/])|(www[.])').sub('', url) #removes 'http' and 'www'
    plain_url = re.compile(re.escape(".")+'.*').sub('', plain_url1)   #removes everything after(and including) '.' (e.g. .com)
    
    conditions = ['feeds', 'feed/', 'feed.', 'rss']
    last_element= ('.css','.png','.js','.jpeg','.bmp','.jpg','.flv','.opml')
    for condition in conditions:
        if plain_url in raw_link and condition in raw_link and  not raw_link.lower().endswith(last_element) and not ('add.' in raw_link or 'ads.' in raw_link):
            return True
    return False


# writes all the RSS links to the specified output file
def write_to_file(rss_urls, output_file):
    rss_file = open(output_file,'a')
    for i in rss_urls:
        rss_file.write(str(i))
        rss_file.write("\n")
    rss_file.close()




#specify the input and output file paths
def take_inputs():
    input_file = input('Enter the path to source file containing the required urls:\n')
    output_file = input('Enter the path to destination file where the RSS links will be written:\n')
    main_program(input_file, output_file)

take_inputs()
