# 简介

`brestore`命令用来批量解冻归档文件。

# 格式
```
qcommand brestore <bucket> <inputfile> [--days= --resfile= ]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|bucket|归档文件所在空间|
|inputfile| 包含归档文件名的 txt文件|
|days| 解冻时长，单位天，范围 1-7，可选参数，默认解冻时长为7天。|
|resfile| 处理结果保存文件路径，可选参数。默认保存在qcommand运行目录，文件名为 resfile_{bucket}.txt。|

# 示例

批量解冻`upload30`空间`./test.txt`中包含的归档文件，解冻有效期7天。

```
qcommand brestore upload30 ./test.txt
```

