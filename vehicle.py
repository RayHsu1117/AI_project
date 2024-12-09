# vehicle.py
from collections import deque
import pygame
from start_end import generate_start, generate_end
from roads import get_road_data
import globals
CAR_COLOR = (255, 0, 0)  # 紅色
CAR_REACHED_COLOR = (255, 165, 0)  # 橘色

class Vehicle:
    def __init__(self, start, destination,road_name, road_type):
        self.x, self.y = start
        self.path = deque(self.calculate_path(start, destination, road_name))  # 計算路徑
        self.destination = destination
        self.road_type = road_type
        self.reached_destination = False  # 車輛是否到達終點
        self.current_road = road_name
        self.speed = 300 / globals.fps  # 每秒 10 pixels，對應到每幀 (30 FPS) 的移動距離

    

    def calculate_path(self, start, destination, road_name):
        """計算車輛移動的路徑"""
        path = []
        sx, sy = start
        dx, dy = destination
 
        return path

    def move(self):
        """讓車輛沿路徑移動"""
        # if not self.reached_destination and self.path:
        #     self.x, self.y = self.path.popleft()
        # if not self.path:  # 如果路徑空了，標記為到達終點
        #     self.reached_destination = True
        self.y -= self.speed  # 向上移動


    def draw(self, screen):
        """繪製車輛"""
        color = CAR_REACHED_COLOR if self.reached_destination else CAR_COLOR
        pygame.draw.rect(screen, color, (self.x, self.y, 8, 8))
    def draw_end(self,screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.destination[0], self.destination[1], 8, 8))


def generate_vehicle(road):
    """在指定道路上隨機生成車輛"""
    road = get_road_data(road["name"])
    try:
        start = generate_start()
        destination = generate_end()
        return Vehicle(start, destination,road["name"] ,road["type"])

    except Exception as e:
        print(f"Error generating vehicle for road {road['name']}: {e}")
        return None

    road = get_road_data(road_name)
    if road["type"] == "horizontal":
        lane = road["lanes"][0]
        if lane[0] < current_y < lane[1]:
            return "left"
        else:
            return "right"
    else:
        lane = road["lanes"][0]
        if lane[0] < current_x < lane[1]:
            return "down"
        else:
            return "up"