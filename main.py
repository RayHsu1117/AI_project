# main.py
import pygame
from draw import draw_roads
# from roads import roads
from vehicle import generate_vehicle
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((602, 602))

# 初始化車輛

vehicles = []
for i in range(10):
    vehicle = generate_vehicle()
    vehicles.append(vehicle)
# 主程式
def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 繪製場景
        draw_roads(screen)
        
        for vehicle in vehicles:
            vehicle.move(vehicles)  # 更新車輛位置
            vehicle.draw_car(screen)  # 繪製車輛
            vehicle.draw_end(screen)  # 繪製目標位置

        pygame.display.flip()
        clock.tick(30)  # 控制幀率

if __name__ == "__main__":
    main()
