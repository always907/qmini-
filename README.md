这是改进版的Qmini代码文件包，操作教程见飞书文档https://xcnn12likzgr.feishu.cn/wiki/GeX9wWriSi5OnskR4LKct3Ffn0f，3
d打印的SolidWorks文件见其他分支





# RoboTamerSdk4Qmini_v1.0
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![C++](https://img.shields.io/badge/Code%20Language-C++-blue.svg) 
![ONNX](https://img.shields.io/badge/Framework-ONNX-orange.svg)
![Version](https://img.shields.io/badge/Version-1.0-blue.svg)  

**This is currently Version 1.0.**  
✅ Initial release complete.  
🚀 Future updates are planned to add new features and optimize performance.  
Stay tuned for changelogs!

This repository provides C++ deployment code for biped robot motion control, 
leveraging ONNX Runtime for high-performance model inference in real-world robotics systems. 
It enables seamless deployment of pre-trained reinforcement learning policies (exported 
as ONNX models from *.pt or *.pth models) onto Linux-based edge devices or robot hardware, 
ensuring low-latency, real-time control for robots like Unitree Qmini. The codebase includes 
optimized inference pipelines, hardware acceleration support (CPU/GPU), and Linux compatibility
for robotics applications.


**Maintainer**: Yanyun Chen, Tiyu Fang, Kaiwen Li, Kunqi Zhang, and Wei zhang<br>
**Affiliation**: Visual Sensing and Intelligent System Lab (VSISLab),
School of Control Science and Engineering,
Shandong University, China<br> 
**Website**: www.vsislab.com<br>
**Contact**: info@vsislab.com

### Features
- **High-Performance Inference** — Optimized C++ implementation with ONNX Runtime for low-latency, real-time policy execution on robots like Unitree Qmini.<br>
- **Hardware Acceleration** — Supports CPU/GPU backends (including CUDA) for maximum inference speed on Linux-based edge devices.<br>
- **Modular Architecture** — Easy-to-use API for integrating with custom robot hardware, sensors, and actuators.<br>
- **Safety-Critical Design** — Built-in emergency stop mechanisms, sensor validation, and fail-safe protocols for real-world operation.<br>
- **Real-Time Control** — Thread-safe implementation supporting hard real-time constraints.<br>
- **Documentation & Examples** — Step-by-step guides for robot deployment and custom hardware setups.<br>


## Code Structure
   ```
RoboTamerSdk4Qmini/
   ├── bin/                    # The pre-trained onnx model, the config file, and the executable files
   ├── include/                # Tne header files
   ├── lib/                    # Tne dependency libraries 
   ├── source/                 # The source files
   ├── thirdparty/             # The thirdparty files
   ├── CMakeLists.txt          # Configuration file for building the executable files
   └── README.md
   ```
### Notes
* Some params are hard-coded in _Motor_thread.hpp_, _run_interface.cpp_, and _test_interface.cpp_. Be careful about them.
* This repository is not maintained anymore. If you have any question, please send emails to info@vsislab.com.
* The project can only be run after successful installation.

## Installation
### Prerequisites
* [Ubuntu](https://cn.ubuntu.com/)(version 20.04 or higher)
* [Unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2)
* [unitree_actuator_sdk](https://github.com/unitreerobotics/unitree_actuator_sdk)
* [CMake](http://www.cmake.org) (version 2.8.3 or higher)
* [Yaml-cpp](https://github.com/jbeder/yaml-cpp) (version 0.6.0 or higher)
* [Eigen](https://gitlab.com/libeigen/eigen/-/releases) (version 3.3.7 or higher)
* [OnnxRuntime](https://onnxruntime.ai/docs/install/) (version 1.17.1 or higher)
* [JsonCpp](https://github.com/open-source-parsers/jsoncpp)
* [Python3](version 3.8.12 or higher)
* [pygame](https://pypi.org/project/pygame/)(version 2.6.1 or higher)

### Steps
1. Install cmake:

```bash
sudo apt-get install cmake
```

2. Install yaml-cpp/eigen:

```bash
cd yaml-cpp-xxx/eigen-x.x.x
mkdir build
cd build
cmake ..
make
sudo make install
```

3. Install OnnxRuntime (copy libonnxruntime.so libonnxruntime.so.1.17.1 to /usr/lib or /usr/local/lib)
```bash
sudo cp -r libonnxruntime.so libonnxruntime.so.1.17.1 /usr/lib
or
sudo cp -r libonnxruntime.so libonnxruntime.so.1.17.1 /usr/local/lib
sudo cp libUnitreeMotorSDK_Linux64.so /usr/local/lib/ /usr/lib/
or
sudo cp libUnitreeMotorSDK_arm64.so /usr/local/lib/ /usr/lib/
```


## Full steps of operating RoboTamerSdk4Qmini on the real Qmini robot
#### Before start
```bash
cmake -DPLATFORM=arm64 .. && make && cd bin
```
#### Step 1: Check the start-up posture of the robot
#### Step 2: Boot up both the joy stick and the robot
#### Step 3: Run the executable file 
```bash
$ ./run_interface
or sudo ./run_interface
```
#### Step 4: Check the initial state of the robot
#### Step 5: Enter 1 and press enter into ready mode.
#### Step 6: Enter 2 and press enter into position stand mode.
#### Step 7: Enter 3 and press enter into AI stand control mode. Now enjoy your robot!


## Contributing

We welcome contributions from the community! Please contact us at info@vsislab.com before submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License —— see the [LICENSE] file —— for details.

## Citation

If you use this code in your research, please cite our work:
```
@article{Chen2025GALA,
  author={Yanyun Chen, Ran Song, Jiapeng Sheng, Xing Fang, Wenhao Tan, Wei Zhang and Yibin Li},
  journal={IEEE Transactions on Automation Science and Engineering}, 
  title={A Generalist Agent Learning Architecture for Versatile Quadruped Locomotion}, 
  year={2025},
  keywords={Quadruped Robots, Versatile Locomotion, Deep Reinforcement Learning, A Single Policy Network, Multiple Critic Networks}
}

@article{Sheng2022BioInspiredRL,
  title={Bio-Inspired Rhythmic Locomotion for Quadruped Robots},
  author={Jiapeng Sheng and Yanyun Chen and Xing Fang and Wei Zhang and Ran Song and Yuan-hua Zheng and Yibin Li},
  journal={IEEE Robotics and Automation Letters},
  year={2022},
  volume={7},
  pages={6782-6789}
}

@article{Liu2024MCLER,
  author={Liu, Maoqi and Chen, Yanyun and Song, Ran and Qian, Longyue and Fang, Xing and Tan, Wenhao and Li, Yibin and Zhang, Wei},
  journal={IEEE Robotics and Automation Letters}, 
  title={MCLER: Multi-Critic Continual Learning With Experience Replay for Quadruped Gait Generation}, 
  year={2024},
  volume={9},
  number={9},
  pages={8138-8145},
  keywords={Quadrupedal robots;Task analysis;Continuing education;Optimization;Legged locomotion;Training;Motors;Continual learning;legged robots},
  doi={10.1109/LRA.2024.3418310}
}

```
