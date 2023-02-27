从mac换到windows，苦于没有`alias`给命令取别名，只好自己简单开发一个了。

## 安装

`pip install -U python-alias`

## 使用

`palias --help`查看支持的命令

主要命令使用如下：

- 添加别名：`palias add gs git status`表示`gs`为命令`git status`的别名

- 别名列表：`palias list`

- 执行命令: 直接终端输入`gs`，代表执行`git status`命令

- 删除别名：`palias del --name gs`





