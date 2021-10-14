

## 安装软件: 
1. Anaconda, 下载地址: https://www.anaconda.com/products/individual
   
2. PyCharm, 下载地址: https://www.jetbrains.com/pycharm/download/


##  python解析器和虚拟环境
1. Python是一门解释性的语言，需要解析器去帮把写好的代码运行起来，这就是python的运行环境。
      
2. 一个电脑可以运行很多个环境，类似微信的多开的功能，每个解析器的内容完全隔离开。


## conda创建虚拟环境:
在终端termial, window在cmd命令行中输入 
> conda create -n <你的环境的名称> python=3.7 # 输入英文拼音，不要带<>

> conda create -n leijmtrade python=3.7

## conda激活安装环境
> conda activate <你的环境名称> # <> 表示变量

> conda activate vnpy
## 查看环境列表
> conda env list 


## 删除环境
> conda deactivate # 先激活自己当前的环境

> conda remove -n <你的环境名称>

> conda remove -n study --all 
  

# Pycharm 配置环境
PyCharm需要能把代码跑起来，需要配置解析环境。 Window系统设置解析器: 
```
file --> setting  --> project --> interpreter --> 找你的环境解析器

```
    
MacOS系统设置解析器: 
```
Pycharm --> Preferences ---> project ---> interpreter --> 找到你的环境环境解析器

```



## 1. 软件要求
通过pip install的方式进行安装
> pip install git+https://github.com/zxc1342802/jiamtrader.git

更新到最新, 后面加上-U表示更新到最新的
> pip install git+https://github.com/zxc1342802/jiamtrader.git -U 

3. 启动界面 
> python main.py

## 注意事项
如何确定自己电脑的网络是否能访问币安交易所呢？

## step 2 jiamtrader

> pip install git+https://github.com/zxc1342802/jiamtrader.git

在终端输入
> ping api.binance.com 

> pip uninstall jiamtrader 

> pip install git+https://github.com/zxc1342802/jiamtrader
>
>
>
数据库配置：
>新建文件：vt_setting.json

{
     "database.driver": "sqlite",               
    "database.database": "database.db"
}

{
    "database.driver": "mongodb",
    "database.database": "jiamtrader",
    "database.host": "localhost",
    "database.port": 27017,
    "database.authentication_source": "admin"
}