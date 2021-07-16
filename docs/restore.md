# 简介

`restore`命令用来解冻单个归档文件。

# 格式
```
qcommand restore <bucket> <key> <days>
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|bucket|归档文件所在空间|
|inputfile| 需要解冻的文件名|
|days| 解冻时长，单位天，范围 1-7|

# 示例

解冻`upload30`空间中的归档文件`test.jpg`，解冻有效期7天。

```
qcommand restore upload30 test.jpg 7
```

