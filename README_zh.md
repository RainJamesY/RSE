# Rain的搜索引擎 -- 信息检索课程项目

----------------------------------------------------------------------------------------------------

版权所有 （c） 2022-2023 中国 武汉大学 ，姚栋宇。保留所有权利。

根据 Apache 许可证 2.0 版获得许可

----------------------------------------------------------------------------------------------------

## 环境配置

对于这个项目，我们使用了python 3.7.0。我们建议您配置新的虚拟环境：

```shell
python -m venv ~/venv/RSE
source ~/venv/RSE/bin/activate
```

在该环境中，可以使用以下命令安装要求内容：

```shell
pip install -r requirements.txt 
```

## 配置数据集

**TDT3:** 请通过[此处](https://drive.google.com/file/d/10Cphorhmc3m_tWHcqcvbrFQaPyA01BYs/view?usp=share_link)下载TDT3数据集并 将其解压到`/tdt3`文件夹

## 在浏览器中运行该引擎

请切换到根目录并在命令行中输入：

```python
run server.py
```

该引擎会在 http://127.0.0.1:5000网页运行

## 创建索引

为了自行创建索引，您可以在home界面点击左上角的'build index'按钮

![image-20230518025338191](https://rainjamesy-image-host.oss-cn-beijing.aliyuncs.com/img/image-20230518025338191.png)

或者您可以下载我们创建好的索引目录，链接放置在[此处](https://drive.google.com/file/d/1YMMRN0qk6oy3Ngta7AVzGAUhzMtNx1lJ/view?usp=sharing)。

## 通过关键词检索

Rain的搜索引擎提供了四种检索方式，它们都会返回Top-N的相关性结果、相关性分数、排名、文档号和文档摘要。

- Show matched words
- Show matched texts
- Search with ambiguity
- Search by stemming

您可以根据场景和需求自行选择检索方式。

## 加入更多的功能

本项目欢迎所有在此基础上添加的拓展功能，比如查询词纠错、同义词查询等等。







