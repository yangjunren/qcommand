# 简介

`listbucket`用来获取七牛空间里面的文件列表，可以指定文件前缀获取指定的文件列表，如果不指定，则获取所有文件的列表。

获取的文件列表组织格式如下（每个字段用,分隔）：

```
Key,Size,MimeType,PutTime,FileType,status
```

参考文档：[资源列举 (list)](http://developer.qiniu.com/code/v6/api/kodo-api/rs/list.html)

# 格式

```
qcommand listbucket <bucket> <outfile> [--prefix= --start= --end= --fileType= --suffix= --fsize= --stype=]
```

（1）获取空间中所有的文件列表，这种情况下，可以直接指定 `bucket` 参数和结果保存文件参数 `outfile` 即可。

```
qcommand listbucket <bucket> <outfile>
```

（3）获取空间中指定前缀的文件列表

```
qcommand listbucket <bucket> <outfile> --prefix=123/
```

# 鉴权

需要在使用了`account`设置了`AccessKey`, `SecretKey` 和  `Name` 的情况下使用。

# 参数

|参数名|描述|可选参数|
|------|------|----|
|bucket|空间名称，可以为私有空间或者公开空间名称|N|
|outfile|获取的文件列表保存在本地的文件名|N|
|prefix|七牛空间中文件名的前缀，该参数为可选参数，如果不指定则获取空间中所有的文件列表|Y|
|start|开始时间，该参数为可选参数，指定后表示列举start时间之后上传的文件，如果不指定则获取空间中所有的文件列表|Y|
|end|结束时间，该参数为可选参数，指定后表示列举end时间之前上传的文件，如果不指定则获取空间中所有的文件列表|Y|
|fileType|七牛空间中文件类型，该参数为可选参数，指定后列举指定类型的文件，如果不指定则获取空间中所有的文件列表|Y|
|suffix|七牛空间中文件名的后缀，该参数为可选参数，指定后列举指定后缀的文件，如果不指定则获取空间中所有的文件列表|Y|
|fsize|七牛空间中文件大小，该参数为可选参数，指定后列举指定大小的文件，如果不指定则获取空间中所有的文件列表|Y|
|stype|七牛空间中文件的存储类型（0 表示标准存储；1 表示低频存储；2 表示归档存储），该参数为可选参数，如果不指定则获取空间中所有的文件列表|Y|

# 示例

1.获取空间`upload30`里面的所有文件列表：

```
qcommand listbucket upload30 upload_list.txt
```

2.获取空间`upload30`里面的以`2014/10/07/`为前缀的文件列表：

```
qcommand listbucket upload30 upload_list.txt --prefix=2014/10/07/
```

3.获取`upload30` 里面在 2021年5月1日 之后上传的文件列表：

```
qcommand listbucket upload30 upload_list.txt --start=1619798400
```

4.获取`upload30`里面 2021年5月1日 到  2021年5月31日 之间上传的文件列表
```
qcommand listbucket upload30 upload_list.txt --start=1619798400 --end=1622390400
```

5.获取`upload30`里面`image/jpeg;image/png`类型的文件列表
```
qcommand listbucket upload30 upload_list.txt --fileType=image/jpeg;image/png
```

6.获取`upload30`里面`.jpg;.png;.html`结尾的文件列表
```
qcommand listbucket upload30 upload_list.txt --suffix=.jpg;.png;.html
```

7.获取`upload30`里面文件大小为`0`的文件列表
```
qcommand listbucket upload30 upload_list.txt --fsize=0
```

8.获取`upload30`里面低频存储类型的文件列表
```
qcommand listbucket upload30 upload_list.txt --stype=1
```




