# app_proxy

### 1、组织架构
```angular2html
├── README.md
├── __init__.py
├── __pycache__
├── aapt.py               获取apk信息模块
├── bin                   运行文件
├── config.py             配置文件
├── database.py           数据库文件
├── format_data.py        写数据库文件
├── install_catch.py      抓包主入口
├── media                 说明文档媒体（不用管）
├── mitm_script.py        抓包文件
├── model.py              数据库模型
├── requirments.txt       依赖文件
└── utils.py              

```
### 2、抓包运行

#### 手机端
```angular2html
手机设置代理端口

手机和电脑必须在同一个局域网下

查找电脑ip

手机端wifi设置代理为手动
```

![img.png](https://github.com/Pineapple1996/app_proxy/blob/main/media/img2.png?raw=true)

证书安装
手机访问mitm.it,根据手机下载证书

![img.png](https://github.com/Pineapple1996/app_proxy/blob/main/media/img.png)

#### 电脑端
```angular2html
安装python3.8

安装pip

pip安装依赖包 pip -r requirments.txt

项目目录下，运行python3 install_catch.py apk文件路径
```
