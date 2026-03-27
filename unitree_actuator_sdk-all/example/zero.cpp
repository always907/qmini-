#include <unistd.h>
#include "serialPort/SerialPort.h"
#include "unitreeMotor/unitreeMotor.h"


int main() {

  SerialPort  serial1("/dev/ttyUSB0");
  SerialPort  serial2("/dev/ttyUSB1");
  SerialPort  serial3("/dev/ttyUSB2");
  SerialPort  serial4("/dev/ttyUSB3");
  MotorCmd    cmd;
  MotorData   data;

  cmd.motorType = MotorType::GO_M8010_6;
  data.motorType = MotorType::GO_M8010_6;
  cmd.mode = queryMotorMode(MotorType::GO_M8010_6,MotorMode::FOC);
  cmd.id   = 0;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial1.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor1.0.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 1;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial1.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor1.1.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 2;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial1.sendRecv(&cmd,&data);


  std::cout <<  std::endl;
  std::cout <<  "motor1.2.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 0;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial2.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor2.0.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 1;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial2.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor2.1.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);


  cmd.id   = 0;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial3.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor3.0.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 1;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial3.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor3.1.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 2;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial3.sendRecv(&cmd,&data);

  usleep(200);
  std::cout <<  std::endl;
  std::cout <<  "motor3.2.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  cmd.id   = 0;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial4.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor4.0.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 1;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial4.sendRecv(&cmd,&data);

  std::cout <<  std::endl;
  std::cout <<  "motor4.1.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

  usleep(200);

  cmd.id   = 2;
  cmd.kp   = 0.0;
  cmd.kd   = 0.0;
  cmd.q    = 0.0;
  cmd.dq   = 0;
  cmd.tau  = 0.0;
  serial4.sendRecv(&cmd,&data);


  std::cout <<  std::endl;
  std::cout <<  "motor4.2.q: "    << data.q    <<  std::endl;
  std::cout <<  std::endl;

}
