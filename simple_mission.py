#!/usr/bin/env python3
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Подключаемся к реальному дрону через USB
print('Подключение к дрону через USB...')
vehicle = connect('/dev/tty.usbmodem327F357730331', wait_ready=True, baud=57600)

def arm_and_takeoff(target_altitude):
    """
    Запуск двигателей и взлет на заданную высоту
    """
    print("Базовые проверки перед взлетом")
    
    while not vehicle.is_armable:
        print("Ожидание готовности дрона...")
        time.sleep(1)

    print("Переключение в режим GUIDED")
    vehicle.mode = VehicleMode("GUIDED")
    
    print("Запуск двигателей")
    vehicle.armed = True

    while not vehicle.armed:
        print("Ожидание запуска двигателей...")
        time.sleep(1)

    print("Взлет!")
    vehicle.simple_takeoff(target_altitude)

    # Ожидание достижения высоты
    while True:
        print(f"Текущая высота: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Достигнута целевая высота")
            break
        time.sleep(1)

try:
    # Взлет на высоту 10 метров
    arm_and_takeoff(10)

    print("Полет вперед")
    # Задаем точку в 30 метрах вперед от текущей позиции
    point = LocationGlobalRelative(
        vehicle.location.global_relative_frame.lat + 0.0001,
        vehicle.location.global_relative_frame.lon,
        10
    )
    vehicle.simple_goto(point)
    time.sleep(20)  # Ждем 20 секунд

    print("Возвращение домой")
    vehicle.mode = VehicleMode("RTL")  # Return To Launch
    
    # Ожидание приземления
    while vehicle.location.global_relative_frame.alt > 0.1:
        print(f"Высота: {vehicle.location.global_relative_frame.alt}")
        time.sleep(1)

finally:
    print("Завершение программы")
    vehicle.close() 