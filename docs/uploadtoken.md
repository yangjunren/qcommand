# 简介

`uploadtoken`是用来计算 Upload Token 的命令。

# 格式

```
qshell uploadtoken <bucket> [--key= --expires=]
```

# 参数

|参数名|描述|
|-----|-----|
|bucket|空间名|
|key| 文件名，可选参数，默认为None|
|expires| 过期时间，可选参数，默认是3600s|

# 示例

生成`upload30`空间的上传token，有效期1小时。
```
qcommand uploadtoken upload30
```

