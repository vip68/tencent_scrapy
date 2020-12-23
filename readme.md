## 项目说明

* 爬取 [腾讯内容开放平台—内容管理](https://om.qq.com/main/management/articleManage)
* 将标题、链接、时间导出到csv、json文件
* 截取所有视频页面，并带地址栏

---

### 环境需求

- python3.6+
- scrapy
- selenium
- chromedriver

---

### 项目初始化

- 生成爬虫项目

  `scrapy startproject tencent`


- 进入项目目录

  `cd tencent`


- 创建蜘蛛

  `scrapy genspider tencent om.qq.com`


- 查看创建的蜘蛛

  `scrapy list`

---

### 项目运行

- 运行爬虫

  `scrapy crawl tencent`
