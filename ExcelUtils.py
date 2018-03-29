# coding:utf-8
import xlwt

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
Excel工具类，爬取的数据通过此类存入excel中

'''


class ExcelUtils(object):

    @staticmethod
    def create_excel(sheet_name, row_titles):
        '''
        创建excel，写入标题并返回
        :param sheet_name:
        :param row_titles:
        :return:
        '''
        excel = xlwt.Workbook();
        sheet_info = excel.add_sheet(sheet_name, cell_overwrite_ok=True)
        for j in range(0, len(row_titles)):
            sheet_info.write(0, j, row_titles[j])

        return excel, sheet_info

    @staticmethod
    def write_excel(excel_file, excel_sheet, count_line, data, excel_name):
        '''
        往excel中写入数据
        :param excel_file: 需要写入的excel
        :param excel_sheet:需要写入的sheet页
        :param count_line:行数
        :param data: 需要写入的数据
        :param excel_name: excel 名称
        :return:
        '''
        for i in range(len(data)):
            excel_sheet.write(count_line, i, data[i])

        excel_file.save(excel_name)