# 简介

`bm3u8` 指令用来批量下载空间中的m3u8文件。


# 格式
```
qcommand bm3u8 <domain> <inputfile> <savedir> [--referer= --private= --successfile= --failurefile= --threacount=]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|domain|空间绑定的域名，可以为公开空间或者私有空间|
|inputfile| 包含m3u8文件名的txt文件|
|savedir| 文件保存路径|
|referer| referer参数，domain域名开启referer白名单的情况下设置，设置一个白名单中的域名即可|
|private| 空间属性，bool类型，默认为False（公开空间），私有空间的话置为True|
|successfile| 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bm3u8download 目录下|
|fileurefile| 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bm3u8download 目录下|
|threadcount| 并发数，可选参数，默认值为3|

# 示例

`inputfile.txt` 文件内容示例： 

```
123.m3u8
qiniu.m3u8
test.m3u8
```

下载`upload30`空间中`inputfile.txt`中的文件，并保存在 ./download 目录下。

```
qcommand bm3u8 test.qiniu.com inputfile.txt ./download
```

