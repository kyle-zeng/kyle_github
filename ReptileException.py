# coding:utf-8
__author__ = "kyle"


class ReptileException(Exception):
    def __init__(self, error_info):
        super(ReptileException, self).__init__()
        self.message = error_info

    def __str__(self):
        return self.message

