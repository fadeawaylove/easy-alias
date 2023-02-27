从mac换到windows，苦于没有`alias`给命令取别名，只好自己简单开发一个了。

## 安装

`python setup install`

## 使用

下面以`git status`命令为例

### 测试命令别名

执行：`pp test git status`

### 添加命令别名

执行：`pp add gs git status`

### 命令别名列表

执行：`pp list`

### 通过别名执行命令

执行：`ppe gs`

### 删除当个命令别名

执行：`pp del -n gs`

### 删除所有命令别名

执行：`pp del -a true`




