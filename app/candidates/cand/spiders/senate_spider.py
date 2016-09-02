import scrapy
import logging, sys
from cand.items import CandItem

# This script contains spiders to crawl different page from ballotpedia.org
# Spider1 parse out state links
# Spider2 parse the majority of candidate
# Spider3 parse only general election candidates
# Spider4 pase FL, NH as they have different html layout

# Note: NY senators have multiple party
# https://ballotpedia.org/United_States_Senate_election_in_New_York,_2016

class SenateSpider1(scrapy.Spider):
    name = "senate1"
    allowed_domains = ["ballotpedia.org"]
    start_urls = ["https://ballotpedia.org/United_States_Congress_elections,_2016"]

    def parse(self, response):
	# grep 50 state's info
        for i, href in enumerate(response.xpath('//table[@class="infobox"]/descendant::node()/a[contains(@href, "United_States_Senate_election_in")]/@href').extract()):
            url = response.urljoin(href)
            print i+1, url 

class SenateSpider2(scrapy.Spider):
    name = "senate2"
    allowed_domains = ["ballotpedia.org"]
    #start_urls = ["https://ballotpedia.org/United_States_Senate_election_in_California,_2016"]
    start_urls = ["https://ballotpedia.org/United_States_Senate_election_in_Alabama,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Alaska,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Arizona,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Arkansas,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_California,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Colorado,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Connecticut,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Georgia,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Hawaii,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Idaho,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Illinois,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Indiana,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Iowa,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Kansas,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Kentucky,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Louisiana,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Maryland,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Missouri,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Nevada,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_New_York,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_North_Carolina,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_North_Dakota,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Ohio,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Oklahoma,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Oregon,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Pennsylvania,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_South_Carolina,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_South_Dakota,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Utah,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Vermont,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Washington,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Wisconsin,_2016"]


    def parse(self, response):
        i=1
        for href in response.xpath('//a[contains(@href, "Independent") or contains(@href, "Libertarian") or contains(@href, "Republican_Party") or contains(@href, "Democratic_Party") or contains(@href, "Green_Party") or contains(@href, "Peace_and_Freedom_Party") or contains(@href, "Equality_Party") or contains(@href, "Working_Families_Party") or contains(@href, "Independence_Party_of_America") or contains(@href, "Conservative_Party") or contains(@href, "Reform_Party") or contains(@href, "Constitution_Party")]'):
            party = href.xpath('./@title').extract()[0]
            logging.info('Party: %s', party)
            ccurl = href.xpath('following-sibling::a/@href').extract()
            if len(ccurl) >= 1:
                logging.debug('candidates url found: %s', ccurl)
                curl = ccurl[0]
            else:
                logging.debug('no candidate found')
                continue
            logging.info("Processing person #%d", i)
            i+=1
            name = curl.replace("_", " ")[1:] 
            cand_urls = response.urljoin(curl)
            logging.info('Candidate url: %s', cand_urls)
            item = CandItem()
            item['name'] = name
            item['url'] = cand_urls
            item['party'] = party #TODO: remove party as parse_cand now handle it
            item['chamber'] = 'S'
            yield scrapy.Request(cand_urls, callback=self.parse_cand, meta={'item':item}) 


    def parse_cand(self, response):
        item = response.meta['item']
        logging.debug('grab picure...')
        for p in response.xpath('//table[@class="infobox"]/descendant::node()/@src'):
            item['pic'] = response.urljoin(p.extract())
            logging.info('pic: %s', p.extract())
            break 

        # Put district number 0 for senators so that later we use this to match sunlight's candidate data
        item['dist'] = '0'
        #logging.debug('grab district...')
        #for dist in response.xpath('//a[contains(@href, "Congressional_District")]/text()'):
        #    d = dist.extract().split()[1]
        #    item['dist'] = d
        #    logging.info('dist: %s', d)
        #    break

        logging.debug('grab party...')
        for l in response.xpath('//table[@class="infobox"]//a[contains(@href, "Independent") or contains(@href, "Libertarian") or contains(@href, "Republican") or contains(@href, "Democratic") or contains(@href, "Green") or contains(@href, "Peace_and_Freedom") or contains(@href, "Equality") or contains(@href, "Working_Families") or contains(@href, "Independence_of_America") or contains(@href, "Conservative") or contains(@href, "Reform") or contains(@href, "Constitution")]'):
            party = l.xpath('./@href').extract()[0]
            item['party'] = party[1:]
            logging.info('party: %s', party)
            break

        logging.debug('grab incumbent...')
        item['incumbent'] = False
        for l in response.xpath('//table[@class="infobox"]//td[contains(text(), "Incumbent")]'):
            item['incumbent'] = True
            logging.info('is Incumbent!')

        logging.debug('grab state...')
        for l in response.xpath('//*[@id="bodyContent"]/a[contains(@href, "U.S._Senate_elections") or contains(@href, "United_States_Senate")] | //*[@id="bodyContent"]/p/a[contains(@href, "U.S._Senate_elections")]'):# this line is for you Patrick Murphy!
            logging.debug('selector, node before state: %s', l)
            h = l.xpath('following-sibling::a/@href').extract()[0][1:].replace('_',' ')
            logging.info('state: %s', h)
            item['state'] = h
            break

        logging.debug('grab campaign website...')
        for l in response.xpath('//a[@class="external text" and contains(text() ,"Campaign")]/@href'):
            logging.info('camp: %s', l.extract())
            item['camp'] = l.extract()
            break

        logging.debug('grab twitter...')
        for l in response.xpath('//a[@class="external text" and contains(text() ,"Twitter")]/@href'):
            logging.info('Twitter Feed: %s', l.extract())
            item['twtr'] = l.extract()
            break

        logging.debug('grab facebook...')
        for l in response.xpath('//a[@class="external text" and contains(text() ,"Facebook")]/@href'):
            logging.info('Facebook Page: %s', l.extract())
            item['fb'] = l.extract()
            break

        logging.debug('grab youtube...')
        for y in response.xpath('//a[@class="external text" and contains(text() ,"Youtube")]/@href'):
            logging.info('Youtube: %s', y.extract())
            item['youtube'] = y.extract()
            break
        yield item

class SenateSpider3(scrapy.Spider):
    name = "senate3"
    allowed_domains = ["ballotpedia.org"]
    #start_urls = ["https://ballotpedia.org/United_States_Senate_election_in_Oklahoma,_2016"]
    start_urls = ["https://ballotpedia.org/United_States_Senate_election_in_Oklahoma,_2016", "https://ballotpedia.org/United_States_Senate_election_in_Alabama,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Alaska,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Arizona,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Arkansas,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_California,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Colorado,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Connecticut,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Georgia,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Hawaii,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Idaho,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Illinois,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Indiana,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Iowa,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Kansas,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Kentucky,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Louisiana,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Maryland,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Missouri,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Nevada,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_New_York,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_North_Carolina,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_North_Dakota,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Ohio,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Oklahoma,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Oregon,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Pennsylvania,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_South_Carolina,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_South_Dakota,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Utah,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Vermont,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Washington,_2016" ,"https://ballotpedia.org/United_States_Senate_election_in_Wisconsin,_2016"]


    def __init__(self):
        self.S2 = SenateSpider2()

    def parse(self, response):
        i=1
        # select all <a> in general election candidates but not the party icon link
        for h in response.xpath('//*[@id="bodyContent"]/table[3]/tr/td[2]/a[not(contains(@href, "Party"))]/@href').extract():
            url = response.urljoin(h)
            logging.info('candidate url: %s', url)
            name = h.replace("_", " ")[1:] 
            item = CandItem()
            item['name'] = name
            item['url'] = url
            item['chamber'] = 'S'
            item['gen_election_candidate'] = True
            yield scrapy.Request(url, callback=self.S2.parse_cand, meta={'item':item}) 


# sameple urls
#start_urls=["https://ballotpedia.org/Patty_Murray" ,"https://ballotpedia.org/Chris_Vance" ,"https://ballotpedia.org/Phil_Cornell" ,"https://ballotpedia.org/Mohammad_Said" ,"https://ballotpedia.org/Thor_Amundson" ,"https://ballotpedia.org/Uncle_Mover" ,"https://ballotpedia.org/Eric_John_Makus" ,"https://ballotpedia.org/Scott_Nazarino" ,"https://ballotpedia.org/Mike_Luke" ,"https://ballotpedia.org/Sam_Wright_(Washington)" ,"https://ballotpedia.org/Zach_Haller" ,"https://ballotpedia.org/Donna_Rae_Lands" ,"https://ballotpedia.org/Alex_Tsimerman" ,"https://ballotpedia.org/Pano_Churchill" ,"https://ballotpedia.org/Ted_Cummings" ,"https://ballotpedia.org/Chuck_Jackson" ,"https://ballotpedia.org/Jeremy_Teuton"] 

# spider3 applies to FL
# Different layout for FL, and NH. Had to hardcode the xpath here
class SenateSpider4(scrapy.Spider):
    name = "senate4"
    allowed_domains = ["ballotpedia.org"]
    start_urls = ["https://ballotpedia.org/United_States_Senate_election_in_New_Hampshire,_2016"]
                 #"https://ballotpedia.org/United_States_Senate_election_in_Florida,_2016"

    def __init__(self):
        self.S2 = SenateSpider2()

    def parse(self, response):
        logging.debug('grab Democratic_Party candidates...') 
        for h in response.xpath('//div[@id="bodyContent"]/table[3]/tr/td[1]/a/@href').extract():
            url = response.urljoin(h)
            logging.info('candidate url: %s', url)
        
            name = h.replace("_", " ")[1:] 
            item = CandItem()
            item['name'] = name
            item['url'] = url
            item['chamber'] = 'S'
            yield scrapy.Request(url, callback=self.S2.parse_cand, meta={'item':item}) 


        logging.debug('grab Republican_Party candidates...')
        for h in response.xpath('//*[@id="bodyContent"]/table[3]/tr/td[3]/a/@href').extract():
            url = response.urljoin(h)
            logging.info('candidate url: %s', url)

            name = h.replace("_", " ")[1:] 
            item = CandItem()
            item['name'] = name
            item['url'] = url
            item['chamber'] = 'S'
            yield scrapy.Request(url, callback=self.S2.parse_cand, meta={'item':item}) 




