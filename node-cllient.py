# pc_ip_address


import socketio
import asyncio
import os
import glob
import time
import datetime

sio = socketio.AsyncClient()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

async def sensor_read_data():
    # Loop through each device folder
    for device_folder in device_folders:
        device_file = device_folder + '/w1_slave'
        temperature = read_temp(device_file)[0]  # Get temperature in Celsius
        return {"temperature": temperature}

@sio.event
async def connect():
    print("Connected to server")

    while True:  # Loop for continuous sensor data emission
        sensor_data = await sensor_read_data()
        print(sensor_data)
        await sio.emit("sensorData", sensor_data)
        await asyncio.sleep(1)  # Send data every second

@sio.event
async def disconnect():
    print("Disconnected from server")

async def main():
    pc_ip_address = "172.20.10.3"
    await sio.connect(f"http://{pc_ip_address}:3000", auth={"token": "JetsonNanoNodeClientToken"})
    await sio.wait()  # Wait for disconnection


if __name__ == "__main__":
    asyncio.run(main())



# orking server
# import socketio
# import asyncio
# import random

# sio = socketio.AsyncClient()

# @sio.event
# async def connect():
#     print("Connected to server")

#     while True:  # Loop for continuous sensor data emission
#         sensor_data = await sensor_read_data()
#         print(sensor_data)
#         await sio.emit("sensorData", sensor_data)
#         await asyncio.sleep(1)  # Send data every second

# @sio.event
# async def disconnect():
#     print("Disconnected from server")

# async def sensor_read_data():
#     # Ideally replace this with your actual sensor reading logic
#     temperature = random.randint(30, 50)
#     pressure = random.randint(50, 100)
#     return {"temperature": temperature, "pressure": pressure}

# async def main():
#     await sio.connect("http://localhost:3000", auth={"token": "JetsonNanoNodeClientToken"})
#     await sio.wait()  # Wait for disconnection

# if __name__ == "__main__":
#     asyncio.run(main())
