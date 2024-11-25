# main.py
import pygame
from draw import draw_roads
from roads import roads
from vehicle import Vehicle
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

# 初始化車輛
def generate_vehicle(road):
    """在指定道路上隨機生成車輛"""
    try:
        lane = random.choice(road["lanes"])  # 隨機選擇一條車道
        if road["type"] == "horizontal":
            # 檢查 x_range 和 lane 的範圍是否有效
            if road["x_range"][0] < road["x_range"][1] and lane[0] < lane[1]:
                start = (random.randint(road["x_range"][0], road["x_range"][1]), random.randint(*lane))
                destination = (random.randint(road["x_range"][0], road["x_range"][1]), start[1])
            else:
                raise ValueError(f"Invalid range in road: {road}")
        elif road["type"] == "vertical":
            # 檢查 y_range 和 lane 的範圍是否有效
            if road["y_range"][0] < road["y_range"][1] and lane[0] < lane[1]:
                start = (random.randint(*lane), random.randint(road["y_range"][0], road["y_range"][1]))
                destination = (start[0], random.randint(road["y_range"][0], road["y_range"][1]))
            else:
                raise ValueError(f"Invalid range in road: {road}")
        else:
            raise ValueError(f"Unknown road type: {road['type']}")

        return Vehicle(start, destination, road["type"])

    except Exception as e:
        print(f"Error generating vehicle for road {road['name']}: {e}")
        return None

vehicles = [v for v in (generate_vehicle(random.choice(roads)) for _ in range(10)) if v is not None]

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
            vehicle.move()
            vehicle.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
