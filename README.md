<div align="center">

# Qmini 双足机器人改进版

**基于宇树 Qmini 的开源双足机器人改进项目 —— 涵盖强化学习运动控制、3D 打印结构、URDF 模型与实时语音交互**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Robot](https://img.shields.io/badge/Robot-Unitree%20Qmini-orange.svg)
![DOF](https://img.shields.io/badge/DOF-10%20(2%C3%975)-green.svg)
![RL](https://img.shields.io/badge/Control-Reinforcement%20Learning-purple.svg)
![ONNX](https://img.shields.io/badge/Inference-ONNX%20Runtime-lightgrey.svg)

[功能特性](#-功能特性) · [硬件结构](#-硬件结构) · [模块总览](#-模块总览) · [快速开始](#-快速开始) · [文档](#-文档与教程)

</div>

---

## 📖 项目简介

本项目是在宇树（Unitree）**Qmini** 双足机器人基础上的开源改进版本，目标是提供一套**从仿真训练到实机部署**的完整工具链。项目整合了强化学习运动控制、3D 打印机械结构、机器人 URDF 模型以及基于大模型的实时语音交互模块，便于学习者与开发者快速复现并二次开发。

> 💡 完整的图文操作教程请见 [飞书云文档](https://xcnn12likzgr.feishu.cn/wiki/GeX9wWriSi5OnskR4LKct3Ffn0f)，建议结合本说明一起阅读。

---

## ✨ 功能特性

- **强化学习运动控制** —— 采用 Isaac Gym 训练步态策略，导出为 ONNX 模型后在实机上低延迟推理。
- **完整 3D 打印结构** —— 提供 SolidWorks/STEP 源文件，可直接导入切片软件打印整机零件。
- **标准 URDF 模型** —— 含双腿各 5 个关节的运动学描述与网格文件，可用于仿真与可视化。
- **实时语音交互** —— 基于 ROS 2 与火山引擎实时语音大模型，实现语音唤醒与对话控制。
- **从仿真到实机** —— 训练、部署、硬件、交互各模块解耦，可单独使用也可组合成完整系统。

---

## 🦿 硬件结构

Qmini 为 **10 自由度**双足机器人，左右腿（`LL` / `RL`）结构对称，每条腿包含 5 个旋转关节：

| 关节 | 名称 | 说明 |
| :--- | :--- | :--- |
| Joint 1 | `hip_yaw` | 髋关节偏航 |
| Joint 2 | `hip_roll` | 髋关节横滚 |
| Joint 3 | `hip_pitch` | 髋关节俯仰 |
| Joint 4 | `knee` | 膝关节 |
| Joint 5 | `ankle` | 踝关节 |

机器人本体的运动学描述与网格文件见 [`urdf.zip`](urdf.zip)（`Qmini.urdf` + `meshes/*.STL`）。

---

## 🧩 模块总览

| 模块 | 资源位置 | 说明 |
| :--- | :--- | :--- |
| 🤖 强化学习与实机部署 | [`master` 分支](../../tree/master) | C++ + ONNX Runtime 部署代码（RoboTamerSdk4Qmini），含预训练 `policy.onnx`、IMU/手柄接口。 |
| 🖨️ 3D 打印结构 | [`Qmini3.0.zip`](Qmini3.0.zip) | 整机 `Qmini3.0.STEP` 模型，使用 SolidWorks 打开后导入切片/打印机即可。 |
| 🎙️ 实时语音模块 | [`realtime_dialogue.zip`](realtime_dialogue.zip) | 基于 ROS 2（rclpy）与火山引擎实时语音大模型的对话程序。 |
| 🦿 URDF 硬件模型 | [`urdf.zip`](urdf.zip) | 机器人 URDF 与 STL 网格，用于仿真与可视化。 |
| 📚 文档手册 | [飞书云文档](https://xcnn12likzgr.feishu.cn/wiki/GeX9wWriSi5OnskR4LKct3Ffn0f) | 详细的环境搭建、训练与部署图文教程。 |

---

## 🚀 快速开始

### 1. 获取代码

```bash
git clone https://github.com/always907/qmini-.git
cd qmini-
```

### 2. 强化学习与实机部署

部署代码位于 `master` 分支（`RoboTamerSdk4Qmini`），请切换分支后按其 README 操作：

```bash
git checkout master
```

> 依赖 Ubuntu 20.04+、CMake、Eigen、yaml-cpp、ONNX Runtime 1.17.1+ 以及 Unitree SDK。
> 训练所需的强化学习文件包与配套教程见 [飞书云文档](https://xcnn12likzgr.feishu.cn/wiki/GeX9wWriSi5OnskR4LKct3Ffn0f)。

### 3. 3D 打印结构

解压 [`Qmini3.0.zip`](Qmini3.0.zip)，使用 SolidWorks 打开 `Qmini3.0.STEP`，导入切片软件或打印机即可打印整机零件。

### 4. 实时语音模块

```bash
# 解压语音模块
unzip realtime_dialogue.zip && cd realtime_dialogue

# 在 config.py 中填入火山引擎控制台的 App ID 与 Access Key
# 安装依赖后通过麦克风启动对话
pip install -r requirements.txt
python main.py --format=pcm
```

详细配置（发音人选择、音频文件输入等）见 `realtime_dialogue/README.md`。

---

## 📂 仓库结构

```text
qmini-/
├── Qmini3.0.zip              # 3D 打印整机 STEP 模型（SolidWorks）
├── realtime_dialogue.zip     # ROS 2 实时语音交互模块
├── urdf.zip                  # 机器人 URDF 与 STL 网格
├── Qmini_DIY-改.docx          # DIY 改装说明文档
├── Qmini拆日.docx             # 拆装/装配说明文档
└── README.md                 # 项目说明（本文件）

# master 分支：RoboTamerSdk4Qmini —— 强化学习实机部署 C++ 代码
```

---

## 📚 文档与教程

- **图文操作手册（强烈推荐）**：[飞书云文档](https://xcnn12likzgr.feishu.cn/wiki/GeX9wWriSi5OnskR4LKct3Ffn0f)
- **实机部署 SDK 说明**：见 [`master` 分支](../../tree/master) 的 `README.md`
- **语音模块说明**：见 `realtime_dialogue.zip` 内的 `README.md`

---

## 🙏 致谢

- 机器人本体基于宇树科技（[Unitree Robotics](https://www.unitree.com/)）Qmini 平台。
- 实机部署 SDK（RoboTamerSdk4Qmini）源自山东大学视觉感知与智能系统实验室（[VSISLab](http://www.vsislab.com/)）。
- 实时语音能力基于火山引擎实时语音大模型。

感谢以上团队的开源工作。

---

## 📄 许可证

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源，详见各分支中的 `LICENSE` 文件。
