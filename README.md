# QQ音乐音频地址抓取
- musicCrawl是完成个别喜欢歌手的全部歌曲代码模块：
  - 使用方法,进入musicCrawl根目录里:
  ```
  $ scrapy crawl requestUrl
  ```
- musicCrawlSinger是包括爬取QQ音乐所有歌手的名字，然后改进相应的代码组成函数块。然后把从MongoDB数据库里面保存的歌手数据动态提取出来使用。
  - 使用方法与musicCrawl类似：
  ```
  $ scrapy crawl requestUrl(requestSinger)
  ```
 - 单个IP爬取可能会造成IP被封禁的情况，所以尽量设置下载延迟以及搭建一个动态更换的IP池，每一个请求换一个IP进行访问
 - 详情过程查看[QQ音乐爬虫](http://www.jianshu.com/p/72b4222fadf5)
