# coding:utf-8

import time
import abc
import requests
from ExcelUtils import ExcelUtils

'''
爬虫的抽象类
主要实现网页内容的获取方法

'''

class Reptile(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.rows_title = [u'招聘标题', u'公司名称', u'公司地址', u'公司所属行业', u'待遇', u'福利', u'学历', u'工作经验', u'发布日期', u'招聘链接', u'招聘要求描述']
        sheet_name = u'liepinjob_Python招聘'
        return_excel= ExcelUtils.create_excel(sheet_name, self.rows_title)
        self.excel = return_excel[0]
        self.sheet_table = return_excel[1]
        self.job_info = []
        self.count = 0      #excel 表格第一行开始

    def reptile_data(self):
        for i in range(0, 3):
            url = 'https://www.liepin.com/zhaopin/?pubTime=&ckid=4ceacca0e5e9d678&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=&industryType=&jobKind=&sortFlag=15&degradeFlag=0&industries=&salary=&compscale=&key=python&clean_condition=&headckid=4ceacca0e5e9d678&d_pageSize=40&siTag=I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw&d_headId=46e2616195974a554a49b7da5aa02a91&d_ckId=46e2616195974a554a49b7da5aa02a91&d_sfrom=search_industry&d_curPage={0}&curPage={1}'.format(i,i+1)
            self.request_job_list(url)
            time.sleep(1)

    def request_job_list(self, page_url):

        try:
            headers = {
                'Referer': 'http://www.liepin.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400'
            }
            response = requests.get(page_url, headers=headers)
            #response.encoding = 'gbk'

            if response.status_code != 200:
                return
            self.parse_job_list(response.text)
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

    @abc.abstractmethod
    def parse_job_list(self, text):

        pass

    def request_job_detail(self, job_href):

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400'
            }
            response = requests.get(job_href, headers=headers)

            if response.status_code != 200:
                return ''

            self.parse_job_detail(response.text)

        except Exception as e:
            print '\n\n获取工作详情出现错误，错误信息如下：{}\n\n'.format(e.message)

    @abc.abstractmethod
    def parse_job_detail(self, text):
        '''
        工作详情抽象方法
        :param text:
        :return:
        '''
        pass