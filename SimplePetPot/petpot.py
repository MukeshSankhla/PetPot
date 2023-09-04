import pygame
import cv2
import random
import datetime
import pytz
from DFRobot_Environmental_Sensor import *
from DFRobot_SGP40 import DFRobot_SGP40
from pinpong.board import Board, Pin

Board().begin()

SEN0501 = DFRobot_Environmental_Sensor_I2C(bus=0x01, addr=0x22)  # Initialize Environmental Sensor
sgp40 = DFRobot_SGP40(relative_humidity=50, temperature_c=25)  # Initialize Air Quality Sensor
MoistureSensor = Pin(Pin.P21, Pin.ANALOG)  # Initialize Soil Moisture Sensor

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

# Load the emoji animations
emoji_animations = {
    'angry1': cv2.VideoCapture("Animations/Angry1.mov"),
    'angry2': cv2.VideoCapture("Animations/Angry2.mov"),
    'angry3': cv2.VideoCapture("Animations/Angry3.mov"),
    'angry4': cv2.VideoCapture("Animations/Angry4.mov"),
    'happy1': cv2.VideoCapture("Animations/Happy1.mov"),
    'happy2': cv2.VideoCapture("Animations/Happy2.mov"),
    'happy3': cv2.VideoCapture("Animations/Happy3.mov"),
    'happy4': cv2.VideoCapture("Animations/Happy4.mov"),
    'sad1': cv2.VideoCapture("Animations/Sad1.mov"),
    'sad2': cv2.VideoCapture("Animations/Sad2.mov"),
    'sad3': cv2.VideoCapture("Animations/Sad3.mov"),
    'sad4': cv2.VideoCapture("Animations/Sad4.mov"),
    'cold': cv2.VideoCapture("Animations/Cold.mov"),
    'dead': cv2.VideoCapture("Animations/Dead.mov"),
    'hot1': cv2.VideoCapture("Animations/Hot1.mov"),
    'hot2': cv2.VideoCapture("Animations/Hot2.mov"),
    'sleep1': cv2.VideoCapture("Animations/Sleep1.mov"),
    'sleep2': cv2.VideoCapture("Animations/Sleep2.mov"),
    'sniff': cv2.VideoCapture("Animations/Sniff.mov"),
    'tired': cv2.VideoCapture("Animations/Tired.mov"),
    'vomit': cv2.VideoCapture("Animations/Vomit.mov")
}

current_animation = emoji_animations['happy1']  # Default animation

fontSize = 24
iconWidhth = 32
iconHeight = 32
ist = pytz.timezone('Asia/Kolkata')  # IST timezone

font = pygame.font.Font(None, fontSize)  # You can adjust the font size and style

TempIcon = pygame.image.load("Icons/temperature.png")  # Replace with the path to your icon image
TempIcon = pygame.transform.scale(TempIcon, (iconWidhth, iconHeight))  # Scale the icon if needed
HumIcon = pygame.image.load("Icons/humidity.png")  # Replace with the path to your icon image
HumIcon = pygame.transform.scale(HumIcon, (iconWidhth, iconHeight))  # Scale the icon if needed
SoilMoisIcon = pygame.image.load("Icons/soilMoist.png")  # Replace with the path to your icon image
SoilMoisIcon = pygame.transform.scale(SoilMoisIcon, (iconWidhth, iconHeight))  # Scale the icon if needed
AirQualIcon = pygame.image.load("Icons/air.png")  # Replace with the path to your icon image
AirQualIcon = pygame.transform.scale(AirQualIcon, (iconWidhth, iconHeight))  # Scale the icon if needed
LightIntIcon = pygame.image.load("Icons/light.png")  # Replace with the path to your icon image
LightIntIcon = pygame.transform.scale(LightIntIcon, (iconWidhth, iconHeight))  # Scale the icon if needed
UVIcon = pygame.image.load("Icons/uv.png")  # Replace with the path to your icon image
UVIcon = pygame.transform.scale(UVIcon, (iconWidhth, iconHeight))  # Scale the icon if needed

randomNum = 1
suffle = True

# Initialize time variables for readings
last_air_quality_reading_time = datetime.datetime.now(ist)
last_other_readings_time = datetime.datetime.now(ist)

# Intervals for readings
air_quality_interval = datetime.timedelta(minutes=5)

# Main loop
running = True
clock = pygame.time.Clock()

AirQuality = sgp40.get_voc_index()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = current_animation.read()
    if not ret:
        current_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    flipped_frame = cv2.flip(frame, 0)
    frame_resized = cv2.resize(flipped_frame, (screen_height, screen_width))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    screen.fill((0, 0, 0))
    screen.blit(frame_surface, (0, 0))

    current_time = datetime.datetime.now(ist)
    minute = current_time.minute
    # print(current_time)

    # Check if it's time to take an Air Quality reading
    if current_time - last_air_quality_reading_time >= air_quality_interval:
        try:
            AirQuality = sgp40.get_voc_index()
            last_air_quality_reading_time = current_time
            print(f"Air Quality: {AirQuality}")
        except Exception as e:
            print(f"Error reading Air Quality data: {e}")
    else:
        try:
            SoilMoisture = MoistureSensor.read_analog()
            Temperature = SEN0501.get_temperature(TEMP_C)
            Humidity = SEN0501.get_humidity()
            UVIndex = SEN0501.get_ultraviolet_intensity()
            Light = SEN0501.get_luminousintensity()
        except Exception as e:
            print(f"Error reading other sensor data: {e}")

    # print(f"Soil Moisture: {(SoilMoisture / 4096) * 100} %")
    # print(f"Temperature: {Temperature} C")
    # print(f"Humidity: {Humidity} %")
    # print(f"UV Index: {UVIndex}")
    # print(f"Light Intensity: {Light}")

    # Check sensor parameters and select the appropriate animation
    if SoilMoisture < 100:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['dead']
    elif SoilMoisture > 100 and SoilMoisture < 2360:  # Adjust the temperature threshold as needed
        current_animation = emoji_animations['angry' + str(randomNum)]
    elif Light < 5:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['sleep1']
    elif UVIndex > 5:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['sad' + str(randomNum)]
    elif AirQuality > 150 and AirQuality > 200:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['vomit']
    elif AirQuality > 150:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['sniff']
    elif Temperature > 30:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['hot1']
    elif Temperature < 15:  # Adjust the humidity threshold as needed
        current_animation = emoji_animations['cold']
    else:
        current_animation = emoji_animations['happy' + str(randomNum)]

    # Render and display Temperature text
    text = str(int(Temperature)) + ' C'
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (160, 5))
    screen.blit(TempIcon, (180, 7))

    # Render and display Humidity text
    text = str(int(Humidity)) + ' %'
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (85, 5))
    screen.blit(HumIcon, (105, 7))

    # Render and display Soil Moisture text
    text = str(int((SoilMoisture / 4096) * 100)) + ' %'
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (10, 5))
    screen.blit(SoilMoisIcon, (30, 7))

    # Render and display Air Quality text
    text = str(int(AirQuality))
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (160, 285))
    screen.blit(AirQualIcon, (180, 280))

    # Render and display Light Intensity text
    text = str(int(Light))
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (85, 285))
    screen.blit(LightIntIcon, (105, 280))

    # Render and display UV Index text
    text = str(int(UVIndex))
    text_surface = font.render(text, True, (255, 255, 255))
    text_surface = pygame.transform.rotate(text_surface, -90)
    screen.blit(text_surface, (10, 290))
    screen.blit(UVIcon, (30, 280))

    pygame.display.update()
    clock.tick(30)

# Clean up video capture objects and quit
for cap in emoji_animations.values():
    cap.release()

try:
    pygame.quit()
except pygame.error as e:
    print(f"Pygame error while quitting: {e}")

quit()

