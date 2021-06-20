# 简介

`bupload`命令用来批量上传本地文件。

# 格式
```
qcommand bupload <bucket> <dir> [--successfile= --failurefile= --threacount=]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|bucket|空间名称，可以为公开空间或者私有空间|
|dir| 需要上传的文件目录|
|successfile| 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的bupload目录下|
|fileurefile| 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的bupload目录下|
|threadcount| 并发数，可选参数，默认值为3|

# 示例

上传`/user/test/`目录下的文件到`upload30`空间。

```
qcommand bupload upload30 /user/test
```

