# main.py
import pygame
from draw import draw_roads
from roads import roads
from vehicle import Vehicle, generate_vehicle
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 700))

# 初始化車輛

vehicles = [v for v in (generate_vehicle(random.choice(roads)) for _ in range(5)) if v is not None]

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
            # vehicle.move()
            vehicle.draw(screen)
            vehicle.draw_end(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
