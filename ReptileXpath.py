# coding:utf-8

from lxml import etree
from ExcelUtils import ExcelUtils
from Reptile import Reptile
import time
from EmailUtils import EmailUtils


class ReptileXpath(Reptile):

    def __init__(self):
        super(ReptileXpath ,self).__init__()

    def parse_job_list(self, text):
        try:
            f = etree.HTML(text)
            lis = f.xpath('//*/div[@class="sojob-result "]/ul[@class="sojob-list"]/li')
            # 对职位列表进行解析
            for li in lis:
                job_info_list = li.xpath('./div[@class="sojob-item-main clearfix"]/div[@class="job-info"]')
                job_href = job_info_list[0].xpath('./h3/a/@href')           # 职位详情链接
                job_title = job_info_list[0].xpath('./h3/a/text()')         # 职位标题
                job_salary = job_info_list[0].xpath('./p/span[1]/text()')  # 薪水
                job_edu = job_info_list[0].xpath('./p/span[2]/text()')     # 学历要求
                job_exp = job_info_list[0].xpath('./p/span[3]/text()')     # 工作经验
                job_addr = job_info_list[0].xpath('./p/a/text()')           # 公司地址
                job_date = job_info_list[0].xpath('./p[2]/time/@title')    # 发布日期

                job_title = job_title[0] if len(job_title) > 0 else ''
                job_href = job_href[0] if len(job_href) > 0 else ''
                job_salary = job_salary[0] if len(job_salary) > 0 else ''
                job_edu = job_edu[0] if len(job_edu) > 0 else ''
                job_exp = job_exp[0] if len(job_exp) > 0 else ''
                job_addr = job_addr[0] if len(job_addr) > 0 else ''
                job_date = job_date[0] if len(job_date) > 0 else ''

                '''
                获取公司信息
              '''
                company_info = li.xpath('./div[@class="sojob-item-main clearfix"]/div[@class="company-info nohover"]')
                company_name = company_info[0].xpath('./p[1]/a/text()')              # 公司名称
                company_tag = company_info[0].xpath('./p[2]/span/a/text()')         # 所属行业
                company_welfares = company_info[0].xpath('./p[@class="temptation clearfix"]/span')  # 公司福利

                company_name = company_name[0] if len(company_name) > 0 else ''
                company_tag = company_tag[0] if len(company_tag) > 0 else ''
                company_welfare = []
                for welfare in company_welfares:
                    welfare = welfare.xpath('./text()')
                    company_welfare.append(welfare[0]+"/" if len(welfare) > 0 else '')

                self.job_info.append(job_title)
                self.job_info.append(company_name)
                self.job_info.append(job_addr)
                self.job_info.append(company_tag)
                self.job_info.append(job_salary)
                self.job_info.append(company_welfare)
                self.job_info.append(job_edu)
                self.job_info.append(job_exp)
                self.job_info.append(job_date)
                self.job_info.append(job_href)
                # 获取职位详情页
                self.request_job_detail(job_href)
                time.sleep(1)
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)
            EmailUtils.send_mail(e.message)   # 发邮件后怎么退出


    def parse_job_detail(self, text):
        '''
        解析工作详情方法
        :param text:
        :return:
        '''
        try:
            html = etree.HTML(text)
            job_statements = html.xpath('//*/div[@class="content content-word"]')
            job_statement = job_statements[0] if len(job_statements) else ''
            if job_statement != '':
                job_statement = job_statement.xpath('string(.)').strip().split('\n')[0]
            else:
                job_statement = '暂无职位描述'
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)
            job_statement = '暂无描述'

        self.job_info.append(job_statement)
        self.count = self.count + 1
        # 写入excel
        ExcelUtils.write_excel(self.excel, self.sheet_table, self.count, self.job_info, u'xpath_liepinjob.xlsx')
        print '采集了{}条信息'.format(self.count)
        # 清空工作信息，便于下次使用
        self.job_info = []
        pass
