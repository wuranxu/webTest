# webTest框架介绍


### 简介

    本框架基于Python3+playwright+unittest组成，用户以Page Object的模式编写用例。

    元素的定位和操作按照页面划分，达到Web端自动化回归测试的目的，
    并生成测试报告。浏览器兼容性暂时未完善。

特点:

- 💚 支持用例重跑及自动错误截图
- 💙 使用antd美化html报告
- 💜 采用po模式，定位元素与实际操作分离，同一个页面的操作代码可复用
- 🖤 优化api，智能等待用例，拒绝代码中time.sleep等待元素
- 💔 支持视频录制功能(playwright自带)
- 封装自带Api，与selenium保持统一


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

mac/Linux/windows: 
```pip3 install -r requirements.txt -i https://pypi.douban.com/simple```

- 安装playwright相关浏览器

```shell
playwright install
```

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


- config.py

  用于存放绝大部分配置。继承于BaseConf类, 可拥有自己的配置。

- requirements.txt

  用于存放本框架所需库。

- start_test.py

  存放组织用例, 生成测试套件, 运行测试用例等函数。

- webdriver_test.log

  存放测试用例执行时候的有关操作和错误信息等。


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

  Linux/mac: ```pip3 install -r requirements.txt```

  windows: ```pip3 install -r requirements.txt```


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
  - 日志在logs/webTest.log查看
  - Page页面编写此页面需要的操作及元素
  - Location类是封装了WebElement, 其中包含name, value, 默认以css方式定位
  - Location类实例化的时候可指定第三个参数, 方便使用其他定位的同学。如:

    ```menu = Location("大后台左侧菜单", ".menuItem", "XPATH")```
  
### 通过cookie控制免登陆

  参考base_case.py