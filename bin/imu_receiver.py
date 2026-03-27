import argparse
import sys
import serial
import serial.tools.list_ports
import struct
import time
import math
import os
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

# 将Yesense库的路径加入系统路径，以便导入 SDK 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'Yesense-Decode-Python3-V2.0'))
try:
    from yis_std_dec import std_decoder
except ImportError as e:
    print(f"Failed to import Yesense SDK (yis_std_dec). Error: {e}")

# 转换系数 - yis_std_dec中解析出来是角度(Degree)，这里转为弧度与原有接收端对齐
DEG_TO_RAD = math.pi / 180.0

# 全局变量
_serial_port = None
_last_result = None
_dec_buf = bytearray()
_decoder = None
# variable to save decoded result (与main.py一致)
_yis_out = {
    'tid':1, 'roll':0.0, 'pitch':0.0, 'yaw':0.0, 
    'q0':1.0, 'q1':1.0, 'q2':0.0, 'q3':0.0, 
    'sensor_temp':25.0, 'acc_x':0.0, 'acc_y':0.0, 'acc_z':1.0, 
    'gyro_x':0.0, 'gyro_y':0.0, 'gyro_z':0.0,	
    'norm_mag_x':0.0, 'norm_mag_y':0.0, 'norm_mag_z':0.0,	
    'raw_mag_x':0.0, 'raw_mag_y':0.0, 'raw_mag_z':0.0,	
    'lat':0.0, 'longt':0.0, 'alt':0.0,	
    'vel_e':0.0, 'vel_n':0.0, 'vel_u':0.0, 
    'ms':0, 'year': 2022, 'month':8, 'day': 31, 
    'hour':12, 'minute':0, 'second':0,	
    'smp_timestamp':0, 'ready_timestamp':0 ,'status':0
}

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, default='/dev/ttyACM0', help='serial port')
    parser.add_argument('--bps', type=int, default=460800, help='baud rate')
    parser.add_argument('--timeout', type=float, default=0.002, help='timeout')
    receive_params = parser.parse_known_args()[0] if known else parser.parse_args()
    return receive_params

def init_serial():
    global _serial_port, _decoder
    if _serial_port is not None and _serial_port.isOpen():
        return _serial_port

    args = parse_opt()
    try:
        _serial_port = serial.Serial(port=args.port, baudrate=args.bps, bytesize=EIGHTBITS, parity=PARITY_NONE,
                                stopbits=STOPBITS_ONE, timeout=args.timeout)
        if _decoder is None:
            _decoder = std_decoder()
        print(f"Serial port {args.port} opened successfully at {args.bps} with Yesense SDK")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        _serial_port = None
    return _serial_port

def get_empty_result():
    return {
        "Accelerometer_X": 0.0, "Accelerometer_Y": 0.0, "Accelerometer_Z": 0.0,
        "RollSpeed": 0.0, "PitchSpeed": 0.0, "HeadingSpeed": 0.0,
        "Roll": 0.0, "Pitch": 0.0, "Heading": 0.0,
        "qw": 1.0, "qx": 0.0, "qy": 0.0, "qz": 0.0,
    }

def read_imu_data():
    global _serial_port, _last_result, _dec_buf, _yis_out, _decoder
    
    if _last_result is None:
        _last_result = get_empty_result()

    if _serial_port is None:
        init_serial()
        if _serial_port is None:
            return _last_result

    try:
        # 读取数据
        data = _serial_port.read(_serial_port.in_waiting or 200)
        num = len(data)
        if num > 0:
            _dec_buf.extend(bytearray(data))
            
        updated = False
        # 解析缓冲区内所有的完整帧
        while len(_dec_buf) > 0:
            current_len = len(_dec_buf)
            ret = _decoder.proc_data(_dec_buf, current_len, _yis_out, False)
            if ret:
                updated = True
            elif len(_dec_buf) == current_len:
                # 若解析没成功且缓冲区长度没有被清空变化，说明数据包还没完全接收，跳出等下一次读取
                break
                
        if updated:
            # 提取转换出的最新数据，并执行标准对齐。
            # 为了对接原有 imu_receiver格式且保证“Z轴向上，X轴向前”的标准
            # 我们延用原有的赋值极性，同时将角度制转为弧度制。
            _last_result["Accelerometer_X"] = _yis_out['acc_x']
            _last_result["Accelerometer_Y"] = _yis_out['acc_y']
            _last_result["Accelerometer_Z"] = _yis_out['acc_z']
            
            # 使用与之前一样的对齐方式：X对应Roll，Y对应Pitch并反向
            _last_result["RollSpeed"] = _yis_out['gyro_x'] * DEG_TO_RAD
            _last_result["PitchSpeed"] = _yis_out['gyro_y'] * DEG_TO_RAD
            _last_result["HeadingSpeed"] = _yis_out['gyro_z'] * DEG_TO_RAD
            
            _last_result["Pitch"] = _yis_out['pitch'] * DEG_TO_RAD
            _last_result["Roll"] = _yis_out['roll'] * DEG_TO_RAD
            _last_result["Heading"] = _yis_out['yaw'] * DEG_TO_RAD
            
            # 四元数
            _last_result["qw"] = _yis_out['q0']
            _last_result["qx"] = _yis_out['q1']
            _last_result["qy"] = _yis_out['q2']
            _last_result["qz"] = _yis_out['q3']
            
    except Exception as e:
        print(f"Error reading IMU: {e}")
        try:
            _serial_port.close()
        except:
            pass
        _serial_port = None
        
    return _last_result

if __name__ == "__main__":
    print("Start reading IMU data...")
    while True:
        data = read_imu_data()
        print(f"Angle(rad) => Roll: {data['Roll']:.4f}, Pitch: {data['Pitch']:.4f}, Yaw: {data['Heading']:.4f} | "
              f"Acc(g) => X: {data['Accelerometer_X']:.4f}, Y: {data['Accelerometer_Y']:.4f}, Z: {data['Accelerometer_Z']:.4f} | "
              f"Gyro(rad/s) => X: {data['RollSpeed']:.4f}, Y: {data['PitchSpeed']:.4f}, Z: {data['HeadingSpeed']:.4f}")
        time.sleep(0.005)
