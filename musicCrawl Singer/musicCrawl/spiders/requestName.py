import scrapy
from scrapy import Request
import logging
import re
import json
from musicCrawl.items import singerItem
class requestNameSpider(scrapy.Spider):
    name = "requestName"
    allowed_domains = ["www.y.qq.com"]
    url="https://shc.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=all_all_all&pagesize=100&pagenum={pagenum}&g_tk=5381&jsonpCallback=GetSingerListCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    headers={
        ':authority':'shc.y.qq.com',
        ':method':'GET',
        ':path':'/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=all_all_all&pagesize=100&pagenum=1&g_tk=5381&jsonpCallback=GetSingerListCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0',
        ':scheme':'https',
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'no-cache',
        'cookie':'pgv_pvi=2539236352; RK=E/NGWlYOOU; ptui_loginuin=1482816494; ptcz=0ed94d9b03e410a4a4d523a936e1de8f739a265f19407322ac522dc4402dd9f8; pt2gguin=o1482816494; yq_index=0; tvfe_boss_uuid=6e9af09cbb0ea51c; pgv_pvid=4700237117; o_cookie=1482816494; pgv_si=s7529175040; ts_last=y.qq.com/portal/singer_list.html; ts_uid=7066888440; yqq_stat=0',
        'pragma':'no-cache',
        'referer':'https://y.qq.com/portal/singer_list.html',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    def start_requests(self):
        yield Request(url=self.url.format(pagenum=1),headers=self.headers,callback=self.parse,dont_filter=True)
    def parse(self, response):
        jsonData=self.dealJson(response,["^ GetSingerListCallback\(","\)$"])
        totalPage=jsonData["data"]["total_page"]
        for i in range(totalPage):
            yield Request(url=self.url.format(pagenum=i),headers=self.headers,callback=self.insertSinger,dont_filter=True)
    def insertSinger(self,response):
        # 第一个pattern前面有一个空格
        jsonData=self.dealJson(response,["^ GetSingerListCallback\(","\)$"])
        singerList=jsonData["data"]["list"]
        for i in range(len(singerList)):
            item=singerItem()
            item["singerName"]=singerList[i]["Fsinger_name"]
            item["singer_mid"]=singerList[i]["Fsinger_mid"]
            yield item

    def dealJson(self,response,pattern):
        text=response.text
        text=re.sub(pattern[0],'',text)
        text=re.sub(pattern[1],'',text)
        jsonData=json.loads(text)
        return jsonData