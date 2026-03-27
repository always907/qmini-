# RoboTamerSdk4Qmini 项目分析文档

## 项目概述

RoboTamerSdk4Qmini 是一个用于双足机器人运动控制的 C++ 部署代码库，专门为 Unitree Qmini 机器人设计。该项目利用 ONNX Runtime 进行高性能模型推理，将预训练的强化学习策略（从 *.pt 或 *.pth 模型导出为 ONNX 格式）部署到基于 Linux 的边缘设备或机器人硬件上，实现低延迟、实时的机器人控制。

**核心特点：**
- 高性能 C++ 实现，支持 CPU/GPU 后端（包括 CUDA）
- 模块化架构，易于集成自定义机器人硬件、传感器和执行器
- 安全关键设计，内置紧急停止机制、传感器验证和故障安全协议
- 实时控制，支持硬实时约束的线程安全实现
- 完整的机器人控制栈，包括 IMU 处理、操纵杆控制、模式切换等

## 项目类型

这是一个 **C++ 机器人控制软件项目**，基于 CMake 构建系统，专门用于机器人硬件控制。

## 技术栈

- **编程语言**: C++17
- **构建系统**: CMake (3.5+)
- **推理框架**: ONNX Runtime (1.17.1+)
- **机器人SDK**: Unitree SDK2, unitree_actuator_sdk
- **配置文件**: YAML (yaml-cpp)
- **数学库**: Eigen3
- **JSON处理**: JsonCpp
- **Python集成**: Python3 (用于部分脚本)
- **DDS通信**: 用于机器人内部通信
- **多线程**: 自定义线程管理

## 代码结构

```
RoboTamerSdk4Qmini/
├── bin/                    # 预训练模型、配置文件和可执行文件
│   ├── config.yaml        # 主要配置文件
│   ├── policy.onnx        # ONNX 模型文件
│   ├── run_interface      # 主可执行文件
│   ├── test_interface     # 测试可执行文件
│   └── *.py               # Python 辅助脚本
├── include/                # 头文件
│   ├── user/              # 用户自定义头文件
│   │   ├── custom.hpp     # 主控制类 G1 定义
│   │   ├── rl_controller.h # RL 控制器类
│   │   └── ...            # 其他控制模块
│   ├── unitree/           # Unitree SDK 头文件
│   ├── onnx/              # ONNX Runtime 头文件
│   └── utils/             # 工具函数
├── source/                 # 源文件
│   ├── run_interface.cpp  # 主程序入口
│   ├── test_interface.cpp # 测试程序
│   └── user/              # 用户自定义实现
│       ├── custom.cpp     # G1 类实现
│       └── rl_controller.cpp # RL 控制器实现
├── lib/                    # 依赖库
│   ├── aarch64/           # ARM64 架构库
│   ├── x86_64/            # x86_64 架构库
│   └── onnx/              # ONNX Runtime 库
├── thirdparty/            # 第三方依赖
└── unitree_actuator_sdk-all/ # Unitree 执行器 SDK
```

## 构建和运行

### 构建项目

项目使用 CMake 构建系统，支持 ARM64 和 x86_64 架构：

```bash
# 在项目根目录下
mkdir -p build && cd build

# 根据目标平台选择
cmake -DPLATFORM=arm64 ..  # 用于 ARM64 平台（如机器人）
# 或
cmake -DPLATFORM=x86_64 .. # 用于 x86_64 平台

make
```

构建完成后，可执行文件将生成在 `bin/` 目录下。

### 运行项目

在真实 Qmini 机器人上运行的完整步骤：

1. **检查机器人启动姿势**
2. **启动操纵杆和机器人**
3. **运行可执行文件**：
   ```bash
   cd bin
   ./run_interface
   # 或使用 sudo（如果需要权限）
   sudo ./run_interface
   ```
4. **检查机器人初始状态**
5. **模式切换**：
   - 输入 `1` + Enter：进入准备模式
   - 输入 `2` + Enter：进入位置站立模式
   - 输入 `3` + Enter：进入 AI 站立控制模式

### 依赖安装

项目依赖多个第三方库，需要在构建前安装：

1. **基础依赖**：
   ```bash
   sudo apt-get install cmake libeigen3-dev libyaml-cpp-dev libjsoncpp-dev python3-dev
   ```

2. **ONNX Runtime**：
   - 下载适合平台的 ONNX Runtime 库
   - 将 `libonnxruntime.so` 和 `libonnxruntime.so.1.17.1` 复制到 `/usr/lib` 或 `/usr/local/lib`

3. **Unitree SDK**：
   - 需要安装 Unitree SDK2 和 unitree_actuator_sdk
   - 将相应的 motor SDK 库复制到系统库目录

## 开发约定

### 代码风格

1. **命名约定**：
   - 类名使用 PascalCase（如 `RLController`, `G1`）
   - 变量和函数名使用 snake_case（如 `joint_pos`, `rl_control()`）
   - 常量使用 UPPER_SNAKE_CASE

2. **文件组织**：
   - 头文件在 `include/` 目录，按功能模块组织
   - 源文件在 `source/` 目录，与头文件对应
   - 配置文件在 `bin/` 目录

3. **多线程设计**：
   - 使用自定义的线程管理类
   - 不同控制循环运行在不同频率的线程中
   - 线程间通过数据缓冲区（DataBuffer）通信

### 控制架构

项目采用分层控制架构：

1. **顶层控制**（`G1` 类）：
   - 管理所有子系统（IMU、操纵杆、电机、模式切换）
   - 协调不同控制线程
   - 处理模式切换和状态机

2. **RL 控制器**（`RLController` 类）：
   - 执行 ONNX 模型推理
   - 计算关节位置增量
   - 处理观察空间和动作空间

3. **底层通信**：
   - 通过 DDS 与机器人硬件通信
   - 电机命令和状态传输
   - IMU 数据读取

### 配置管理

- 主要配置在 `bin/config.yaml` 中
- 包含观察/动作空间维度、控制参数、关节限制等
- 支持软控制和硬控制的不同刚度/阻尼参数

## 测试和验证

### 测试模式

项目支持多种测试模式：

1. **正弦测试**：关节正弦运动测试
2. **模拟步态测试**：从文件读取步态数据
3. **本地测试模式**：不连接真实硬件的测试

### 数据报告

内置数据报告系统，可实时报告：
- 关节位置和速度
- 机器人姿态（RPY）
- 控制命令
- 系统状态

## 注意事项

1. **硬件依赖**：
   - 项目专为 Unitree Qmini 机器人设计
   - 需要特定的网络接口（默认 `wlan0`）
   - 依赖 Unitree 专有 SDK 和硬件

2. **硬编码参数**：
   - 部分参数在 `Motor_thread.hpp`、`run_interface.cpp` 和 `test_interface.cpp` 中硬编码
   - 修改时需要特别注意

3. **实时性要求**：
   - 控制循环有严格的定时要求
   - 线程优先级和调度需要优化

4. **安全考虑**：
   - 包含紧急停止机制
   - 建议在受控环境中测试
   - 遵循机器人安全操作规范

## 维护状态

- **当前版本**：1.0（初始发布完成）
- **维护状态**：不再积极维护（如有问题请联系 info@vsislab.com）
- **未来计划**：计划添加新功能和性能优化

## 联系信息

- **维护团队**：Visual Sensing and Intelligent System Lab (VSISLab)
- **所属机构**：山东大学控制科学与工程学院
- **网站**：www.vsislab.com
- **邮箱**：info@vsislab.com

---

*本文档基于代码分析生成，适用于后续 AI 助手理解项目上下文和提供开发协助。*
