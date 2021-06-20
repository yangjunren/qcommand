# 简介

`bchstatus`命令用来批量修改文件状态（0表示启用，1表示禁用）。

# 格式
```
qcommand bchstatus <bucket> <inputfile> [--sep= --successfile= --failurefile= --threacount=]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|bucket|空间名称，可以为公开空间或者私有空间|
|inputfile| 包含文件名和文件状态的txt文件|
|sep|inputfile 文件中 需要修改存储类型的文件名与存储类型（0 表示标准存储；1 表示低频存储；2 表示归档存储）之间的分割符（默认是,分割）|
|successfile| 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bchstatus 目录下|
|fileurefile| 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bchstatus 目录下|
|threadcount| 并发数，可选参数，默认值为3|

# 示例

`inputfile.txt` 文件内容示例： 

```
123.jpg,0
qiniu.png,1
test.html,0
```

修改`upload30`空间中`inputfile.txt`中的文件存储类型。

```
qcommand bchstatus upload30 inputfile.txt
```

