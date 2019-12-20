# FiscoBcos-PyConsole
FiscoBcos 的区块链浏览器

### 简介
基于python-sdk开发的区块链浏览器，页面参考原始的区块链浏览器
```
https://github.com/FISCO-BCOS/fisco-bcos-browser.git
```
点击进入原始 [区块链浏览器](https://github.com/FISCO-BCOS/fisco-bcos-browser.git)

本工程只需要Python3.5 + 即可

原始工程需要Python2.7, Java, 以及MySQL.因此进行了简化,不需要任何数据库

#### 项目效果
首页

![首页截图](https://github.com/Wall-ee/FiscoBcos-PyConsole/blob/master/index.png)

交易详情

![首页截图](https://github.com/Wall-ee/FiscoBcos-PyConsole/blob/master/transaction_detail.png)

### 环境要求
1. Fisco Bcos 网络配置完毕
2. Python3.5+
3. Flask/Tornado安装
4. 安装Fisco Bcos 的Python-SDK
```
https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/python_sdk/install.html
```
点击进入[Python SDK](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/python_sdk/install.html)

轻量级Python的Http服务器--Flask [官方文档](https://flask.palletsprojects.com/en/master/)

高性能异步非阻塞Python服务器(FaceBook开源)--Tornado [官方文档](http://www.tornadoweb.org/en/stable/)
### 使用方法

1. 安装Fisco Bcos的python-sdk，python-sdk配置规则参照官方教程；

2. 将python-fisco-consle下面的所有文件与文件夹一并复制放入python-sdk根目录。其中包括static静态页面目录，以及flask和tornado 的启动文件；

3. 启动fisco_browser_flask.py 或 fisco_browser_tornado.py 则分别启动flask/tornado 的工程；

4. 主页访问地址:http:ip:5555/index.html

### 区块链浏览器的api详解：

1. 浏览器可配合python-sdk配置的区块链查看三个主要模块：首页概览、区块列表、交易列表。
2. api分为flask版和tornado版，实现功能基本相同。
3. api启动自动部署合约，获取合约地址，合约地址在交易上链的时候需要用到。（可获取一次合约后存入缓存，之后启动查询缓存）
4. 如果只使用浏览器的查询，不需要部署合约，也无需合约地址。
5. 每次部署合约都会生成一个区块，区块内包含一个交易。


### API详解：

>GET 查询api：

/query_info/index  获取主页的数据，包括预览，交易量图，最近的区块和交易

/query_info/block_list  获取区块列表，根据区块高度或者区块哈希搜索或者根据页数取10个区块列表

/query_info/transaction_list  获取交易列表，根据区块高度或者交易哈希搜索或者根据页数取10个交易列表

/query_info/block_detail   根据区块哈希，获取区块的详情

/query_info/transaction_detail   根据交易哈希，获取交易详情和交易回执

>POST 上传交易api：

/sendTrans/rawTrans   上传json格式数据，发送交易上链 