# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
import json
import re
import urllib.parse
import urllib.request
from musicCrawl.items import MusiccrawlItem
class requestUrlSpider(scrapy.Spider):
    name = "requestUrl"
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
    reqHeader={
        ':authority':'c.y.qq.com',
        ':method':'GET',
        ':path':'/v8/fcg-bin/fcg_play_single_song.fcg?songmid=001bhwUC1gE6ep&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0',
        ':scheme':'https',
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cache-control':'no-cache',
        'cookie':'pgv_pvi=2539236352; RK=E/NGWlYOOU; pgv_pvid=4700237117; ptui_loginuin=1482816494; ptcz=0ed94d9b03e410a4a4d523a936e1de8f739a265f19407322ac522dc4402dd9f8; pt2gguin=o1482816494; pgv_si=s1229479936; yq_playdata=s; yq_playschange=0; yq_index=3; qqmusic_fromtag=66; player_exist=1; yplayer_open=0; ts_last=y.qq.com/n/yqq/song/001bhwUC1gE6ep.html; ts_uid=7066888440; yqq_stat=0',
        'pragma':'no-cache',
        'referer':'https://y.qq.com/n/yqq/song/001bhwUC1gE6ep.html',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=56365046261055832&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=50&w={singer}&g_tk=5381&jsonpCallback=searchCallbacksong412&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    allUrl="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=63213556368351152&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p={page}&n=164&w={singer}&g_tk=5381&jsonpCallback=searchCallbacksong8887&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    singerName=["赵雷","薛之谦","李荣浩","陈奕迅","许嵩"]
    def start_requests(self):
        for i in range(len(self.singerName)):
            singer=urllib.parse.quote(self.singerName[i])
            yield Request(url=self.url.format(singer=singer),headers=self.headers,callback=self.songCount,dont_filter=True)
    def parse(self, response):
        jsonData=self.dealJson(response,["^searchCallbacksong\d{0,}\(","\)$"])
        songDetail=jsonData["data"]["song"]
        length=len(songDetail["list"])
        for i in range(length):
            action=songDetail["list"][i]
            songmid=action["mid"]
            musicUrl="https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid={mid}&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
            yield Request(url=musicUrl.format(mid=songmid),headers=self.reqHeader,callback=self.parse_music,dont_filter=True)
    def parse_music(self,response):
        jsonData=self.dealJson(response,["^getOneSongInfoCallback\(","\)$"])
        musicList=jsonData["data"][0]
        musicName=musicList["name"]
        musicUrl=jsonData["url"]
        for key,val in musicUrl.items():
            item=MusiccrawlItem()
            item["name"]=musicName
            item["url"]="http://"+val
            yield item
            # yield Request(url='http://'+val,headers=self.reqHeader,callback=self.downloadMusic,dont_filter=True)
    def dealJson(self,response,pattern):
        text=response.text
        text=re.sub(pattern[0],'',text)
        text=re.sub(pattern[1],'',text)
        jsonData=json.loads(text)
        return jsonData
    def songCount(self,response):
        numData=response
        numData=self.dealJson(numData,["^searchCallbacksong\d{0,}\(","\)$"])
        pageNum=(numData["data"]["song"]["totalnum"]//20)+1
        for j in range(len(self.singerName)):
            for i in range(pageNum):
                singer=urllib.parse.quote(self.singerName[j])
                yield Request(url=self.allUrl.format(page=i,singer=singer),headers=self.headers,callback=self.parse,dont_filter=True)
