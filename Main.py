# coding:utf-8

from ReptileXpath import  ReptileXpath

'''
爬虫入口
'''
class Main(object):

    @staticmethod
    def select_type():
        type = input('请输入你先选择的爬虫类型:\n1.xpath爬取数据\n2.正则爬取数据 \n3.bs4爬取数据 \n默认使用xpath提取数据\n你的输入是:')
        if type == 1:
            print '选择了xpath爬取数据\n\n'
            xpath = ReptileXpath()
            xpath.reptile_data()
        else:
            print '暂不支持其他类型\n\n'

if __name__ == '__main__':
    Main().select_type()