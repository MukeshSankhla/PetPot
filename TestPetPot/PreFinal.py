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

# Initialize Pygame
pygame.init()

# Set the display dimensions
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the video file
video_file = "Animations/Angry1.mov"                                       # Replace with the actual path to your video file
cap = cv2.VideoCapture(video_file)                                         # Open the video using OpenCV

fontSize =24
iconWidhth = 32
iconHeight = 32

font = pygame.font.Font(None, fontSize)                                                         # You can adjust the font size and style

TempIcon = pygame.image.load("Icons/temperature.png")                                           # Replace with the path to your icon image
TempIcon = pygame.transform.scale(TempIcon, (iconWidhth, iconHeight))                           # Scale the icon if needed
HumIcon = pygame.image.load("Icons/humidity.png")                                               # Replace with the path to your icon image
HumIcon = pygame.transform.scale(HumIcon, (iconWidhth, iconHeight))                             # Scale the icon if needed
SoilMoisIcon = pygame.image.load("Icons/soilMoist.png")                                         # Replace with the path to your icon image
SoilMoisIcon = pygame.transform.scale(SoilMoisIcon, (iconWidhth, iconHeight))                   # Scale the icon if needed
AirQualIcon = pygame.image.load("Icons/air.png")                                                # Replace with the path to your icon image
AirQualIcon = pygame.transform.scale(AirQualIcon, (iconWidhth, iconHeight))                     # Scale the icon if needed
LightIntIcon = pygame.image.load("Icons/light.png")                                             # Replace with the path to your icon image
LightIntIcon = pygame.transform.scale(LightIntIcon, (iconWidhth, iconHeight))                   # Scale the icon if needed
UVIcon = pygame.image.load("Icons/uv.png")                                                      # Replace with the path to your icon image
UVIcon = pygame.transform.scale(UVIcon, (iconWidhth, iconHeight))                               # Scale the icon if needed

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()                                                                    # Read a frame from the video

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)                                                    # Restart the video if it reaches the end
        continue
    
    flipped_frame = cv2.flip(frame, 0)                                                         # Vertically flip the frame (mirror effect)
    frame_resized = cv2.resize(flipped_frame, (screen_height, screen_width))                   # Resize the flipped frame to fit the display
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)                                 # Convert the resized frame to Pygame surface
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    screen.fill((0, 0, 0))                                                                     # Clear the screen
    screen.blit(frame_surface, (0, 0))                                                         # Draw the video frame

    Temperature = SEN0501.get_temperature(TEMP_C)
    Humidity = SEN0501.get_humidity()
    UVIndex = SEN0501.get_ultraviolet_intensity()
    Light = SEN0501.get_luminousintensity()
    # Pressure = SEN0501.get_atmosphere_pressure(HPA)
    # Elevation = SEN0501.get_elevation()
    AirQulity = sgp40.get_voc_index()
    SoilMoisture = MoistureSensor.read_analog()
    # print('Temp : ' + str(Temperature) + ' C')
    # print('Humi: ' + str(Humidity) + ' %')
    # print('UV: ' + str(UVIndex))
    # print('Lux: ' + str(Light))
    # print('Air: ' + str(AirQulity))
    # print('Soil Moisture: ' + str(SoilMoisture))

    text = str(int(Temperature))+' C'                                                       # Replace with your desired text
    text_surface = font.render(text, True, (255, 255, 255))                                 # White text color
    text_surface = pygame.transform.rotate(text_surface, -90)                               # Rotate the text surface by 90 degrees
    screen.blit(text_surface, (160, 5))                                                     # Blit the rotated text surface on the left side of the screen
    
    screen.blit(TempIcon, (180, 10))
    screen.blit(HumIcon, (105, 5))
    screen.blit(SoilMoisIcon, (30, 5))
    screen.blit(AirQualIcon, (180, 285))
    screen.blit(LightIntIcon, (105, 285))
    screen.blit(UVIcon, (30, 285))                                                          # Blit the icon in the top left corner

    pygame.display.update()                                                                 # Update the display without flipping
    clock.tick(30)                                                                          # Adjust the frame rate as needed
    
# Clean up and quit
cap.release()
pygame.quit()
quit()