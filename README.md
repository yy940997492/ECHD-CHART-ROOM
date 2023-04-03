## 多人聊天室介绍

>  使用环境：Python 3.8 + Mysql 8.0
>
> 2023年4月3日：新增支持基于ECDH+AES端到端加密通讯
> 需要额外创建一张表,执行chatdb.sql脚本后，再执行chatdb2.sql脚本
>
> 主要技术：Socket 实现实时聊天和通知等双向性的功能，HTTP 实现登录注册等单向性的功能



## 环境

> 使用 Python3.8 + MySQL8.0



## 功能

- 登录/注册
- 加好友
- 与好友私聊
- 创建群
- 在群里进行群聊
- 聊天发表情
- 聊天发文件
- 聊天发图片，并且预览显示
- 新消息声音提醒
- 聊天记录保存本地
- 聊天文件保存本地



## 运行教程

### 1、检查环境版本

**确保 python 版本为3.8 或 3.9 ！！！！**

**确保 MySQL 版 本为8.0 ！！！！**



若环境不是上述版本，请先安装。

MySQL 8.0 的安装可参考此文章： https://blog.csdn.net/xy_best_/article/details/116698099 

### 2、初始化数据库

执行chatdb.sql脚本，初始化数据库。有以下两种执行方式（任选其一）：



方式一：在cmd登录MySQL后，使用source命令执行，**source + chatdb.sql的绝对路径**

```
source F:\multiplayer-chat-room\chatdb.sql
```



方式二：使用Navicat等工具执行chatdb.sql脚本

### 3、代码导入到pycharm中

**将代码解压后放置在非C盘的目录中，千万不要放在桌面！！！！**

**将代码解压后放置在非C盘的目录中，千万不要放在桌面！！！！**

**将代码解压后放置在非C盘的目录中，千万不要放在桌面！！！！**



代码的导入有两种方式，推荐使用方式一。



**代码导入方式一（推荐）：**

打开pycharm后，点击左上角的 File ->> Open ->> 选择解压后的代码的文件夹（注意选择python文件所在的目录）

如下图所示

![image-20220526092152184](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220526092152184.png)



打开后，会弹出一个python版本选择框，如下图所示

**需要在 Base Interpreter中选择python 3.8的版本**

![image-20220526092656618](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220526092656618.png)



点击确定后，等待项目安装需要的库，安装完成后，转至步骤4





**代码导入方式二：**

若open后没出现方式一所示的提示框，则需要手动安装库，安装方法如下：



在open代码后，先点File ->> Settings

**在Settings中找到Interpreter项，如下图所示，修改上方的python版本为3.8。**

> 若安装过3.8但此处没有3.8选项，可通过+号浏览3.8的安装目录进行添加。

![image-20220526093217440](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220526093217440.png)



选择python版本后，在pycharm下方点击Terminal打开控制台，在控制台中执行下列命令，安装项目所需的库。

**注意：在requirements.txt同级的目录执行下列命令**

```properties
pip install -r requirements.txt
```

![image-20220526093453609](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220526093453609.png)

### 4、修改server.conf文件配置

主要需要修改的配置为数据库的账号和密码，例如下方数据库账号为root，数据库密码为123

配置文件说明如下：

```yml
[server]

# 服务端的ip地址
SERVER_IP = 127.0.0.1

# Http服务的端口号
HTTP_PORT = 8000

# socket服务的端口号
SOCKET_PORT = 8001

# 数据库连接配置 下方root是账号，123是密码
SQLALCHEMY_DATABASE_URI = mysql://root:123@127.0.0.1:3306/chatdb
```

### 5、运行服务端

运行ChatServer.py文件。

**注意：每次运行都需要先运行此服务端。因为这是整个程序的服务端**



**（1）若运行后，控制台出现如下图所示绿色两行字，则表示运行正常，直接查看文档的【6、pycharm配置同时运行同一个文件】步骤：**



![image-20230108011547954](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20230108011547954.png)



**（2）若运行后，控制台出现如下图所示，则表示运行方式有误：**

![1](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/1.jpg)



需要配置运行方式，点击【Edit Configurations】，如下图所示

![image-20220426233429059](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220426233429059.png)



将ChatServer配置为Python方式运行，不要使用默认的Flask运行

![image-20230108011402602](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20230108011402602.png)





**（3）若运行后，控制台出现如下图所示红色两行字，则表示无法访问数据库**

解决方式是：

（1）检查是否已安装MySQL，且版本为8.0的

（2）检查【server.conf】文件中的数据库配置，检查数据库的地址、端口、账号、密码等是否正确

（3）检查是否根据【步骤一】成功执行chatdb.sql脚本文件

![image-20230108011856771](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20230108011856771.png)



### 6、pycharm配置同时运行同一个文件

> 因为pycharm运行客户端默认同时只能运行同一个文件，需要配置才能同时运行同一个文件

- 点击运行按钮左侧的多选框，点击【Edit Configurations】，如下图所示：

![image-20220426233429059](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20220426233429059.png)



- 左边选中ChatLogin，勾选上方的【Allow parallel run】多选框，如下图红框所示
- **若左侧无ChatLogin选择，先运行一次ChatLogin后再配置**

![](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20230227202331064.png)





- 确保上图中蓝框和下图中蓝框所选择的Python环境一致（注意上图**不能**选择 Project Default 的python环境，直接选择 Python 3.8 的环境）

![](https://wangcong-images.oss-cn-guangzhou.aliyuncs.com/img/image-20230227202519205.png)



### 7、运行客户端

同时运行多个ChatLogin.py，分别登录不同的用户即可进行聊天。



### 8、常见错误

- 弹窗提示参数异常

1. 检查数据库账号密码
2. 未运行数据库
3. 检查python、mysql版本
4. 检查导入的包的版本是否和requirements.txt中一致

- 缺少包

1. 检查python、mysql版本
2. 检查导入的包的版本是否和requirements.txt中一致，包的版本很重要！！！！

