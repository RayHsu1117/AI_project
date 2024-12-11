# vehicle.py
from collections import deque
import pygame
# from start_end import generate_start, generate_end
# from roads import roads
from map import roads
import random
import globals

VEHICLE_SIZE = 15
CAR_COLOR = (255, 0, 0)  # 紅色
CAR_REACHED_COLOR = (255, 165, 0)  # 橘色

# 車輛編號計數器
vehicle_counter = 1

class Vehicle:
    def __init__(self, start, destination,start_road,destination_road, vehicle_id):
        self.x, self.y = start
        self.path = deque(self.calculate_path(start, destination))  # 計算路徑
        self.start = start
        self.destination = destination
        self.reached_destination = False  # 車輛是否到達終點
        self.start_road = start_road
        self.destination_road = destination_road
        self.speed = 100 / globals.fps  # 車輛速度
        self.vehicle_id = vehicle_id  # 使用傳入的車號

    def calculate_path(self, start, destination):
        """計算車輛移動的路徑"""
        path = []
        sx, sy = start
        dx, dy = destination
 
        return path

    # def move(self):
    #     """讓車輛沿路徑移動"""
    #     if not self.reached_destination and self.path:
    #         self.x, self.y = self.path.popleft()
    #     if not self.path:  # 如果路徑空了，標記為到達終點
    #         self.reached_destination = True

    def move(self, direction):
        if direction == "UP":
            self.y -= self.speed
        elif direction == "DOWN":
            self.y += self.speed
        elif direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed

    def draw(self, screen):
        """繪製車輛"""
        color = CAR_REACHED_COLOR if self.reached_destination else CAR_COLOR
        pygame.draw.rect(screen, color, (self.x, self.y, VEHICLE_SIZE, VEHICLE_SIZE))
    
        # 顯示車號
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.vehicle_id), True, (0, 0, 0))  # 車號顯示為黑色
    
        # 計算車號顯示的位置，使其位於車輛方框的中心
        text_rect = text.get_rect(center=(self.x + VEHICLE_SIZE // 2, self.y + VEHICLE_SIZE // 2))
        screen.blit(text, text_rect)  # 把車號渲染到畫面

    def draw_end(self, screen):
        """繪製終點並顯示車號"""
        pygame.draw.rect(screen, (0, 255, 0), (self.destination[0], self.destination[1], VEHICLE_SIZE, VEHICLE_SIZE))
    
        # 顯示車號
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.vehicle_id), True, (0, 0, 0))  # 車號顯示為黑色
    
        # 計算車號顯示的位置，使其位於終點方框的中心
        text_rect = text.get_rect(center=(self.destination[0] + VEHICLE_SIZE // 2, self.destination[1] + VEHICLE_SIZE // 2))
        screen.blit(text, text_rect)  # 把車號渲染到畫面


def generate_vehicle():
    """在隨機道路上隨機生成車輛"""
    global vehicle_counter  # 引用全局車輛編號變數
    try:
        start_point, start_road = generate_random()
        destination_point, destination_road = generate_random()
        
        # 創建車輛並將當前車號傳入
        vehicle = Vehicle(start_point, destination_point, start_road, destination_road, vehicle_counter)
        
        # 車號遞增
        vehicle_counter += 1
        
        return vehicle

    except Exception as e:
        print(f"Error generating vehicle : {e}")
        return None


def generate_random():
    """生成隨機的點"""
    road = random.choice(list(roads.keys()))
    if(roads[road].direction == "LEFT" or roads[road].direction == "RIGHT"):
        point = (random.randint(roads[road].x1,roads[road].x2),random.randint(roads[road].y1,roads[road].y2-VEHICLE_SIZE))
    else:    
        point = (random.randint(roads[road].x1,roads[road].x2-VEHICLE_SIZE),random.randint(roads[road].y1,roads[road].y2))
    return point,road
