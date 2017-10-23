# 支付宝账单爬虫 --- v2

---
<h3 id="Q&A">问题反馈</h3>
在使用中有任何问题，可以反馈给我，以下联系方式跟我交流
* Wechat: Leo-sunhailin
* E-mail: 379978424@qq.com
* Github URL: [项目链接](https://github.com/sunhailin-Leo/Alipay-Spider)

---
* 目录
    * [开发环境](#DevelopEnv)
    * [安装方式](#HowToInstall)
    * [功能](#Function)
    * [技术点](#TechPoints)
    * [疑难点](#QuestionAndIssue)
    * [未来开发目标](#Future)

---
<h3 id="DevelopEnv">开发环境</h3>
Python 版本：3.4.4（尽量不要使用python3.5，因为lxml库的源码暂时有问题本项目需要用到etree这个方法）
Python库列表：

* lxml --- `3.8.0`
* Selenium --- `3.5.0`
* requests --- `2.18.4`
* pymongo --- `3.5.1`

---

<h3 id="HowToInstall">安装方式</h3>
```shell
    pip install lxml
    pip install selenium
    pip install requests
    pip install pymongo
```
```python
# 爬虫+分析模块启动
python starter.py

# 如果有数据的情况下可以直接跑分析模块
python analyse_starter.py
```
Ps:

* 此外还需要安装PhantomJs，具体配置请看官网文档[PhantomJs官网]http://phantomjs.org/
* 如果使用Chrome driver或者是FireFox的可以参考Selenium官网的文档
[Selenium文档]http://selenium-python-docs-zh.readthedocs.io/zh_CN/latest/
~~* 需要配置MongoDB数据库,这一版本暂时没保存到文件中。（以后待扩展修改）~~
* 可以写入到SQLite和MongoDB中,后续加入导出脚本将MongoDB的数据导出


---
<h3 id="Function">功能</h3>
1、模拟登录支付宝，并检测是否有手机验证码
2、成功登录后获取账单记录花呗额度(花呗使用清单，暂时无法获取)
3、Selenium和MongoDB和SQLite的配置通过conf文件进行配置（按需配置）
4、数据结果写入到MongoDB或SQLite数据库中
5、加入数据分析模块（待完善）

---
<h3 id="TechPoints">技术点</h3>
1、通过selenium + webdriver(PhantomJs & ChromeDriver) 模拟登录支付宝
2、利用python requests库的session更新和保存cookies
3、通过conf文件夹下的.conf文件维护配置,更人性化,避免改动代码
4、支持选择数据源的形式进行写入(MongoDB和Sqlite数据库)
5、支持SQLite可以免部署数据库进行写入，轻量化项目
6、暂时性找到不需要验证码登陆的链接，跳转到个人界面暂时不用验证码
7、加入了python collection库中的OrderDict有序字典

---
<h3 id="QuestionAndIssue">疑难点（待解决）</h3>
~~1、账单抓取翻页的问题~~
~~2、验证码的问题，需要手动输入，用户体验不好（且支付宝有时限）~~
3、cookie的持久性问题(未来可能加入Redis进行存储)
~~4、验证码的问题补充,因为目前项目使用PhantomJs和Chrome两个浏览器验证码的出现概率（PhantomJs 小于 Chrome）~~
~~5、PhantomJs还存在的问题在于，输完密码之后点击登录时，概率卡死代码无法执行下去，暂时不知道问题出在哪里（网页 or 代码）~~
6、爬虫整体爬取速度需要一定时间（待优化）
7、数据分析的模块，待优化。分析的需求比较粗糙，待细化

---

<h3 id="Future">未来开发任务</h3>
1、首要目标：解决Bug列表
2、设计Web页面进行可视化操作。
3、考虑模拟登陆到手机版的支付宝，获取花呗使用清单(难度较大)
4、完善数据分析的结果,并接入可视化展示。

---
