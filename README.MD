# 支付宝账单爬虫 --- Beta v1
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
Python 版本：3.4.4（尽量不要使用python 3.5,因为lxml库的问题，需要用到etree）
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
Ps:

* 此外还需要安装PhantomJs，具体配置请看官网文档[PhantomJs官网]http://phantomjs.org/
* 如果使用Chrome driver或者是FireFox的可以参考Selenium官网的文档
[Selenium文档]http://selenium-python-docs-zh.readthedocs.io/zh_CN/latest/
* 需要配置MongoDB数据库,这一版本暂时没保存到文件中。（以后待扩展修改）


---
<h3 id="Function">功能</h3>
1、尝试模拟登录支付宝，并检测是否有手机验证码
2、成功登录后获取账单记录（待抓取）
3、Selenium和MongoDB的配置通过conf文件进行配置（按需配置）
4、数据结果写入到MongoDB数据库中

---
<h3 id="TechPoints">技术点</h3>
1、通过 selenium 模拟登录支付宝（更加拟人化）
2、利用python requests库的session更新cookies
3、通过conf维护,更人性化,避免改动代码

---
<h3 id="QuestionAndIssue">疑难点（待解决）</h3>
~~1、账单抓取翻页的问题~~
2、验证码的问题，需要手动输入，用户体验不好（且支付宝有时限）
3、cookie的持久性问题
4、验证码的问题补充,因为目前项目使用PhantomJs和Chrome两个浏览器
    验证码的出现概率（PhantomJs 小于 Chrome）
5、PhantomJs还存在的问题在于，输完密码之后点击登录时，概率卡死
代码无法执行下去，暂时不知道问题出在哪里（网页 or 代码）

---

<h3 id="Future">未来开发任务</h3>
1、首要目标：解决Bug列表
2、设计Web页面进行可视化操作。

---
