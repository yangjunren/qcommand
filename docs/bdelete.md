# 简介

`bdelete` 指令用来批量删除空间中的文件。


# 格式
```
qcommand bdelete <bucket> <inputfile> [--successfile= --failurefile= --threacount=]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|bucket|空间名称，可以为公开空间或者私有空间|
|inputfile| 包含文件名的txt文件|
|successfile| 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdelete 目录下|
|fileurefile| 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdelete 目录下|
|threadcount| 并发数，可选参数，默认值为3|

# 示例

`inputfile.txt` 文件内容示例： 

```
123.jpg
qiniu.png
test.html
```

删除`upload30`空间中`inputfile.txt`中的文件。

```
qcommand bdelete upload30 inputfile.txt
```

