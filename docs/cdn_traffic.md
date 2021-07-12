# 简介

`cdn_traffic` 指令用来获取CDN回源流量统计。可查询当天计量，统计延迟大概 5 分钟。


# 格式
```
qcommand cdn_traffic <begin> <end> <g> [--new_bucket= --domain= --ftype= --new_region= ]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|begin|起始日期字符串，闭区间，例如： 20060102150405|
|end| 结束日期字符串，开区间，例如： 20060102150405|
|g|时间粒度，支持 day；当天支持5min、hour、day|
|new_bucket|存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。|
|domain|空间访问域名。可选参数|
|ftype|存储类型，0 标准存储，1 低频存储，2 归档存储。可选参数，不指定默认获取所有|
|new_region|存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。|

# 示例

查询 20210701 这天的CDN回源流量
```
qcommand cdn_traffic 20210701 20210702 day
```

