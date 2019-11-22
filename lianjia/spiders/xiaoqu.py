# -*- coding: utf-8 -*-

import scrapy
from lianjia.items import ResidenceInfoItem
import datetime
from lianjia.Exception.emailSender import emailSender

city_dict = {
    'bj.lianjia': u'北京', 'sh.lianjia': u'上海', 'xm.lianjia': u'厦门', 'nj.lianjia': u'南京', 'cd.lianjia': u'成都', 'qd.lianjia': u'青岛',
    'wh.lianjia': u'武汉', 'jn.lianjia': u'济南', 'hf.lianjia': u'合肥', 'xa.lianjia': u'西安', 'gz.lianjia': u'广州', 'su.lianjia': u'苏州',
    'cq.lianjia': u'重庆', 'lf.lianjia': u'廊坊', 'tj.lianjia': u'天津', 'cs.lianjia': u'长沙', 'wx.lianjia': u'无锡', 'sy.lianjia': u'沈阳',
    'zz.lianjia': u'郑州', 'nb.lianjia': u'宁波', 'hz.lianjia': u'杭州', 'sz.lianjia': u'深圳', 'km.lianjia': u'昆明', 'jh.lianjia': u'金华',
    'lz.lianjia': u'兰州', 'fs.lianjia': u'佛山', 'dl.lianjia': u'大连', 'nn.lianjia': u'南宁', 'dg.lianjia': u'东莞', 'sjz.lianjia': u'石家庄',
    'wz.lianjia': u'温州'
}


class LjXiaoquSpider(scrapy.Spider):
    name = "lj_xiaoqu"
    allowed_domain = [
        'https://bj.lianjia.com',
        'https://lf.lianjia.com',
        'https://cd.lianjia.com',
        'https://jn.lianjia.com',
        'https://nj.lianjia.com',
        'https://qd.lianjia.com',
        'https://sh.lianjia.com',
        'http://sh.lianjia.com',
        'https://hf.lianjia.com',
        'https://wh.lianjia.com',
        'https://xm.lianjia.com',
        'https://xa.lianjia.com',
        'https://gz.lianjia.com',
        'https://cq.lianjia.com',
        'http://su.lianjia.com'
    ]

    start_urls = {
        'https://bj.lianjia.com/xiaoqu',
        'https://sh.lianjia.com/xiaoqu',
        'https://tj.lianjia.com/xiaoqu',
        'https://cs.lianjia.com/xiaoqu',
        'https://xa.lianjia.com/xiaoqu',
        'https://wh.lianjia.com/xiaoqu',
        'https://nj.lianjia.com/xiaoqu',
        'https://wx.lianjia.com/xiaoqu',
        'https://cd.lianjia.com/xiaoqu',
        'https://sy.lianjia.com/xiaoqu',
        'https://qd.lianjia.com/xiaoqu',
        'https://zz.lianjia.com/xiaoqu',
        'https://nb.lianjia.com/xiaoqu',
        'https://hz.lianjia.com/xiaoqu',
        'https://sz.lianjia.com/xiaoqu',
        'https://km.lianjia.com/xiaoqu',
        'https://jh.lianjia.com/xiaoqu',
        'https://lz.lianjia.com/xiaoqu',
        'https://fs.lianjia.com/xiaoqu',
        'https://dl.lianjia.com/xiaoqu',
        'https://nn.lianjia.com/xiaoqu',
        'https://dg.lianjia.com/xiaoqu',
        'https://sz.lianjia.com/xiaoqu',
        'https://cq.lianjia.com/xiaoqu',
        'https://sjz.lianjia.com/xiaoqu',
        'https://wz.lianjia.com/xiaoqu',
        # 'https://lf.lianjia.com/xiaoqu',
        # 'https://bj.lianjia.com/xiaoqu',
        # 'https://cd.lianjia.com/xiaoqu',
        # 'https://cq.lianjia.com/xiaoqu',
        # 'https://jn.lianjia.com/xiaoqu',
        # 'https://nj.lianjia.com/xiaoqu',
        # 'https://qd.lianjia.com/xiaoqu',
        # 'https://hf.lianjia.com/xiaoqu'
        # 'http://sh.lianjia.com/xiaoqu',
        # 'https://sjz.lianjia.com/xiaoqu',
        # 'https://wh.lianjia.com/xiaoqu',
        # 'https://xm.lianjia.com/xiaoqu',
        # 'https://xa.lianjia.com/xiaoqu',
        # 'https://gz.lianjia.com/xiaoqu',
        # 'http://su.lianjia.com/xiaoqu',
    }

    # 获取区域链接
    def parse(self, response):
        u = response.url
        URL = u.split(r"/xiaoqu/")[0]
        urls = response.xpath(
            '//div[@class="position"]/dl[2]/dd/div[@data-role="ershoufang"]/div/a/@href').extract()
        for url in urls:
            if "https" not in url:
                new_url = URL + url
                yield scrapy.Request(url=new_url, callback=self.parse_community)

    # 获取小区链接
    def parse_community(self, response):
        item = ResidenceInfoItem()
        select = scrapy.Selector(response)
        li = select.xpath("/html/body/div[4]/div[1]/ul//li")
        for l in li:
            url = l.xpath("a/@href").extract_first()
            # item['residence_name'] = l.xpath("div[@class='info']/div/a/text()").extract_first()
            item['district'] = l.xpath(
                "div/div/a[@class='district']/text()").extract_first()
            item['community'] = l.xpath(
                "div/div/a[@class='bizcircle']/text()").extract_first()

            yield scrapy.Request(url, meta={'key': item}, callback=self.parse_residence_info)

        page_box = select.xpath(
            '//div[@class="page-box house-lst-page-box"]').extract_first()
        if page_box is not None:
            totalPage = eval(scrapy.Selector(text=page_box).xpath(
                '//@page-data').extract_first())['totalPage']
            curPage = eval(scrapy.Selector(text=page_box).xpath(
                '//@page-data').extract_first())['curPage']
            if totalPage > curPage:
                yield scrapy.Request(
                    response.url[0:response.url.find(
                        '/', 30) + 1] + 'pg' + str(curPage + 1) + '/',
                    callback=self.parse_community
                )

    def parse_residence_info(self, response):
        select = scrapy.Selector(response)
        item = response.meta['key']
        # 小区地址，别名
        name_str = select.xpath(
            '//*[@class="detailDesc"]/text()').extract_first()
        item['address'] = name_str
        # if r'(' in name_str:
        #     address = re.findall(r'\((.*?)\)', name_str)[0]
        #     item['address'] = address
        #     alias = name_str[len(address)+2:]
        #     item['alias'] = alias
        # else:
        #     item['address'] = name_str
        #     item['alias'] = u"无"
        # 小区经纬度
        item['coordinate'] = select.xpath(
            '//*[@class="xiaoquInfoContent"]/span/@xiaoqu').extract_first()
        # 建成时间
        item['build_time'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract_first()
        # 物业费
        item['property_price'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[3]/span[2]/text()').extract_first()
        # 物业公司
        item['property_company'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[4]/span[2]/text()').extract_first()
        # 开发商
        item['developer'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[5]/span[2]/text()').extract_first()
        # 楼栋总数
        item['total_buildings'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract_first()
        # 总户数
        item['total_houses'] = select.xpath(
            '//*[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract_first()
        # 小区名字
        item['residence_name'] = select.xpath(
            '//*[@class="detailTitle"]/text()').extract_first()
        # 业务时间
        item['bsn_dt'] = str(datetime.date.today())
        # 抓取时间
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
        # 入库时间戳
        item['tms'] = datetime.datetime.now().strftime('%Y-%m-%d %X')

        item['webst_nm'] = u'链家'
        # 城市
        for key in city_dict.keys():
            if key in response.url:
                item['city'] = city_dict[key]
        item['url'] = response.url
        yield item

    @staticmethod
    def close(spider, reason):
        print "closed!!!!!"
        # emailSenderClient = emailSender()
        # toSendEmailLst = ['liuyang@zhongjiaxin.com']
        # finishTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
        # subject = u"爬虫结束状态汇报"
        # body = u"爬虫结束状态汇报：\n\
        #     爬虫名称：" + spider.name + u"\n\
        #     结束原因：" + reason +u"\n\
        #     结束时间：" + finishTime
        # emailSenderClient.sendEmail(toSendEmailLst, subject, body, spider)

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES_BASE': {
            'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
            'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
            'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
            'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
            'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
            'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 800,
            'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
            'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'lianjia.filter_url.LjprojectSpiderMiddleware': 310,
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'fangproject.useragent_middlewares.RandomUserAgent': 400,
        },
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {
            'lianjia.pipelines.LjProjectPipeline': 300,
        }
    }
