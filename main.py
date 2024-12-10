# main.py
import pygame
from draw import draw_roads
from vehicle import generate_vehicle
from map import roads  # 導入道路資料
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

def create_graph(roads):
    """
    創建一個圖 (Graph)，用於最短路徑計算。
    :param roads: 道路物件的字典
    :return: 圖的鄰接表表示法 {節點: [(鄰居節點, 邊的權重)]}
    """
    graph = {}
    for road_name, road in roads.items():
        # 道路起點與終點作為節點
        start_node = (road.x1, road.y1)
        end_node = (road.x2, road.y2)

        # 根據方向計算距離
        if road.direction in ['LEFT', 'RIGHT']:
            distance = abs(road.x2 - road.x1)  # 水平道路使用 x 差值
        elif road.direction in ['UP', 'DOWN']:
            distance = abs(road.y2 - road.y1)  # 垂直道路使用 y 差值
        else:
            raise ValueError(f"Unknown road direction: {road.direction}")

        # 添加起點到終點的邊
        if start_node not in graph:
            graph[start_node] = []
        graph[start_node].append((end_node, distance))

        # 添加終點到起點的邊
        if end_node not in graph:
            graph[end_node] = []
        graph[end_node].append((start_node, distance))

    return graph

# 主程序
def main():

    # 創建道路圖結構
    graph = create_graph(roads)
    from pprint import pprint
    pprint(graph)

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
