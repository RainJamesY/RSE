# Rain's Search Engine -- Information Retrieval Final Project

----------------------------------------------------------------------------------------------------

Copyright (c) 2022-2023 WHU China, Dongyu Yao. All rights reserved. 

Licensed under the Apache License, Version 2.0

----------------------------------------------------------------------------------------------------

For Chinese version of Instructions,  please refer to  [Rain的搜索引擎](README_zh.md)

## Setup Environment

For this project, we used python 3.7.0. We recommend setting up a new virtual
environment:

```shell
python -m venv ~/venv/RSE
source ~/venv/RSE/bin/activate
```

In that environment, the requirements can be installed with:

```shell
pip install -r requirements.txt 
```

## Setup Datasets

**TDT3:** Please, download tdt3.zip from [here](https://drive.google.com/file/d/10Cphorhmc3m_tWHcqcvbrFQaPyA01BYs/view?usp=share_link) and extract them to `/tdt3`.

## Open Search Engine in your browser

Please switch to the root folder and use command

```python
run server.py
```

The project will then be running on http://127.0.0.1:5000

## Create Index

For creating index on your own, press the 'build index' bottom on the top left of the screen.

![image-20230518025338191](https://rainjamesy-image-host.oss-cn-beijing.aliyuncs.com/img/image-20230518025338191.png)

Or you may use our provided document index for TDT3 dataset, download [here](https://drive.google.com/file/d/1YMMRN0qk6oy3Ngta7AVzGAUhzMtNx1lJ/view?usp=sharing)

## Search for your Queries

There are four types of searching provided, they all return with Top-N relavance score, rankings, docID and snippets.

- Show matched words
- Show matched texts
- Search with ambiguity
- Search by stemming

you may choose the type and the number of results based on your needs.

## Adding more components

This project welcomes any additional functions (such as correction of query, synonymous queries and so on) to be added.







