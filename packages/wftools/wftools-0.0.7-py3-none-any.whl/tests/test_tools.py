import unittest

from tests.test_utils.test_input import stub_stdin
from wftools.api.tools import *


class TestTools(unittest.TestCase):
    def test_weather(self):
        stub_stdin(self, '北京\ny\nq\n')  # 依次输入
        weather()

    def test_url2ip(self):
        url2ip('www.python-office.com')

    def test_lottery8ticket(self):
        stub_stdin(self, '12\n0\n')  # 依次输入
        lottery8ticket()

    def test_create_article(self):
        create_article('生日快乐', line_num=2000)

    # def test_pwd4wifi(self):
    #     stub_stdin(self, '1\ny\n')  #依次输入
    #     pwd4wifi(pwd_list=['12345678', 'CoderWanFeng'])
