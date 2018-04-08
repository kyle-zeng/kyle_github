# coding:utf-8

from bs4 import BeautifulSoup
from ExcelUtils import ExcelUtils
from Reptile import Reptile
import time
from ReptileException import ReptileException

class ReptileBs4(Reptile):

    def __init__(self):
        super(ReptileBs4, self).__init__()

    def parse_job_list(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            results = soup.select('ul.sojob-list > li')[1:]
            for result in results:
                job_href = result.select('div.job-info h3 a')  # 职位详情链接
                # job_title = result.select('div.job-info p span.text-warning')  # 职位标题
                job_salary = result.select('div.job-info p span.text-warning')  # 薪水
                job_edu = result.select('div.job-info p span.edu')  # 学历要求
                job_exp = result.select('div.job-info p > span')  # 工作经验
                job_addr = result.select('div.job-info p a.area')  # 公司地址
                job_date = result.select('div.job-info p time')  # 发布日期

                job_title = job_href[0].text if len(job_href) > 0 else ''
                job_href = job_href[0].attrs['href'] if len(job_href) > 0 else ''
                job_salary = job_salary[0].text if len(job_salary) > 0 else ''
                job_edu = job_edu[0].text if len(job_edu) > 0 else ''
                job_exp = job_exp[2].text if len(job_exp) > 2 else ''
                job_addr = job_addr[0].text if len(job_addr) > 0 else ''
                job_date = job_date[0].attrs['title'] if len(job_date) > 0 else ''

                company_name = result.select('p.company-name > a')
                company_tag = result.select('p.field-financing > span > a')  # 所属行业
                company_welfares = result.select('div[class="company-info nohover"] p[class="temptation clearfix"] > span')  # 公司福利

                company_name = company_name[0].text if len(company_name) > 0 else ''
                company_tag = company_tag[0].text if len(company_tag) > 0 else ''
                company_welfare = []
                for welfare in company_welfares:
                    welfare = welfare.text if len(welfare) > 0 else ''
                    company_welfare.append(welfare + "/" )

                self.job_info.append(job_title)
                self.job_info.append(company_name)
                self.job_info.append(job_addr)
                self.job_info.append(company_tag)
                self.job_info.append(job_salary)
                self.job_info.append(company_welfares)
                self.job_info.append(job_edu)
                self.job_info.append(job_exp)
                self.job_info.append(job_date)
                self.job_info.append(job_href)

                # 获取职位详情页
                self.request_job_detail(job_href)
                time.sleep(1)
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

    def parse_job_detail(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            job_statements = soup.select('div[class="content content-word"]')
            job_statement = job_statements[0].text if len(job_statements) > 0 else ''
        except Exception as e:
            job_statement = '暂无描述'
            ex = ReptileException('parse_job_detail 解析职位详情异常，异常信息：{}'.format(e.message))
            raise ex

        self.job_info.append(job_statement)
        self.count = self.count + 1
        #  写入excel
        ExcelUtils.write_excel(self.excel, self.sheet_table, self.count, self.job_info, u'bs4_liepinjob.xlsx')
        print '采集了{}条信息'.format(self.count)
        #  清空工作信息，便于下次使用
        self.job_info = []
        pass
