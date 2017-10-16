# -*- coding: UTF-8 -*-
"""
Created on 2017年9月25日
@author: Leo
"""

# 系统库
import random
from urllib.parse import quote_plus

# 第三方库
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 工程内部引用
from db.mgo import *
from model.transfer import *

# 账单页面URL
MY_Url = 'https://my.alipay.com/portal/i.htm'
Bill_Url = 'https://consumeprod.alipay.com/record/advanced.htm'
# 登录页面URL(quote_plus的理由是会处理斜杠)
Login_Url = 'https://auth.alipay.com/login/index.htm?goto=' + quote_plus(MY_Url)
# Login_Url = 'https://auth.alipay.com/login/index.htm?goto=' + quote_plus(Bill_Url)

# 登录用户名和密码
USERNAME = ''
PASSWORD = ''

# User-agent
USER_AGENT = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/61.0.3163.100 Safari/537.36']

# 自定义 headers
HEADERS = {
    'User-Agent': random.choice(USER_AGENT),
    'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
    'Host': 'consumeprod.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}

# 日志基本配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()


# 支付宝账单信息
class AlipayBill(object):
    # headers, cookies, info_list: 存储账单信息的列表
    def __init__(self, headers, uname, upwd):
        # 初始化浏览器字段
        self.browser = None

        # 初始化headers
        self.headers = headers

        # 初始化用户名和密码
        self.username = uname
        self.password = upwd

        # requests的session对象
        self.session = requests.Session()

        # 将请求头添加到session之中
        self.session.headers = self.headers

        # cookie存储
        self.cookie = {}

        # 交易类别选项
        self.transfer_option = None

    # 查看浏览器(用配置文件进行维护,智能化)
    def choose_browser(self):
        # 读取自定义selenium配置文件
        browser_configure = json.load(open("./conf/selenium.conf"))
        if browser_configure['PhantomJs'] != "" and browser_configure['ChromeDriver'] != "":
            logging.info("请输入浏览器类型: (1和回车是phantomJs, 2是Google Chrome浏览器)")
            browser_choice = input()
            # 选择1
            if browser_choice == "" or browser_choice == "1":
                self.load_phantomjs(browser_configure)
            # 选择2
            elif browser_choice == "2":
                self.load_chrome(browser_configure)
            # 异常选择
            else:
                raise ValueError("浏览器类型错误,请重试....")
        else:
            if browser_configure['PhantomJs'] != "":
                logger.info("加载PhantomJs浏览器...")
                self.load_phantomjs(browser_configure)
            elif browser_configure['ChromeDriver'] != "":
                logger.info("加载Chrome浏览器...")
                self.load_chrome(browser_configure)
            else:
                raise ValueError("Selenium configuration load failed, please check your configuration!...")

    # 加载PhantomJs
    def load_phantomjs(self, browser_configure):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = random.choice(USER_AGENT)
        self.browser = webdriver.PhantomJS(executable_path=browser_configure['PhantomJs'],
                                           service_log_path="./watchDog.log",
                                           desired_capabilities=dcap,
                                           port=9999)

    # 加载Google Chrome
    def load_chrome(self, browser_configure):
        self.browser = webdriver.Chrome(executable_path=browser_configure['ChromeDriver'],
                                        service_log_path="./watchDog.log", port=9999)

    # 减慢账号密码的输入速度
    @staticmethod
    def slow_input(ele, word):
        for i in word:
            # 输出一个字符
            ele.send_keys(i)
            # 随机睡眠0到1秒
            time.sleep(random.uniform(0, 0.5))

    # 获取cookies
    def get_cookies(self):
        # 浏览器初始化失败
        if self.browser is None:
            raise ValueError("Browser is not initialize!...")

        # 初始化浏览器对象
        self.browser.maximize_window()
        self.browser.get(Login_Url)
        self.browser.implicitly_wait(3)

        # 用户名输入框
        username = self.browser.find_element_by_id('J-input-user')
        username.clear()
        logger.info('正在输入账号.....')
        self.slow_input(username, self.username)
        time.sleep(random.uniform(0.4, 0.8))

        # 密码输入框
        password = self.browser.find_element_by_id('password_rsainput')
        password.clear()
        logger.info('正在输入密码....')
        self.slow_input(password, self.password)

        # 登录按钮
        # 隐藏Bug(1)：phantomJs在这里容易卡死...不知道为什么
        time.sleep(random.uniform(0.3, 0.5))
        self.browser.find_element_by_id('J-login-btn').click()

        # 输出当前链接
        logger.info("当前页面链接: " + self.browser.current_url)

        # 跳转下一个页面
        logger.info('正在跳转页面....')
        if "checkSecurity" in self.browser.current_url:
            logger.info("进入手机验证码页面")
            self.browser.get(self.browser.current_url)

            # 手机验证码输入框
            secure_code = self.browser.find_element_by_id("riskackcode")

            # 一次清空输入框
            secure_code.click()
            secure_code.clear()

            logger.info("输出验证码:")
            user_input = input()

            # 防止一些操作失误，二次清空输入框
            secure_code.click()
            secure_code.clear()

            # 开始输入用户提供的验证码
            self.slow_input(secure_code, user_input)

            # 验证码界面下一步按钮
            next_button = self.browser.find_element_by_xpath('//*[@id="J-submit"]/input')
            time.sleep(random.uniform(0.5, 1.2))
            next_button.click()

            logger.info("准备进入账单页面")
            logger.info("当前页面: " + self.browser.current_url)
            # self.browser.get(Bill_Url)
            self.browser.get(MY_Url)

            # 获取cookies转换成字典
            cookies = self.browser.get_cookies()

            # cookie字典
            cookies_dict = {}
            for cookie in cookies:
                if 'name' in cookie and 'value' in cookie:
                    cookies_dict[cookie['name']] = cookie['value']
            self.cookie = cookies_dict
            return True

        elif "login" in self.browser.current_url:
            logger.info("没有进入验证码界面,用户名密码错误,请重试")
            return False

        else:
            logger.info("没有进入验证码界面,进入账单页面")
            logger.info("当前页面: " + self.browser.current_url)
            self.browser.get(MY_Url)

            # 获取cookies转换成字典
            cookies = self.browser.get_cookies()

            # cookie字典
            cookies_dict = {}
            for cookie in cookies:
                if 'name' in cookie and 'value' in cookie:
                    cookies_dict[cookie['name']] = cookie['value']
            self.cookie = cookies_dict
            return True

    # set cookies 到 session
    def set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        logger.debug(self.session.cookies)

    # 判断登录状态
    def login_status(self):
        # 添加 cookies
        self.set_cookies()
        status = self.session.get(MY_Url, timeout=5, allow_redirects=False).status_code
        logging.debug(status)
        return True

        # 以下注释和以上代码,在爬取中发现404依然能够保留登录状态并成功跳转.
        # if status == 200:
        #     return True
        # else:
        #     return False

    # 该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def is_element_exist(self):
        try:
            self.browser.find_element_by_link_text('下一页')
            return True
        except Exception as err:
            logger.debug("判断是否存在下一页: " + str(err))
            return False

    # 翻页查询(参数is_next_page 控制是否有下一页)
    def turn_page(self, option):
        # 先判断是否存在下一页的标签
        is_next_page = self.is_element_exist()
        logger.info("是否存在下一页: " + str(is_next_page))

        # 上一个版本用的是BeautifulSoup进行标签获取,现在改成用lxml获取
        html = self.browser.page_source
        selector = etree.HTML(html)

        # 选取的父标签
        trs = selector.xpath("//tbody//tr")

        try:
            # 加载数据库配置
            mgo = Mgo(logger)

            # 开始循环第一页
            for tr in trs:
                # 交易记录实体类
                transfer = Transfer()

                # 交易时间(年月日 + 时分)
                time_tag = tr.xpath('td[@class="time"]/p/text()')
                time_list = (str(time_tag[0]).strip() + " " + str(time_tag[1]).strip()).split(" ")
                y_m_d = time_list[0]
                transfer.year = y_m_d.split(".")[0]
                transfer.month = y_m_d.split(".")[1]
                transfer.day = y_m_d.split(".")[2]
                # 时分
                h_m = time_list[1]
                transfer.hour = h_m.split(":")[0]
                transfer.minutes = h_m.split(":")[1]

                # memo标签(交易备注)
                try:
                    transfer.memo = str(tr.xpath('td[@class="memo"]/div[@class="fn-hide content-memo"]/div[@class="fn-clear"]/p[@class="memo-info"]/text()')[0]).strip()
                except:
                    transfer.memo = ""

                # 交易名称
                try:
                    transfer.name = str(tr.xpath('td[@class="name"]/p/a/text()')[0]).strip()
                except:
                    try:
                        transfer.name = str(tr.xpath('td[@class="name"]/p/text()')[0]).strip()
                    except:
                        transfer.name = ""

                # 交易订单号(商户订单号和交易号)
                code = tr.xpath('td[@class="tradeNo ft-gray"]/p/text()')
                if "流水号" in code[0]:
                    transfer.serial_num = (str(code[0]).split(":"))[-1]
                    transfer.seller_code = ""
                    transfer.transfer_code = ""
                else:
                    code_list = str(code[0]).split(" | ")
                    transfer.serial_num = ""
                    transfer.seller_code = (str(code_list[0]).split(":"))[-1]
                    transfer.transfer_code = (str(code_list[-1]).split(":"))[-1]

                # 对方(转账的标签有不同...奇葩的设计)
                if transfer.memo == "":
                    try:
                        transfer.opposite = str(tr.xpath('td[@class="other"]/p[@class="name"]/span/text()')[0]).strip()
                    except:
                        transfer.opposite = str(tr.xpath('td[@class="other"]/p[@class="name"]/text()')[0]).strip()
                else:
                    try:
                        transfer.opposite = str(tr.xpath('td[@class="other"]/p[@class="name"]/span/text()')[0]).strip()
                    except:
                        transfer.opposite = str(tr.xpath('td[@class="other"]/p/text()')[0]).strip()

                # 金额
                transfer.money = str(tr.xpath('td[@class="amount"]/span/text()')[0]).replace(" ", "").replace("+", "")

                # 状态
                transfer.status = tr.xpath('td[@class="status"]/p[1]/text()')[0]

                # 用户
                transfer.user = USERNAME

                # 交易类型
                transfer.tag = option

                # 输出
                logger.info(transfer)
                mgo.insert_data_with_eval(transfer)

            # 判断是否存在下一页的标签
            if is_next_page:
                # 智能等待 --- 3

                # 抓取完当页的数据后,滚动事件到底部，点击下一页
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # 智能等待 --- 4
                time.sleep(random.uniform(1, 2))

                # 点击下一页
                next_page_btn = self.browser.find_element_by_link_text('下一页')
                next_page_btn.click()
                self.turn_page(option)
            else:
                return

        except Exception as err:
            logger.debug(err.with_traceback(err))
            logger.error('抓取出错,页面数据获取失败')
            return

    # 抓取数据
    def get_data(self):
        # 判断登录状态
        status = self.login_status()

        logger.info("当前页面: " + self.browser.current_url)

        # 上一个版本用的是BeautifulSoup进行标签获取,现在改成用lxml获取
        html = self.browser.page_source
        selector = etree.HTML(html)

        # 我的页面
        user_limit = selector.xpath('//div[@class="i-assets-body"]/div/p[1]/text()')[0]
        user_limit_money = selector.xpath('//div[@class="i-assets-body"]/div/p[1]/span/strong/text()')[0] + \
                           selector.xpath('//div[@class="i-assets-body"]/div/p[1]/span/strong/span/text()')[0]

        user_all = selector.xpath('//div[@class="i-assets-body"]/div/p[2]/text()')[0].strip().replace(":", "")
        user_all_money = selector.xpath('//div[@class="i-assets-body"]/div/p[2]/strong/text()')[0] + \
                         selector.xpath('//div[@class="i-assets-body"]/div/p[2]/strong/span/text()')[0]

        # 用户花呗当前额度和全部额度的字典
        user_hua_bei_dict = {"user": self.username, user_limit: user_limit_money, user_all: user_all_money}

        # 先写入到数据库
        mgo = Mgo(logger)
        mgo.insert_data(user_hua_bei_dict, "user_info")

        # 智能等待 --- 6
        time.sleep(random.uniform(0.2, 0.9))

        # 获取完后跳转到账单页面
        # self.browser.get(Bill_Url)
        self.browser.find_element_by_xpath('//ul[@class="global-nav"]/li[@class="global-nav-item "]/a').click()

        if status:
            # 下拉框a标签点击事件触发
            self.browser.find_element_by_xpath('//div[@id="J-datetime-select"]/a[1]').click()

            # 选择下拉框的选项
            self.browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="customDate"]').click()

            # 起始日期和最终日期的初始化
            begin_date_tag = "beginDate"
            begin_date = "2017.07.14"
            end_date_tag = "endDate"
            end_date = "2017.10.14"

            # 设置起始日期
            remove_start_time_read_only = "document.getElementById('" + begin_date_tag + "')." \
                                                                                         "removeAttribute('readonly')"
            self.browser.execute_script(remove_start_time_read_only)
            ele_begin = self.browser.find_element_by_id(begin_date_tag)
            ele_begin.clear()
            self.slow_input(ele_begin, begin_date)

            # 智能等待 --- 1
            time.sleep(random.uniform(1, 2))

            # 设置结束日期
            remove_end_time_read_only = "document.getElementById('" + end_date_tag + "').removeAttribute('readonly')"
            self.browser.execute_script(remove_end_time_read_only)
            ele_end = self.browser.find_element_by_id(end_date_tag)
            ele_end.clear()
            self.slow_input(ele_end, end_date)

            # 智能等待 --- 2
            time.sleep(random.uniform(0.5, 0.9))

            # 选择交易分类
            self.browser.find_element_by_xpath('//div[@id="J-category-select"]/a[1]').click()

            # 选择交易分类项
            # 购物 SHOPPING
            # 线下 OFFLINENETSHOPPING
            # 还款 CCR
            # 缴费 PUC_CHARGE
            if self.transfer_option == "1":
                self.browser.find_element_by_xpath(
                    '//ul[@class="ui-select-content"]/li[@data-value="SHOPPING"]').click()
            elif self.transfer_option == "2":
                self.browser.find_element_by_xpath(
                    '//ul[@class="ui-select-content"]/li[@data-value="OFFLINENETSHOPPING"]').click()
            elif self.transfer_option == "3":
                self.browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="CCR"]').click()
            elif self.transfer_option == "4":
                self.browser.find_element_by_xpath(
                    '//ul[@class="ui-select-content"]/li[@data-value="PUC_CHARGE"]').click()

            # 智能等待 --- 3
            time.sleep(random.uniform(1, 2))

            # 按钮(交易记录点击搜索)
            self.browser.find_element_by_id("J-set-query-form").click()
            logger.info("跳转到自定义时间页面....")
            logger.info(self.browser.current_url)

            # 进行页面数据抓取
            self.turn_page(option=self.transfer_option)
        else:
            logger.error('抓取出错,登录失败!')

    # 关闭浏览器
    def close_browser(self):
        self.browser.close()

    # 主启动类
    def main(self):
        # 检测是否为项目默认值
        if USERNAME == "支付宝账号" or PASSWORD == "支付宝密码":
            logger.info("请输入正确的账号和密码!")
            raise ValueError("Account or password is illegal!")

        # 选择日志等级(后期改为用参数进行选择)
        logging.info("请输入日志等级: (1和回车是debug模式, 2是info)")
        log_level = input()
        if log_level == "" or log_level == "1":
            logging.debug("日志等级为: DEBUG")
            logger.setLevel("DEBUG")
        elif log_level == "2":
            logging.debug("日志等级为: INFO")
            logger.setLevel("INFO")
        else:
            raise ValueError("logger choice is illegal!")

        # 选择爬取交易选项
        logging.info("请输入交易选项类别: (1和回车是购物类, 2是线下, 3是还款, 4是缴费)")
        transfer_option = input()
        if transfer_option == "" or transfer_option == "1":
            transfer_option = "1"
        elif transfer_option == "2":
            transfer_option = "2"
        elif transfer_option == "3":
            transfer_option = "3"
        elif transfer_option == "4":
            transfer_option = "4"

        # 赋值交易选择的类别
        self.transfer_option = transfer_option

# if __name__ == '__main__':
#     # 入口
#     alipay = AlipayBill(HEADERS, USERNAME, PASSWORD)
#
#     # 选择浏览器
#     alipay.choose_browser()
#
#     # 初始化结束后，开始登陆
#     alipay.get_cookies()
#
#     # 登陆后开始获取数据
#     alipay.get_data()
#
#     # 关闭浏览器
#     alipay.close_browser()
