# qcommand

## 简介
qcommand 工具使用python3实现的一个方便使用七牛API服务的命令行工具。目前该工具融合了七牛对象存储和一些常用的便捷命令。

## 下载
| 支持平台                 | 链接                                                                                               |
| ----------------------- | -------------------------------------------------------------------------------------------------|
| Mac OS                  | [下载](https://github.com/yangjunren/qcommand/blob/main/releases/v0.0/mac_os/qcommand)      |


**其他平台支持版本后续会逐步更新**


## 安装

qcommand是命令行工具，所以下载之后即可使用。


**Linux和Mac平台**

（1）权限
如果在Linux或者Mac系统上遇到`Permission Denied`的错误，请使用命令`chmod +x qcommand`来为文件添加可执行权限。这里的`qcommand`是上面文件重命名之后的简写。

（2）任何位置运行
对于Linux或者Mac，如果希望能够在任何位置都可以执行，那么可以把`qcommand`所在的目录加入到环境变量`$PATH`中去。假设`qcommand`命令被解压到路径`/home/jemy/tools`目录下面，那么我们可以把如下的命令写入到你所使用的bash所对应的配置文件中，如果是`/bin/bash`，那么就是`~/.bashrc`文件，如果是`/bin/zsh`，那么就是`~/.zshrc`文件中。写入的内容为：

```
export PATH=$PATH:/home/jemy/tools
```
保存完毕之后，可以通过两种方式立即生效，其一为输入`source ~/.zshrc`或者`source ~/.bashrc`来使配置立即生效，或者完全关闭命令行，然后重新打开一个即可，接下来就可以在任何位置使用`qcommand`命令了。

**Windows平台**

（1）闪退问题
本工具是一个命令行工具，在Windows下面请先打开命令行终端，然后输入工具名称执行，不要双击打开，否则会出现闪退现象。

（2）任何位置运行
如果你希望可以在任意目录下使用`qcommand`，请将`qcommand`工具可执行文件所在目录添加到系统的环境变量中。由于Windows系统是图形界面，所以方便一点。假设`qcommand.exe`命令被解压到路径`E:\jemy\tools`目录下面，那么我们把这个目录放到系统的环境变量`PATH`里面。

![windows-qcommand-path-settings.png](https://dn-odum9helk.qbox.me/FrJbSsVTFtZyFcEPKhVMYLfsSd9e)

## qcommand使用

1. 添加密钥和账户名称

该工具有两类命令，一类需要鉴权，另一类不需要。

需要鉴权的命令都需要依赖七牛账号下的 `AccessKey`, `SecretKey`和 `name`。所以这类命令运行之前，需要使用 `account` 命令来添加 `AccessKey` ，`SecretKey`和`Name` 。
`name`是用户可以自定义的字符串，用来唯一表示AccessKey/SecretKey账户，可以使用自命令`user`进行切换，切换账户的时候，需要使用账户唯一标识`name`。

```
qcommand account <name> <ak> <sk>
```

可以连续使用qaommand account 添加账号ak, sk, name信息，qcommand会保存这些账号的信息。


2. 添加完账户后，就可以使用qcommand进行相关操作了。

## 用户管理

使用qcommand user子命令可以用来管理记录的多账户信息。
1. qcommand user ls 列举所有的用户信息
2. qcommand user cu <name> 可以用来切换账户
3. qcommand user remove <name> 删除对应账户信息

<name>是使用qcommand account <name> <ak> <sk> 记录的时候的<name>名字，这个名字可以任意指定。

## 命令列表
| 命令        | 类别   | 描述                                                                    | 详细                         |
| ----------- | ------  | -------------------------------------------------------------------- | --------------------------- |
| account     | 账号     | 设置或显示当前用户的`accessKey`和`secretKey`                             | [文档](docs/account.md)      |
| user        | 账户管理 | 管理qcommand登录的七牛账号                                               | [文档](docs/user.md)         |
| listbucket  | 列举   | 列举七牛空间里面的所有文件                                                  | [文档](docs/listbucket.md)   |
| bdelete     | 删除   | 批量删除七牛空间中的文件                                                    | [文档](docs/bdelete.md)      |
| bmodtype    | 修改   | 批量批量修改空间中的文件 **存储类型**                                        | [文档](docs/bmodtype.md)     |
| bchstatus   | 修改   | 批量修改文件状态（0表示启用，1表示禁用）                                      | [文档](docs/bchstatus.md)    |
| bupload     | 上传   | 批量上传本地文件                                                          | [文档](docs/bupload.md)      |
| bdownload   | 下载   | 批量下载空间文件                                                          | [文档](docs/bdownload.md)    |
| bm3u8       | 下载   | 批量下载m3u8文件及其ts文件                                                 | [文档](docs/bm3u8.md)        |
| bcdnlog     | 下载   | 批量下载CDN日志                                                           | [文档](docs/bcdnlog.md)      |

## 其他命令
| 命令         | 描述                                                                     | 详细                         |
| ----------- | --------------------------------------------------------------------     | --------------------------- |
| ts2d | 时间戳转日期，转换后的进度秒级                                                       | [文档](docs/ts2d.md)         |
| uploadtoken   | 上传token，仅支持指定bucket、key（可选参数）、有效期（可选参数，默认为3600s）    | [文档](docs/uploadtoken.md)  |
| version   | 查看qcommand工具版本号                                                       | [文档](docs/version.md)      |

## 问题反馈

如果您有任何问题，请写在[ISSUE列表](https://github.com/yangjunren/qcommand/issues)里面，我们会尽快回复您。
