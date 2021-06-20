# 简介

`user`命令用来对本地数据库中存储的账户信息进行管理，可以切换当前账号， 列举本地保存的账号， 移除特定的账号。

# 格式

```
qcommand user <子命令>
``` 

# 帮助

```
qcommand user --help
```
如果想查看字命令的帮助信息，比如cu字命令， 可以使用`qcommand user cu --help`

# 字命令

user的字命令有：
* cu 切换当前的账户
* ls 列出所有本地的账户信息
* remove 移除特定用户

# 示例

1. 列举本地所有的账号信息

```
qcommand user ls
```

2. 切换到`test`账号

```
qcommand user cu test
```

3. 删除`test`账号

```
qcommand user remove test
```
