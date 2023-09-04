import time
import pygame
import cv2
import numpy as np

from DFRobot_Environmental_Sensor import *
from DFRobot_SGP40 import DFRobot_SGP40
from pinpong.board import Board, Pin

Board().begin()

SEN0501 = DFRobot_Environmental_Sensor_I2C(bus=0x01,addr=0x22)      #Initialize Environmental Sensor
sgp40 = DFRobot_SGP40(relative_humidity=50, temperature_c=25)       #Initialize Air Quality Sensor
MoistureSensor = Pin(Pin.P21, Pin.ANALOG)                           #Initialize Soil Moisture Sensor

# Atmospheric pressure unit select
HPA = 0x01
KPA = 0X02
# Temperature unit select
TEMP_C = 0X03
TEMP_F = 0X04

SEN0501.begin()
sgp40.begin(10)

while True:
    Temperature = SEN0501.get_temperature(TEMP_C)
    Humidity = SEN0501.get_humidity()
    UVIndex = SEN0501.get_ultraviolet_intensity()
    Light = SEN0501.get_luminousintensity()
#   Pressure = SEN0501.get_atmosphere_pressure(HPA)
#   Elevation = SEN0501.get_elevation()
    AirQulity = sgp40.get_voc_index()
    SoilMoisture = MoistureSensor.read_analog()
    print('Temp : ' + str(Temperature) + ' C')
    print('Humi: ' + str(Humidity) + ' %')
    print('UV: ' + str(UVIndex))
    print('Lux: ' + str(Light))
    print('Air: ' + str(AirQulity))
    print('Soil Moisture: ' + str(SoilMoisture))
    time.sleep(1)
