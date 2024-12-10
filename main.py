# main.py
import pygame
from draw import draw_roads
# from roads import roads
from vehicle import generate_vehicle
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))

# 設定要初始化幾台車
how_many_cars = 1
# 初始化車輛s
vehicles = []
for i in range(how_many_cars):
    vehicle = generate_vehicle()
    vehicles.append(vehicle)

# 主程序
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
            vehicle.move("UP")
            vehicle.draw(screen)
            vehicle.draw_end(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
