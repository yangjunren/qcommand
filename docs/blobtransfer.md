# 简介

`blobtransfer` 指令用来获取跨区域同步流量统计数据。可查询当天计量，统计延迟大概 5 分钟。


# 格式
```
qcommand blobtransfer <begin> <end> <g> [--is_oversea= --taskid= ]
```

# 鉴权

需要在使用了`account`设置了`AccessKey`和`SecretKey`的情况下使用。

# 参数

|参数名|描述|
|-----|-----|
|begin|起始日期字符串，闭区间，例如： 20060102150405|
|end| 结束日期字符串，开区间，例如： 20060102150405|
|g|时间粒度，支持 day；当天支持5min、hour、day|
|is_oversea|是否为海外同步,0 国内,1 海外。可选参数，不填表示查询总跨区域同步流量.|
|taskid|任务 id。|


# 示例

查询 20210701 这天的跨区域同步流量
```
qcommand blobtransfer 20210701 20210702 day
```

