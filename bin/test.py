#!/usr/bin/env python3
import serial
import struct
import time
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

def smart_frame_detection():
    print("=== 智能帧同步检测 ===")
    print("波特率: 115200")
    
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=2
        )
        print("✓ 串口打开成功")
    except Exception as e:
        print(f"✗ 串口打开失败: {e}")
        return

    print("\n搜索有效的帧结构... (按 Ctrl+C 停止)")
    print("-" * 50)
    
    # 收集数据样本进行分析
    buffer = bytearray()
    start_time = time.time()
    
    try:
        while time.time() - start_time < 10:  # 收集10秒数据
            data = ser.read(ser.in_waiting or 1)
            if data:
                buffer.extend(data)
                if len(buffer) > 1000:  # 收集足够数据后分析
                    break
        
        print(f"收集了 {len(buffer)} 字节数据")
        
        # 分析数据模式
        print("\n=== 数据分析 ===")
        
        # 1. 查找所有可能的帧头位置
        fc_positions = []
        for i in range(len(buffer) - 2):
            if buffer[i] == 0xfc:
                fc_positions.append(i)
        
        print(f"找到 {len(fc_positions)} 个 0xfc 字节")
        
        if not fc_positions:
            print("❌ 未找到帧头 0xfc")
            return
        
        # 2. 分析每个帧头后的数据模式
        valid_frames = []
        known_types = [0x40, 0x41, 0x42, 0x5c, 0x50]  # 已知的数据类型
        
        for pos in fc_positions[:20]:  # 分析前20个可能的帧
            if pos + 2 < len(buffer):
                data_type = buffer[pos + 1]
                data_len = buffer[pos + 2]
                
                # 检查是否是合理的数据类型和长度
                if data_type in known_types and 10 <= data_len <= 200:
                    valid_frames.append((pos, data_type, data_len))
                    print(f"  位置 {pos}: 类型=0x{data_type:02x}, 长度={data_len} ✓")
                else:
                    print(f"  位置 {pos}: 类型=0x{data_type:02x}, 长度={data_len}")
        
        # 3. 如果找到有效帧，尝试解析
        if valid_frames:
            print(f"\n🎯 找到 {len(valid_frames)} 个有效帧结构")
            print("尝试解析第一个有效帧...")
            
            pos, data_type, data_len = valid_frames[0]
            total_len = 3 + data_len + 4  # 头+类型+长度+数据+CRC
            
            if pos + total_len <= len(buffer):
                frame_data = buffer[pos:pos + total_len]
                print(f"帧数据: {' '.join([f'{b:02x}' for b in frame_data])}")
                
                # 尝试解析
                if data_type == 0x40 and data_len == 56:  # IMU
                    try:
                        imu_data = struct.unpack('12f ii', frame_data[6:62])  # 跳过头部
                        print("✓ IMU数据解析成功!")
                        print(f"  加速度: X={imu_data[3]:.3f}, Y={imu_data[4]:.3f}, Z={imu_data[5]:.3f}")
                    except:
                        print("✗ IMU数据解析失败")
                
                elif data_type == 0x41 and data_len == 48:  # AHRS
                    try:
                        ahrs_data = struct.unpack('10f ii', frame_data[6:54])  # 跳过头部
                        print("✓ AHRS数据解析成功!")
                        print(f"  欧拉角: 滚转={ahrs_data[3]:.3f}, 俯仰={ahrs_data[4]:.3f}, 偏航={ahrs_data[5]:.3f}")
                    except:
                        print("✗ AHRS数据解析失败")
        
        else:
            print("\n❌ 未找到有效的帧结构")
            print("可能的原因:")
            print("  1. 协议不匹配")
            print("  2. 需要设备初始化")
            print("  3. 硬件问题")
            
            # 显示数据模式分析
            print("\n数据模式分析:")
            byte_counts = {}
            for b in buffer[:100]:
                byte_counts[b] = byte_counts.get(b, 0) + 1
            
            common_bytes = sorted(byte_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            print("最常见字节:", common_bytes)
    
    except KeyboardInterrupt:
        print("\n\n停止")
    finally:
        ser.close()

def try_different_protocols():
    """尝试不同的协议解析"""
    print("\n=== 尝试不同协议 ===")
    
    protocols = [
        {"name": "标准IMU协议", "header": b'\xfc', "types": [0x40, 0x41]},
        {"name": "VN-100协议", "header": b'\xfa', "types": []},
        {"name": "Custom协议", "header": b'\xff', "types": []},
        {"name": "文本协议", "header": b'$', "types": []},
    ]
    
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
        buffer = ser.read(500)  # 读取500字节
        ser.close()
        
        print(f"读取了 {len(buffer)} 字节")
        
        for protocol in protocols:
            header = protocol["header"]
            count = buffer.count(header)
            print(f"{protocol['name']}: 找到头字节 {header.hex()} 共 {count} 次")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    smart_frame_detection()
    try_different_protocols()