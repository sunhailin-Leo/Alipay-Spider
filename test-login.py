# -*- coding: UTF-8 -*-
"""
Created on 2017年9月25日
@author: Leo
"""

# 系统库
import time

# 第三方库
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


# 登录 url
Login_Url = 'https://auth.alipay.com/login/index.htm?goto=https%3A%2F%2Fwww.alipay.com%2F'
# 账单 url
Bill_Url = 'https://consumeprod.alipay.com/record/advanced.htm'
# 验证码 url
Secure_Url = 'https://authem14.alipay.com/login/checkSecurity.htm'


# 登录用户名和密码
USERNAME = '支付宝账号'
PASSWORD = '支付宝密码'

# 自定义 headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
    'Host': 'consumeprod.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}


# 支付宝账单信息
class AlipayBill(object):
    # headers, cookies, info_list: 存储账单信息的列表
    def __init__(self, headers, uname, upwd):
        # 初始化headers
        self.headers = headers

        # 初始化用户名和密码
        self.username = uname
        self.password = upwd

        # requests的session对象
        self.session = requests.Session()

        # 将请求头添加到session之中
        self.session.headers = self.headers

        # 初始化账单列表
        self.info_list = []

        # cookie存储
        self.cookie = {}

    # 减慢账号密码的输入速度
    def slow_input(self, ele, str):
        for i in str:
            ele.send_keys(i)
            time.sleep(0.5)

    # 获取cookies
    def get_cookies(self):
        # 初始化浏览器对象
        # self.sel = webdriver.PhantomJS(executable_path="D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        self.sel = webdriver.Chrome()
        self.sel.maximize_window()
        self.sel.get(Login_Url)
        self.sel.implicitly_wait(3)

        # 用户名输入框
        username = self.sel.find_element_by_id('J-input-user')
        username.clear()
        print('正在输入账号.....')
        self.slow_input(username, self.user)
        time.sleep(1)

        # 密码输入框
        password = self.sel.find_element_by_id('password_rsainput')
        password.clear()
        print('正在输入密码....')
        self.slow_input(password, self.passwd)

        # 登录按钮
        butten = self.sel.find_element_by_id('J-login-btn')
        time.sleep(1)
        butten.click()

        # 输出当前链接
        print(self.sel.current_url)
        # 跳转到账单页面
        print('正在跳转页面....')
        if self.sel.current_url == Secure_Url:
            print("进入手机验证码页面")
            self.sel.get(Secure_Url)

            # 手机验证码输入框
            secure_code = self.sel.find_element_by_id("riskackcode")
            print("输出验证码")
            user_input = input()
            self.slow_input(secure_code, user_input)

            # 验证码界面下一步按钮
            next_button = self.sel.find_element_by_xpath('//*[@id="J-submit"]/input')
            time.sleep(0.9)
            next_button.click()
        else:
            print("没有进入验证码界面,进入账单页面")
            self.sel.get(Bill_Url)
            self.sel.implicitly_wait(3)

            # get cookies transfer to dict
            # 获取字典
            cookies = self.sel.get_cookies()

            # cookie字典
            cookies_dict = {}
            for cookie in cookies:
                if 'name' in cookie and 'value' in cookie:
                    cookies_dict[cookie['name']] = cookie['value']
            self.cookie = cookies_dict

    # set cookies 到 session
    def set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        print(self.session.cookies)

    # 判断登录状态
    def login_status(self):
        # 添加 cookies
        self.set_cookies()
        status = self.session.get(Bill_Url, timeout=5, allow_redirects=False).status_code
        print(status)
        if status == 200:
            return True
        else:
            return False

    # 抓取数据
    def get_data(self):
        status = self.login_status()
        if status:
            html = self.session.get(Bill_Url).text
            soup = BeautifulSoup(html, 'lxml')

            # 待修改以下代码

            # # # 抓取前五个交易记录
            # trades = soup.find_all('tr', class_='J-item ')[:5]
            #
            # for trade in trades:
            #     # 做一个 try except 避免异常中断
            #     try:
            #         # 分别找到账单的 时间 金额 以及流水号
            #         time = trade.find('p', class_='text-muted').text.strip()
            #         amount = trade.find(
            #             'span', class_='amount-pay').text.strip()
            #         code = trade.find(
            #             'a', class_='J-tradeNo-copy J-tradeNo')['title']
            #         self.info_list.append(dict(time=time, amount=amount, code=code))
            #     except Exception as err:
            #         print(err)
            #         self.info_list.append({'error': '出现错误'})
            #         # 关闭浏览器
            #         self.sel.close()

        else:
            self.info_list.append({'error': '出现错误'})

        return self.info_list


if __name__ == '__main__':
    a = AlipayBill(HEADERS, USERNAME, PASSWORD)
    a.get_cookies()
    data = a.get_data()
    print(data)
