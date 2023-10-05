# [English](README_EN.md)
# perf-orange-cat
## 客户端性能测试平台

![微信图片_20230624120931](https://github.com/1033866383/perf-orange-cat/assets/56209295/ce1d47eb-01bb-41d8-88d4-e07828aea825)

**演示地址：** [http://112.126.75.188/](http://112.126.75.188/)

**源码地址：** [https://github.com/1033866383/perf-orange-cat](https://github.com/1033866383/perf-orange-cat)

**免安装二进制包：** [https://github.com/1033866383/perf-orange-cat/releases](https://github.com/1033866383/perf-orange-cat/releases)

**安装：** `pip install -U performancetest`

**启动：** `python -m performancetest.web.main`

启动后访问：[http://localhost/](http://localhost/) 即可开始Android/IOS性能测试

**API文档访问：** [http://localhost/redoc/](http://localhost/redoc/)

**环境要求：** python3.9+，如果Python版本有问题可以考虑使用 [pyenv](https://github.com/pyenv/pyenv) 进行环境隔离。

请注意本项目的开源协议。

**计划功能：**
- 增加对Windows、macOS、Linux等PC平台上应用的性能测试支持。
- 增加性能测试任务的对比功能。
- 添加标签功能，用于选择性能测试场景。
- 开发分支：dev

## 简介
- 替代perfdog等客户端性能测试工具。
- 支持Android/IOS平台上应用的性能数据测试，包括游戏和视频类应用。
- 支持多种性能指标，包括CPU、内存、FPS、GPU、温度、电量、流量等。
- 提供详细的CPU性能数据，包括Top版CPU、Procstat版应用CPU和Procstat版系统CPU。
- 在FPS指标中包括卡顿（jank）、强卡顿（big jank）等指标。
- 提供准确的性能数据，与perfdog一致。
- 可以实时记录设备画面，并支持点击跳转到对应的场景。
- 支持局域网内使用，允许在整个局域网上进行性能测试。
- 提供可执行文件，方便部署，同时提供API详情。

## 目录介绍
- `performancetest/web/test_result/`：包含前端页面和测试结果。
- `log.log`：项目运行日志。
- `task.sqlite`：SQLite数据库，包含每个任务的基本详情，也是唯一的DAO对象。

## 2023.8.10 新功能
**Android 多类型CPU，流量新功能演示：**

![微信图片_20230810000255](https://github.com/1033866383/perf-orange-cat/assets/56209295/da98d4bc-9784-4e75-8a3c-a8b9e94d02bd)
![微信图片_20230810000359](https://github.com/1033866383/perf-orange-cat/assets/56209295/bb88db4f-2013-4937-b1f2-cd1510adc9d1)

## 使用教程
建议使用以下步骤安装和启动 Perf-Orange-Cat：

1. 安装 Perf-Orange-Cat：`pip install -U performancetest`

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/b0d566fd-cf1e-4fd2-85eb-21f1e3762619)

2. 启动 Perf-Orange-Cat：`python -m performancetest.web.main`，此时项目已经启动了。

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/38f32ab0-a967-4cc4-963a-e57320e9da11)

3. 访问 [http://localhost/](http://localhost/)。

默认页面：

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/6b7d1e37-d488-4dda-b8b3-4e89890edf3f)

4. 点击上方红色按钮，创建新的性能测试任务。此时会开始自动检测你电脑上连接到Android/Ios设备。
   **需要注意的点：**
   - Android设备需要打开开发者模式，部分设备可能需要选择传输模式为传输文件！
   - IOS设备IOS系统16版本以上需要在设备上打开开发者选择，在隐私与安全中如下图。设备上如果看不到这个选项可用下载icarefone打开开发者模式。IOS16版本以下的需要连接xcode打开开发者选项。实际上连接一下选中手机就可以了。IOS16也可用通过此操作让开发者选项展示出来，如果是windows电脑连接IOS设备还需要记得安装iTunes。

![微信图片_20230625011358](https://github.com/1033866383/perf-orange-cat/assets/56209295/78d05b9e-7370-486c-b8cd-3ad0afaf5744)

下面是手机打开开发者选项后检测到的一个Android的模拟器和我自己的iphone手机实例：

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/78634fab-7225-4226-bca1-fdd4884abaec)

5. 点击手机图标选中手机后，下拉选中应用，选中后会自动展示版本号，随后点击创建任务。

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/ffbb3ef7-0623-44fd-97a2-f9e17135173b)

6. 点击完创建任务后页面会自动刷新，并开始性能测试，如果打开实时显示屏幕按钮，则上方的图片会实时展示手机屏幕的情况。左侧的是时间按钮是此任务的开始时间也代表此任务的名称，IOS的fps下方的卡顿，强卡顿并不会计算，Android则会真实计算，计算方式与perfdog一致。

![微信图片_20230810000513](https://github.com/1033866383/perf-orange-cat/assets/56209295/6021212f-d68c-431c-b4a0-50ec464f951e)
![微信图片_20230810000547](https://github.com/1033866383/perf-orange-cat/assets/56209295/b7a33e0e-7a9f-42d5-9dd7-571684ba428d)

7. 最后点击停止任务，任务即可停止，任务停止之后可用删除任务，删除任务是物理删除会把所有的任务数据删除，请谨慎操作。

![image](https://github.com/1033866383/perf-orange-cat/assets/56209295/a2f65fca-2256-4fac-a1a3-79fb8899ea0f)

IOS性能测试使用的是 [tidevice工具](https://github.com/alibaba/taobao-iphone-device)。

8. Android 多类型CPU，流量新功能演示：

![微信图片_20230810000255](https://github.com/1033866383/perf-orange-cat/assets/56209295/da98d4bc-9784-4e75-8a3c-a8b9e94d02bd)
![微信图片_20230810000359](https://github.com/1033866383/perf-orange-cat/assets/56209295/bb88db4f-2013-4937-b1f2-cd1510adc9d1)

## 风险提示
本软件使用了 GNU General Public License（GPL）开源许可证。大致理解如下：
- 自由使用：任何人可以免费使用被许可软件，无论是个人用户还是组织机构。
- 源代码访问：对于分发基于GPL v3.0许可的软件的人来说，必须提供源代码或者方便获取源代码的方式。这意味着用户可以查看、修改和适应软件以满足他们的需求。
- 修改的自由：任何人都可以对基于GPL v3.0许可的软件进行修改，并将修改后的版本再次发布。这确保了用户可以根据自己的需求对软件进行定制和改进。
- 再分发条件：如果你在基于GPL v3.0许可的软件上进行修改并分发，你必须将你的修改版本同样基于GPL v3.0许可协议进行分发。这样做可以确保修改的代码也对其他人开放，从而促进软件的共同发展。
- 公开许可证：任何附带基于GPL v3.0许可的软件的分发，都必须提供GPL v3.0许可协议的副本。这样其他人可以了解他们的权利和责任。
