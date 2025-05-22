# 基于UR5的五子棋机器人

## 项目简介
本项目通过摄像头捕捉棋子位置与控制UR5机械臂机器人，完成与机械臂下棋的任务

## 安装使用步骤

### 1. 环境配置
- **操作系统**：Windows 10/11
- **Python环境**：建议使用Anaconda创建虚拟环境。
```bash
# 创建并激活虚拟环境
conda create -n ur5 pip python=3.9
conda activate ur5
```

### 2. 安装依赖包
- **opencv-python**：用于识别五子棋和棋盘。
- **pygame**：用于显示游戏页面。

```bash
# 安装Opencv
pip install opencv-python

# 安装pygame
pip install pygame
```

### 3. 运行项目
- 运行`获取新增棋子坐标.py`获得棋盘位置。
- 更改`最终代码.py`中棋盘位置参数。
- 运行`最终代码.py`选择你要使用的棋子颜色即可开始下棋。
```bash
# 运行程序
python 获取新增棋子坐标.py
python 最终代码.py
```
通过以上步骤，您可以成功运行该程序与UR5机械臂机器人下五子棋。
