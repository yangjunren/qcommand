# 简介

`bcdnlog` 指令用来批量下载CDN 域名的访问日志。


# 格式
```
qcommand bcdnlog <date> <domains> <savedir> [--successfile= --failurefile= --threacount=]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|date|日期，例如 2016-07-01|
|domains| 域名，多个域名用;分割，示例 123.qiniu.com;345.test.com |
|savedir| 文件保存路径|
|successfile| 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bcdnlogdownload 目录下|
|fileurefile| 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bcdnlogdownload 目录下|
|threadcount| 并发数，可选参数，默认值为3|

# 示例

下载`123.qiniu.com;345.test.com`2个域名`2016-07-01`的访问日志，并保存在 ./cdn_download 目录下。

```
qcommand bcdnlog 2016-07-01 123.qiniu.com;345.test.com ./cdn_download
```

