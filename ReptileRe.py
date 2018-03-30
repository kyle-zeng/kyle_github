# coding:utf-8


import re
from ExcelUtils import ExcelUtils
from Reptile import Reptile
import time
from ReptileException import ReptileException


class ReptileRe(Reptile):

    def __init__(self):
        super(ReptileRe, self).__init__()

    def parse_job_list(self, text):
        try:
            pattern = re.compile('<li>.*?<div class="job-info">.*?<h3.*?title="(.*?)".*?<a.*?href="(.*?)".*?<span.*?"text-warning">(.*?)</span>'
                                 '.*?<a.*?"area">(.*?)</a>.*?<span.*?"edu">(.*?)</span>.*?<span>(.*?)</span>.*?<time.*?title="(.*?)".*?href=".*?">(.*?)</a>'
                                 '.*?class="field-financing">.*?target="_blank">(.*?)</a>.*?class="temptation clearfix">.*?<span>(.*?)</span>.*?<span>(.*?)</span>'
                                 '.*?<span>(.*?)</span>.*?</li>',
                                 re.S)
            jobs = re.findall(pattern, text)
            for job in jobs:
                job_title = job[0]
                job_href = job[1]
                job_salary = job[2]
                job_addr = job[3]
                job_edu = job[4]
                job_exp = job[5]
                job_date = job[6]

                company_name = job[7]
                company_tag = job[8]
                company_welfare = []
                for i in range(9, len(job)):
                    company_welfare.append(job[i] + "/" )

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
        except ReptileException as e1:
            raise e1
        except Exception as e2:
            # 异常抛出调用处处理
            ex = ReptileException('parse_job_list 解析职位列表异常，异常信息：{}'.format(e2.message))
            raise ex

    def parse_job_detail(self, text):
        try:
            result = re.findall(r'<div class="content content-word">(.*?)</div', text, re.S)
            job_statement = ''
            if len(result) > 0:
                job_statement = ''.join(
                [i.strip() for i in re.split(r'<br/>', re.sub('<[/]?\w+>', '', result[0].strip()))]) if \
                result[0] else ''
        except ReptileException as e1:
            raise e1
        except Exception as e2:
            # 异常抛出调用处处理
            ex = ReptileException('parse_job_detail 解析职位详情异常，异常信息：{}'.format(e2.message))
            raise ex

        self.job_info.append(job_statement)
        self.count = self.count + 1
        #  写入excel
        ExcelUtils.write_excel(self.excel, self.sheet_table, self.count, self.job_info, u're_liepinjob.xlsx')
        print '采集了{}条信息'.format(self.count)
        #  清空工作信息，便于下次使用
        self.job_info = []
        pass