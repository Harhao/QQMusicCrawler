# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
import json
import re
class MusicSpider(scrapy.Spider):
    name = "Music"
    allowed_domains = ["www.y.qq.com"]
    start_urls = ['http://www.y.qq.com/']
    headers={
        ':authority':'c.y.qq.com',
        ':method':'GET',
        ':path':'/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=54134794373394557&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=%E8%B5%B5%E9%9B%B7&g_tk=5381&jsonpCallback=searchCallbacksong4621&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0',
        ':scheme':'https',
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'no-cache',
        'cookie':'pgv_pvi=2539236352; RK=E/NGWlYOOU; pgv_pvid=4700237117; ptui_loginuin=1482816494; ptcz=0ed94d9b03e410a4a4d523a936e1de8f739a265f19407322ac522dc4402dd9f8; pt2gguin=o1482816494; yq_index=0; pgv_si=s1229479936; ts_last=y.qq.com/portal/search.html; ts_uid=7066888440; yqq_stat=0',
        'pragma':'no-cache',
        'referer':'https://y.qq.com/portal/search.html',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    reqHeaders={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Cookie':'pgv_pvi=2539236352; RK=E/NGWlYOOU; pgv_pvid=4700237117; ptui_loginuin=1482816494; ptcz=0ed94d9b03e410a4a4d523a936e1de8f739a265f19407322ac522dc4402dd9f8; pt2gguin=o1482816494; pgv_si=s1229479936; qqmusic_fromtag=66',
        'Host':'dl.stream.qqmusic.qq.com',
        'Pragma':'no-cache',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=54134794373394557&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=%E8%B5%B5%E9%9B%B7&g_tk=5381&jsonpCallback=searchCallbacksong4621&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    def start_requests(self):
        yield Request(url=self.url,headers=self.headers,callback=self.parse)
    def parse(self, response):
        text=response.text
        text=re.sub(r'^searchCallbacksong4621\(','',text)
        text=re.sub(r'\)$','',text)
        # with open("data.json","w",encoding="UTF-8") as f:
        #     f.writelines(text)
        jsonData=json.loads(text)
        songDetail=jsonData["data"]["song"]
        action=songDetail["list"][0]
        mid=action['album']["mid"]
        yield Request(url="http://dl.stream.qqmusic.qq.com/C400"+mid+".m4a?vkey=D7063FD71A1B910396EB580503329D63D2BBB0033AB317FF8C3685095B5C6B318566D57CC84018AFC7DE6249EFDD6ECA4F037D5B439FFD52&guid=4700237117&uin=0&fromtag=66",headers=self.reqHeaders,callback=self.downloadMusic,dont_filter=True)
    def downloadMusic(self,response):
        with open("1.mp3","wb") as f:
            f.write(response)
        # logging.info(response)