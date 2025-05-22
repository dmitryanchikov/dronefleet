#!/usr/bin/env python3
import time
import os
from dotenv import load_dotenv
import pyMultiWii

# Загружаем переменные окружения
load_dotenv()

# Получаем порт из переменных окружения
port = os.getenv('PORT')

def connect_drone():
    """
    Подключение к дрону через TCP/IP
    
    Примечание: Эта реализация работает только с дронами,
    которые используют TCP/IP соединение (например, Pluto Drone).
    Для дронов с USB-подключением используйте msp_telemetry.py
    """
    try:
        # Для Pluto Drone используется TCP/IP соединение
        # IP адрес и порт по умолчанию для Pluto: 192.168.4.1:23
        print("Подключение к дрону через TCP/IP...")
        board = pyMultiWii.pyMultiWii("192.168.4.1", 23)
        print("Подключение успешно!")
        return board
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def get_telemetry(board):
    """
    Получение телеметрии с дрона
    
    Примечание: pyMultiWii не имеет прямых методов для получения телеметрии,
    поэтому этот метод является заглушкой. В реальной ситуации необходимо
    использовать другие библиотеки или собственную реализацию.
    """
    try:
        # Это заглушка, так как библиотека pyMultiWii не предоставляет
        # методов для получения телеметрии
        return {
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'voltage': 0
        }
    except Exception as e:
        print(f"Ошибка получения телеметрии: {e}")
        return None

def main():
    print("ВАЖНОЕ ПРИМЕЧАНИЕ:")
    print("Библиотека pyMultiWii разработана специально для Pluto Drone")
    print("и использует TCP/IP соединение вместо USB.")
    print("Она не подходит для дронов с Betaflight через USB.")
    print("Для вашего дрона рекомендуется использовать msp_telemetry.py\n")
    
    # Подключаемся к дрону
    board = connect_drone()
    if not board:
        print("Не удалось подключиться к дрону")
        return
    
    try:
        # Вместо получения телеметрии, демонстрируем управление
        print("Демонстрация управления (без получения телеметрии):")
        
        # Включаем моторы
        print("Включение моторов...")
        board.arm()
        time.sleep(2)
        
        # Устанавливаем минимальные обороты двигателя
        print("Установка минимальной тяги...")
        board.setThrottle(1000)
        time.sleep(2)
        
        # Отключаем моторы
        print("Отключение моторов...")
        board.disarm()
            
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем соединение
        if board:
            board.disconnect()
            print("Соединение закрыто")

if __name__ == "__main__":
    main() 