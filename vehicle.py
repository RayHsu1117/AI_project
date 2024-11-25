# vehicle.py
from collections import deque
import pygame

CAR_COLOR = (255, 0, 0)  # 紅色
CAR_REACHED_COLOR = (255, 165, 0)  # 橘色

class Vehicle:
    def __init__(self, start, destination, road_type):
        self.x, self.y = start
        self.path = deque(self.calculate_path(start, destination, road_type))  # 計算路徑
        self.destination = destination
        self.road_type = road_type
        self.reached_destination = False  # 車輛是否到達終點

    def calculate_path(self, start, destination, road_type):
        """計算車輛移動的路徑"""
        path = []
        sx, sy = start
        dx, dy = destination

        if road_type == "horizontal":
            for x in range(sx, dx, 1 if dx > sx else -1):
                path.append((x, sy))
        elif road_type == "vertical":
            for y in range(sy, dy, 1 if dy > sy else -1):
                path.append((sx, y))

        return path

    def move(self):
        """讓車輛沿路徑移動"""
        if not self.reached_destination and self.path:
            self.x, self.y = self.path.popleft()
        if not self.path:  # 如果路徑空了，標記為到達終點
            self.reached_destination = True

    def draw(self, screen):
        """繪製車輛"""
        color = CAR_REACHED_COLOR if self.reached_destination else CAR_COLOR
        pygame.draw.rect(screen, color, (self.x, self.y, 8, 8))
