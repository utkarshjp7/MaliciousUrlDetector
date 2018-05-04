from urlparse import urlparse
import re
import urllib2
import urllib
from xml.dom import minidom
import csv
import pygeoip

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

nf = -1

def get_stats(url):
        if url == '':
            return [0,0,0]
        token_word = re.split('\W+', url)
        no_ele=sum_len = largest=0
        for ele in token_word:
                l = len(ele)
                sum_len += l
                if l > 0:                                        ## for empty element exclusion in average length
                    no_ele += 1
                if largest < l:
                    largest = l
        try:
            return [float(sum_len)/no_ele,no_ele,largest]
        except:
            return [0, no_ele, largest]


def find_ele_with_attribute(dom,ele,attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return nf
        

def sitepopularity(host):
    xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url=' + host
    
    try:
        xml = urllib2.urlopen(xmlpath)
        dom = minidom.parse(xml)
        rank_host = find_ele_with_attribute(dom,'REACH','RANK')
        rank_country = find_ele_with_attribute(dom,'COUNTRY','RANK')
        return [rank_host,rank_country]
    except:
        return [nf,nf]

def count_sensitive_words(token_words):
    token_words = set(token_words)
    sensitive_words = set(['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin'])
    return len(token_words.intersection(sensitive_words))

def is_ipAddress(host):
    count = 0;
    for c in host:
        if unicode(c).isnumeric():
            count += 1
        else:
            if count >= 4 :
                return 1
            else:
                count = 0;
    if count >= 4:
        return 1
    return 0
    
def getASN(host):
    try:
        g = pygeoip.GeoIP('GeoIPASNum.dat')
        asn=int(g.org_by_name(host).split()[0][2:])
        return asn
    except:
        return  nf

def safebrowsing(url):
    api_key = "ABQIAAAA8C6Tfr7tocAe04vXo5uYqRTEYoRzLFR0-nQ3fRl5qJUqcubbrw"
    name = "URL_check"
    ver = "1.0"

    req = {}
    req["client"] = name
    req["apikey"] = api_key
    req["appver"] = ver
    req["pver"] = "3.0"
    req["url"] = url #change to check type of url

    try:
        params = urllib.urlencode(req)
        req_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?" + params
        res = urllib2.urlopen(req_url)

        if res.code==204:
            return 0
        elif res.code==200:
            # print "The queried URL is either phishing, malware or both, see the response body for the specific type."
            return 1
        elif res.code==204:
            print "The requested URL is legitimate, no response body returned."
        elif res.code==400:
            print "Bad Request The HTTP request was not correctly formed."
        elif res.code==401:
            print "Not Authorized The apikey is not authorized"
        else:
            print "Service Unavailable The server cannot handle the request. Besides the normal server failures, it could also indicate that the client has been throttled by sending too many requests"
    except:
        return -1

def extract(url_input):

    feature = {}
    tokens_words = re.split('\W+', url_input)       #Extract stings delimited by (.,/,?,,=,-,_)
    
    obj = urlparse(url_input)
    host = obj.netloc
    path = obj.path

    feature['URL']=url_input

    feature['rank_host'], feature['rank_country'] = sitepopularity(host)

    feature['host']=obj.netloc
    feature['path']=obj.path

    feature['Length_of_url']=len(url_input)
    feature['Length_of_host']=len(host)
    feature['No_of_dots']=url_input.count('.')

    feature['avg_token_length'], feature['token_count'], feature['largest_token'] = get_stats(url_input)
    feature['avg_domain_token_length'], feature['domain_token_count'], feature['largest_domain'] = get_stats(host)
    feature['avg_path_token'], feature['path_token_count'], feature['largest_path'] = get_stats(path)

    feature['sec_sen_word_cnt'] = count_sensitive_words(tokens_words)
    feature['IPaddress_presence'] = is_ipAddress(tokens_words)
    
    feature['ASNno']=getASN(host)
    feature['safebrowsing']=safebrowsing(url_input)

    return feature