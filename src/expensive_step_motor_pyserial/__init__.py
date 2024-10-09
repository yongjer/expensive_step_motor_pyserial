import serial
import time
import threading

# 設定 Serial 連接
arduino_port = "/dev/ttyUSB0"  # 根據你的情況設定
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def send_command(command):
    ser.write(f"{command}\n".encode())  # 發送指令到 Arduino

def motor_control():
    while True:
        command = input("輸入指令 (START CW, START CCW, RUN CW <秒數>, RUN CCW <秒數>, STOP) 或按 'q' 來緊急停止: ")
        if command == 'q':
            send_command("EMERGENCY")  # 緊急停止
            break
        elif command.startswith("RUN"):
            try:
                _, direction, run_time = command.split()  # 提取運行方向和時間
                run_time = int(run_time)
                send_command(f"RUN {direction} {run_time}")
            except ValueError:
                print("無效的時間格式或指令，請輸入正確的方向和秒數！")
        else:
            send_command(command)

def emergency_stop_listener():
    while True:
        if input() == 'q':  # 偵測到 'q' 輸入時即時停止
            send_command("EMERGENCY")
            break

# 啟動馬達控制和緊急停止監聽器
motor_thread = threading.Thread(target=motor_control)
emergency_thread = threading.Thread(target=emergency_stop_listener)

motor_thread.start()
emergency_thread.start()

motor_thread.join()
emergency_thread.join()

ser.close()  # 關閉 Serial 連接
