# draw.py
import pygame
from roads import roads

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD_COLOR = (169, 169, 169)
YELLOW = (255, 255, 0)

def draw_roads(screen):
    """繪製所有道路"""
    screen.fill(WHITE)
    for road in roads:
        # 繪製邊緣（黑色）
        for border in road["borders"]:
            if road["type"] == "horizontal":
                pygame.draw.rect(screen, BLACK, (road["x_range"][0], border[0], road["x_range"][1] - road["x_range"][0], border[1] - border[0]))
            elif road["type"] == "vertical":
                pygame.draw.rect(screen, BLACK, (border[0], road["y_range"][0], border[1] - border[0], road["y_range"][1] - road["y_range"][0]))

        # 繪製車道（灰色）
        for lane in road["lanes"]:
            if road["type"] == "horizontal":
                pygame.draw.rect(screen, ROAD_COLOR, (road["x_range"][0], lane[0], road["x_range"][1] - road["x_range"][0], lane[1] - lane[0]))
            elif road["type"] == "vertical":
                pygame.draw.rect(screen, ROAD_COLOR, (lane[0], road["y_range"][0], lane[1] - lane[0], road["y_range"][1] - road["y_range"][0]))

        # 繪製車道間隔（黃色）
        for separation in road["separation"]:
            if road["type"] == "horizontal":
                pygame.draw.rect(screen, YELLOW, (road["x_range"][0], separation[0], road["x_range"][1] - road["x_range"][0], separation[1] - separation[0]))
            elif road["type"] == "vertical":
                pygame.draw.rect(screen, YELLOW, (separation[0], road["y_range"][0], separation[1] - separation[0], road["y_range"][1] - road["y_range"][0]))
