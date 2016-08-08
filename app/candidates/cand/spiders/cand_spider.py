import scrapy
from cand.items import CandItem


# Parsing logic:
#1 search all Independent/Libertarian/Republican/Democratic node and following the node to the candidate's page
#2 get all primary candidate's href link, and find it's district/name information
# TODO remove duplicate candidate

class CandSpider(scrapy.Spider):
    name = "cand"
    allowed_domains = ["ballotpedia.org"]
    start_urls = ["https://ballotpedia.org/United_States_Congress_elections,_2016"]

    def parse(self, response):
				# grep 50 state's info
        for i, href in enumerate(response.xpath('//table[@class="infobox"]/descendant::node()/a[contains(@href, "United_States_House_of_Representatives_elections_in")]/@href').extract()):
            print "State==>" #/United_States_House_of_Representatives_elections_in_Louisiana,_2016
            state = href.split(',')[0].split('_')[-1]
            print state
            url = response.urljoin(href)

            item = CandItem()  
            item['state'] = state
            # pass item to next level
            request =  scrapy.Request(url, callback=self.parse_states)
            request.meta['item'] = item

            print "successfully parsed " + str(i) + " states"
            yield request

    # parse state info 
    # get party/candidate url/candidate's name
    def parse_states(self, response):
        for i, href in enumerate(response.xpath('//a[contains(@href, "Independent") or contains(@href, "Libertarian") or contains(@href, "Republican_Party") or contains(@href, "Democratic_Party")]')):
            party = href.xpath('./@title').extract()[0]
            print "party: "
            print party

            # sometimes this return a list of name, hence get the first one
            # e.g. u'/Pepper_Snyder' 
            ccurl = href.xpath('following-sibling::a/@href').extract()
            if len(ccurl) > 0:
                print 'multiple candidates url found: '
                print ccurl
                curl = ccurl[0]
            else:
                curl = ""
            print "curl:"
            print curl

            name = curl.replace("_", " ")[1:] 
            print "name:"
            print name

            cand_urls = response.urljoin(curl)
            print cand_urls
            
            # get item from upper level 
            item = response.meta['item']
            # TODO bad data overwrite good one
            # if 'name' not in item or len(item['name'])!= 0:
            item['name'] = name
            item['url'] = cand_urls
            item['party'] = party
            request = scrapy.Request(cand_urls, callback=self.parse_cand, meta={'item':item}) 
            #request.meta['item'] = item

            print "successfully parsed " + str(i) + " persons"
            yield request

    #1 get img src in table class infobox
    #2 get district number
    #3 get Campaign website, Facebook page, Twitter feed

    def parse_cand(self, response):
        item = response.meta['item']
        for p in response.xpath('//table[@class="infobox"]/descendant::node()/@src'):
            item['pic'] = response.urljoin(p.extract())
            print p.extract()
            break # break for debug only

        for dist in response.xpath('//a[contains(@href, "Congressional_District")]/text()'):
            d = dist.extract().split()[1]
            item['dist'] = d
            print d
            break

        for l in response.xpath('//a[@class="external text" and contains(text() ,"Campaign")]/@href'):
            print "Campaign website:"
            print l.extract()
            item['camp'] = l.extract()
            break

        for l in response.xpath('//a[@class="external text" and contains(text() ,"Twitter")]/@href'):
            print "Twitter Feed:"
            print l.extract()
            item['twtr'] = l.extract()
            break

        for l in response.xpath('//a[@class="external text" and contains(text() ,"Facebook")]/@href'):
            print "Facebook Page:"
            print l.extract()
            item['fb'] = l.extract()
            break

        return item

