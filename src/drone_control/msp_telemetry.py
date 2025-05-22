#!/usr/bin/env python3
import serial
import time
import struct
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем порт из переменных окружения или используем значение по умолчанию
port = os.getenv('PORT')

class MSPProtocol:
    """Базовый класс для работы с MSP протоколом"""
    
    # MSP команды
    MSP_ATTITUDE = 108
    MSP_ANALOG = 110
    MSP_RAW_IMU = 102
    
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate)
        
    def send_cmd(self, cmd, data=None):
        """Отправка команды по протоколу MSP"""
        if data is None:
            data = []
            
        size = len(data)
        checksum = 0
        
        # Заголовок пакета
        packet = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), size, cmd]
        
        # Расчет контрольной суммы
        checksum ^= size
        checksum ^= cmd
        
        # Добавление данных и обновление контрольной суммы
        for d in data:
            checksum ^= d
            packet.append(d)
            
        packet.append(checksum)
        
        # Отправка пакета
        for b in packet:
            if isinstance(b, int):
                self.serial.write(struct.pack('B', b))
            else:
                self.serial.write(b)
                
    def read_response(self):
        """Чтение ответа от контроллера"""
        header = self.serial.read(3)
        if header != b'$M>':
            return None
            
        size = struct.unpack('B', self.serial.read(1))[0]
        cmd = struct.unpack('B', self.serial.read(1))[0]
        data = self.serial.read(size)
        checksum = struct.unpack('B', self.serial.read(1))[0]
        
        return {'cmd': cmd, 'data': data}
        
    def get_attitude(self):
        """Получение данных о положении дрона"""
        self.send_cmd(self.MSP_ATTITUDE)
        response = self.read_response()
        if response and len(response['data']) >= 6:
            roll = struct.unpack('<h', response['data'][0:2])[0] / 10.0
            pitch = struct.unpack('<h', response['data'][2:4])[0] / 10.0
            yaw = struct.unpack('<h', response['data'][4:6])[0]
            return {'roll': roll, 'pitch': pitch, 'yaw': yaw}
        return None
        
    def get_battery(self):
        """Получение данных о батарее"""
        self.send_cmd(self.MSP_ANALOG)
        response = self.read_response()
        if response and len(response['data']) >= 3:
            vbat = struct.unpack('B', response['data'][0:1])[0] / 10.0
            return {'voltage': vbat}
        return None
        
    def close(self):
        """Закрытие соединения"""
        self.serial.close()

def main():
    # Подключаемся к дрону
    try:
        print(f'Подключение к дрону на порту {port}...')
        drone = MSPProtocol(port)
        print('Подключение успешно!')
        
        while True:
            # Получаем данные о положении
            attitude = drone.get_attitude()
            if attitude:
                print(f"\nПоложение дрона:")
                print(f"Крен (Roll): {attitude['roll']}°")
                print(f"Тангаж (Pitch): {attitude['pitch']}°")
                print(f"Рыскание (Yaw): {attitude['yaw']}°")
            
            # Получаем данные о батарее
            battery = drone.get_battery()
            if battery:
                print(f"\nБатарея:")
                print(f"Напряжение: {battery['voltage']}V")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if 'drone' in locals():
            drone.close()

if __name__ == "__main__":
    main() 