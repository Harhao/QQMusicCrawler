# QQ音乐音频地址抓取
- 1.musicCrawl是完成个别喜欢歌手的全部歌曲代码模块：
  - 使用方法,进入musicCrawl根目录里:
  ```
  $ scrapy crawl requestUrl
  ```
- 2.musicCrawlSinger是包括爬取QQ音乐所有歌手的名字，然后改进相应的代码组成函数块。然后把从MongoDB数据库里面保存的歌手数据动态提取出来使用。
  - 使用方法与musicCrawl类似：
  ```
  $ scrapy crawl requestUrl(requestSinger)
  ```
