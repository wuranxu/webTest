# webTest框架介绍


### 简介

    本框架基于Python3+selenium3+unittest组成，用户以Page Object的模式编写用例。

    元素的定位和操作按照页面划分，达到Web端自动化回归测试的目的，
    并生成测试报告。浏览器兼容性暂时未完善。

    本例子展示了一个必应首页搜索"龙珠超"的测试用例，比较简陋。

列举一下相关的亮点:

- ❤️ 支持xmind文件转为测试用例，目前存在部分问题
- 💛 支持chrome驱动自动下载
- 💚 支持用例重跑及自动错误截图
- 💙 使用antd美化html报告
- 💜 采用po模式，定位元素与实际操作分离，同一个页面的操作代码可复用
- 🖤 优化api，智能等待用例，拒绝代码中time.sleep等待元素
- 💔 其他（可在下方留言或github issue提需求）

### 运行日志

![image.png](http://upload-images.jianshu.io/upload_images/6053915-6b49d999bd81fd03.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 过程截图

![image.png](http://upload-images.jianshu.io/upload_images/6053915-2f1cb468358719c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 效果展示

![image.png](https://upload-images.jianshu.io/upload_images/6053915-792a2f538e5e2bb7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 快速上手

- 从远程仓库拉取代码

```git clone https://github.com/wuranxu/webTest.git```

![image.png](http://upload-images.jianshu.io/upload_images/6053915-535641f29e7df072.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 安装依赖包

进入下载好的webTest目录，并在此目录运行安装依赖, 需要安装好pip(默认自带的就行)

mac/Linux/windows: ```pip3 install -r requirements.txt -i https://pypi.douban.com/simple```

- 运行demo

在webTest目录输入命令(确保chrome浏览器已安装, 驱动会自行下载):

```python3 start_test.py```

![image.png](http://upload-images.jianshu.io/upload_images/6053915-3698662b1b177b18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 配置说明

    见config.py，大部分说明都有对应的描述，RETRY是全局重试次数。可以参考XmindTest.py文件里面的retry字段，设置单个用例的重试次数。
   

### 环境配置
##### 注: 无桌面版Linux目前只做到支持firefox
- os: Windows/Mac os x/Linux
- Python3.x
- Chrome浏览器


### 目录结构


```
project

└───error
|
└───database
|
└───logs
|
└───xmind
|
└───page
|
└───report
|
└───tests
|   |    base_case.py
|
└───templates
|   |   report_templates.html
└───result
|   |   report_templates.html
|   |   generator.py
|   |   text_test_result.py
|
└───chromedriver
│   │   chromedriver.exe
|
└───util
|   |   chrome.py
|   |   decorator.py
|   |   driver.py
|   |   utils.py
|   |   logger.py
|   |   web_tool.py
|
│   README.md
│   run_case.py
|   requirements.txt
│   config.py
|   webdriver_test.log


```

### 内容介绍

- chromedriver

  存放chromedriver驱动, 若本机未安装chromedriver则自动匹配本机chrome版本下载对应驱动。

- database

  存放Mysql和Mongodb的连接类
  
- error

  异常分类

- screenshot

  存放出错截图, 目前根据用例名称创建文件夹并存放。

- logs

  存放所有日志文件, 目前只有webdriver_test.log, 主要目的是将日志区分开来。

- page

  页面目录, 可扩展, 针对不同模块的页面可设计不同目录结构。一般存放该页面的操作(Action)以及元素(Location), 用例具体断言不建议写于此处(因人而异)。

- Report

  存放测试报告，为html形式，可右键通过浏览器打开，使用chrome效果尤佳。

- templates

  存放html模板，传入测试结果以生成测试报告。

- result

  - generator.py

    是组织测试结果, 生成测试报告, 填入数据至html报告模板的方法。

  - text_test_result.py

    继承自unittest.TextTestResult类, 存放测试结果。

- tests

  测试套件目录, 可扩展, 子目录为某个测试集。测试集中存放测试用例。

  - base_case.py

    存放基础测试用例。


- util

  - chrome.py

    用于更新/下载chromedriver, 目前只支持mac os和windows系统。

  - decorator.py

    用于存放自动截图/重跑等装饰器, 主要是为测试函数添加错误截图以及重跑等功能。

  - driver.py

    继承自WebDriver类, 主要用于简化原生api以及添加切换frame/handle等api。

  - logger.py

    记录日志的功能函数。

  - web_tool.py

    用于Web自动化测试的工具类, 包括截图、获取用例等方法。

  - xmind_reader.py

    用于解析xmind文件，暂时不支持过于复杂的xmind。用例的大概编写方式如下图。
    ![image](http://upload-images.jianshu.io/upload_images/6053915-4f08935ff9ddff18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- xmind

  存放Xmind文件, xmind文件用于编写测试用例。


- config.py

  用于存放绝大部分配置。继承于BaseConf类, 可拥有自己的配置。

- requirements.txt

  用于存放本框架所需库。

- start_test.py

  存放组织用例, 生成测试套件, 运行测试用例等函数。

- webdriver_test.log

  存放测试用例执行时候的有关操作和错误信息等。


#### 注: 以上目录结构/命名可能并不合理, 还望海涵。

---

### 使用手册

##### 以下内容若已安装, 可跳过。

- 安装Python3

  [Python3.6下载地址](https://www.python.org/downloads/release/python-364/)

  下载对应操作系统的Python版本并安装。

- 下载IDE(非必须)

  推荐Pycharm

  [Pycharm下载地址](https://www.jetbrains.com/pycharm/)

- 安装必须的库

  目录中有install.py, 安装好Python之后, 在终端窗口中输入如下命令:

  Linux/mac: ```python3 install.py```

  windows: ```python install.py```

  注意: 安装时需要带上install.py路径或者进入该文件所在目录。


- Pycharm配置(若有)

  - 第一步: 配置项目Python环境

    File->Open

  ![image.png](http://upload-images.jianshu.io/upload_images/6053915-01ed844c0870d6c7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   选择webTest目录, 点击窗口右下角的Open

   ![image.png](http://upload-images.jianshu.io/upload_images/6053915-cd6a91df8687e4c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  打开Preferences, 在Project Interpreter里选择刚才安装Python的地址, 点击OK

  ![image.png](http://upload-images.jianshu.io/upload_images/6053915-e4ad74e6fc94703b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  - 第二步: 配置start_test.py

  点击Edit Configurations

 ![image.png](http://upload-images.jianshu.io/upload_images/6053915-7e2c8d7c3be8afb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 如果没有Python配置的话, 点击图中"+"图标, 然后选择Python并添加
 ![image.png](http://upload-images.jianshu.io/upload_images/6053915-5036e9d36e54da08.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 ![image.png](http://upload-images.jianshu.io/upload_images/6053915-92391a98b0d090c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 配置脚本
 ![image.png](http://upload-images.jianshu.io/upload_images/6053915-9bb907d9d3df9026.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 - 第三步: 运行用例

 右击start_test.py, 选择Run则为运行模式, Debug则为调试模式
 ![image.png](http://upload-images.jianshu.io/upload_images/6053915-9eae73a79ef61182.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 用例编写规则

  Python:

  - 可参考Search.py编写用例(最好用例的类名不重复)
  - 用例需要写在TestSuite/测试集/这种目录下
  - 用例需要继承base_case.py
  - 用例需要以test开头如test_bmp
  - 用例的test函数需要带上screenshot的装饰器, 不带无截图功能
  - 报告会按照时间生成, 且会写入2份report.html
  - 日志在webdriver_test.log查看
  - Page页面编写此页面需要的操作及元素
  - Location类是封装了WebElement, 其中包含name, value, 默认以css方式定位
  - Location类实例化的时候可指定第三个参数, 方便使用其他定位的同学。如:

    ```menu = Location("大后台左侧菜单", ".menuItem", "XPATH")```

  Xmind:

  - 画布(必填)

    为TestSuite名, 可允许重复画布名

  - 根元素(必填)

    为用例的Class名

  - 描述(最好有)

    为该用例的测试点

  - 页面(必填)

    需要填写Page下的页面, 子节点为其页面下需要用到的方法, 方法后如果还有子节点，则为该方法返回值, 若有多个返回值则用;分割且该返回值会被保留方便做断言

  - 跳过(不填默认生成用例)

    不为True的时候均会生成用例

  - 重跑次数(可选)

    用例若失败, 重新运行的次数, 默认为0。

  - 步骤(必填)

    子节点为页面方法或断言, 若以assert开头则为断言, 否则则判断为方法, 若在页面中忘了填写该方法, 则调用系统内部方法。

    方法节点的子节点为参数, 同样以;分割。

    断言的子节点为2或3个, 如assertEqual, 可理解是```A==B?true:msg```, 最后一个参数是msg, 具体出错原因。

  - 已知缺陷
    1. 截止到现在还未支持非页面方法调用如print;
    2. 不支持导入本用例需要的其他类库;
    3. 其他不爽的有待补充。



### 亮痛点

- 浏览器驱动

  - 问题: 浏览器驱动偶尔会与浏览器对应不上
  - 解决方案: 自动下载, 但只针对mac/win下的chrome, 且版本不能太低。firefox不支持, 任性。

- 集成jenkins

  - 问题: centos6.x不带桌面无法运行UI自动化用例
  - 解决方案:

    1. phantomJs(不合适, 还是要写出来)

       新版selenium使用的时候会提示被废弃, 建议用无头模式取代, 且运行不稳定。

    2. Chrome无头模式(centos7以上应可行)

       由于jenkins所在机器centos6.x版本过低, 被Chrome放弃支持, Chrome浏览器无法安装

    3. Firefox无头模式(目测不可行, 测太多次了记不住)

       Firefox可正常安装, 但是geckodriver比较挑浏览器版本, 多次试验不成功, 换了无数个浏览器版本+geckodriver版本后已经忘了是否可行。

    4. Firefox+虚拟桌面(目前解决方案)

       见用例driver.py文件。但不完美, 错误截图显示的网页内容都····一言难尽, 好像一个瞎子终于重获光明却发现自己满脸麻子。回到正题, 为什么不自动同步firefox驱动, 因为在c方案卡壳太久比较恶心。

       版本信息:

       geckodriver0.16

       selenium>=3.4

       firefox52.0

- 测试报告

  由于邮件不支持js和引入的css, 导致报告巨难看。所以采用了附件形式, 目前是个比较大的痛点。
  
- Page Object

  关于po, 确实也没有很深的研究, 只等小白鼠试水了。
  
- api封装

  api封装得还不够多, 除了常用方法以外。但是基本上每个方法都插入了显示等待, 大大降低了元素找不到, 点不到, 各种不到的可能性。
  
- 重跑

  解决了使用装饰器重跑用例不执行setUp+tearDown的问题。
  
- 错误截图

  截图用base64保存, 所以只有错误的时候才会截图。因为base64太大。
  
- Xmind编写用例

  这算一个小亮点吧。
  
- 自动化配置环境

  已完成, 方便使用。
  
- 数据库

  支持mongo和mysql。

- 执行效率

  目前是单线程, 后续可能会支持异步。