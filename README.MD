# 支付宝账单爬虫
---
* 目录
    * [开发环境](#DevelopEnv)
    * [安装方式](#HowToInstall)
    * [功能](#Function)
    * [技术点](#TechPoints)
    * [疑难点](#QuestionAndIssue)

---
<h3 id="DevelopEnv">开发环境</h3>
Python 版本：3.4.4
Python库列表：

    * BeautifulSoup4 --- `4.6.0`
    * Selenium --- `3.5.0`
    * requests --- `2.18.4`

---

<h3 id="HowToInstall">安装方式</h3>
```shell
    pip install BeautifulSoup4
    pip install selenium
    pip install requests
```
Ps:此外还需要安装PhantomJs，具体配置请看官网文档
[PhantomJs官网]http://phantomjs.org/

---
<h3 id="Function">功能</h3>
1、尝试模拟登录支付宝，并检测是否有手机验证码
2、成功登录后获取账单记录（待抓取）

---
<h3 id="TechPoints">技术点</h3>
1、通过 selenium 模拟登录支付宝（更加拟人化）
2、利用python requests库的session更新cookies

---
<h3 id="QuestionAndIssue">疑难点（待解决）</h3>
1、账单抓取翻页的问题
2、验证码的问题，需要手动输入，用户体验不好（且支付宝有时限）
3、cookie的持久性问题

---



