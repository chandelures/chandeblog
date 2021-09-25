Python 虽然提供了庞大的标准库(python standard library)，例如 os 提供了一些文件、目录的操作，sys 提供了和操作系统的交互，但是在一些项目下仅仅依赖这些标准库还是远远不够的。例如我们经常需要用于科学计算的 numpy，网络爬虫的 requests 以及 web 框架 Flask 等 python 库，都属于 python 第三方库。而这些第三方库则需要我们通过 python 官方提供的包管理工具 pip 来进行安装，因此学习 pip 的一些基本操作是很有必要的。

## 入门指南

在 python>=3.4 的版本中，python 在安装时已经自带了 pip 工具，我们可以通过以下命令来确认 pip 是否已经可以直接使用

```shell
$ pip --version # python version 3
$ pip3 --version # python version 3

pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)

```

如果还没有安装 pip 的话，则可以通过使用脚本来进行安装

```shell
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py # 获取get-pip.py
$ sudo python get-pip.py

```

或使用包管理器进行安装（Linux 环境下）

```shell
$ sudo apt install python3-pip # ubuntu/debian
$ sudo yum install python3-pip # centos

```

### 安装第三方包

例如，我们需要开发一个网络爬虫的项目时需要用到 requests，那么就需要先使用 pip 来安装 requests

```shell
$ pip install requests

```

然后我们可以通过在 python 命令行中 import requests 来判断是否安装成功

```shell
$ python
>>> import requests
>>>
```

如果安装成功的话，我们就可以在常规的 py 文件中引用 requests 了

```python
import requests

url = 'https://www.baidu.com'
res = requests.get(url)
print(res.text)
```

如果安装不成功的话可以通过在搜索引擎中查询相关错误信息来解决。

### 卸载第三方包

同时我们也可以通过 pip 来卸载一些我们用不到的包

```shell
$ pip uninstall requests
```

但是这种方法的缺点就是无法卸载 requests 的依赖包，

```shell
$ pip list # 列出pip安装的包
Package       Version
------------- ---------
certifi       2020.12.5
chardet       4.0.0
idna          2.10
pip           20.0.2
pkg-resources 0.0.0
requests      2.25.1
setuptools    44.0.0
urllib3       1.26.4

$ pip uninstall requests

$ pip list
Package       Version
------------- ---------
certifi       2020.12.5
chardet       4.0.0
idna          2.10
pip           20.0.2
pkg-resources 0.0.0
setuptools    44.0.0
urllib3       1.26.4
```

因此我们可以通过 pip-autoremove 来实现同时卸载这些依赖包

```shell
$ pip install pip-autoremove

$ pip list
Package        Version
-------------- ---------
certifi        2020.12.5
chardet        4.0.0
idna           2.10
pip            20.0.2
pip-autoremove 0.9.1
pkg-resources  0.0.0
requests       2.25.1
setuptools     44.0.0
urllib3        1.26.4

$ pip-autoremove requests

$ pip list
Package        Version
-------------- -------
pip            20.0.2
pip-autoremove 0.9.1
pkg-resources  0.0.0
setuptools     44.0.0
```

### 其他常用的 pip 命令

**显示帮助**

```shell
$ pip help

Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  check                       Verify installed packages have compatible dependencies.
  config                      Manage local and global configuration.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion.
  debug                       Show information useful for debugging.
  help                        Show help for commands.
```

**升级**

```shell
$ pip install --upgrade [package]
```

**搜索**

```shell
$ pip search [package]
```

**显示相关信息**

```shell
$ pip show [package]
```

## 使用 Requirements.txt

我们在进行项目开发时，通常需要记录我们所安装的第三方库作为依赖，我们可以通过 python freeze 来生成一个名为 requirements.txt 的文件来管理这些第三方库

```shell
$ pip freeze > requirements.txt
$ cat requirements.txt
certifi==2020.12.5
chardet==4.0.0
idna==2.10
pip-autoremove==0.9.1
requests==2.25.1
urllib3==1.26.4
```

freeze 命令生成了所有安装过的第三方库名称以及版本号,这样我们在其他环境下就可以通过 requirements.txt 来安装项目中的所有依赖了

```shell
$ pip install -r requirements.txt

```

通过 pip freeze 来生成的 requirements.txt 存在一个缺点就是其中包含了我们所需要安装库的依赖，如果我们不想要在项目中的 requirements.txt 中存在这些依赖项，则需要通过 pipreqs 来实现

```shell
$ pip install pipreqs
$ pipreqs . # 在项目根目录下运行

```

pipreqs 只会生成在项目中 import 过的包，因此如果项目中还含有一些没有通过 import 导入的包则需要手动添加到 requirements.txt 之中。

## 换源

如果在国内使用 pip 的默认源来安装第三方包的话，则可能会出现下载速度缓慢的情况。我们可以通过更换默认源为国内的镜像源来解决，例如我们将 pip 换为阿里的镜像源

```shell
$ pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

```

该命令将会在我们当前用户的家目录下创建一个 pip 配置文件用于更换镜像源

```shell
$ cat ~/.config/pip/pip.conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple

```

也可以通过在 pip 后面加参数临时改变源

```shell
$ pip install [package] -i https://mirrors.aliyun.com/pypi/simple

```
