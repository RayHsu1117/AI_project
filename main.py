import pygame
import argparse
from draw import draw_roads
from vehicle import generate_vehicle, car_crash, every_vehicle_reached_end
import globals

# Add argparse to get simulation_id and no-draw option from the command line
parser = argparse.ArgumentParser(description="Simulate traffic with vehicles.")
parser.add_argument("simulation_id", type=int, help="Simulation ID for logging results")
parser.add_argument("--no-draw", action="store_true", help="Disable drawing for faster simulation")
args = parser.parse_args()

# Configure global drawing flag
globals.enable_drawing = not args.no_draw

how_many_cars = 10

def main(simulation_id):
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((602, 602)) if globals.enable_drawing else None

    # Initialize vehicles
    vehicles = [generate_vehicle() for _ in range(how_many_cars)]

    clock = pygame.time.Clock()
    running = True
    crash = False
    total_frames = 0  # Total frames

    while running:
        total_frames += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Skip drawing if disabled
        if globals.enable_drawing:
            draw_roads(screen)
            for vehicle in vehicles:
                vehicle.draw_car(screen)
                vehicle.draw_end(screen)

        # Update vehicle movement
        for vehicle in vehicles:
            vehicle.move(vehicles, total_frames)

        # Check for collisions or all vehicles reaching their destination
        if car_crash(vehicles):
            with open("simulation_results.txt", "a") as file:
                file.write(f"{simulation_id}: Collision\n")
            running = False
            crash = True

        if every_vehicle_reached_end(vehicles):
            with open("simulation_results.txt", "a") as file:
                file.write(f"{simulation_id}: Successful\n")
            running = False

        if globals.enable_drawing:
            pygame.display.flip()
            clock.tick(globals.fps)

    # Analyze and log simulation time
    if not crash:
        analyze_simulation_time(vehicles, simulation_id, total_frames)

def ending_simulation(crash, reached):
    if crash:
        with open("simulation_results.txt", "a") as file:
            file.write(f"Collision detected\n")
        pygame.quit()
    
    if reached:
        with open("simulation_results.txt", "a") as file:
            file.write(f"Successful\n")
        pygame.quit()

def analyze_simulation_time(vehicles, simulation_id, total_frames):
    """Analyze vehicle simulation time and record results"""
    times = [vehicle.time_to_reach for vehicle in vehicles if vehicle.reached_destination and vehicle.time_to_reach is not None]

    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)

        # Write results to a file
        with open("simulation_time_analysis.txt", "a") as file:
            file.write(f"Simulation {simulation_id}:\n")
            file.write(f"  Average Time: {avg_time:.2f} frames\n")
            file.write(f"  Max Time: {max_time} frames\n")
            file.write(f"  Min Time: {min_time} frames\n")
        print(f"Simulation {simulation_id}: Time analysis recorded")
    # else:
    #     with open("simulation_time_analysis.txt", "a") as file:
    #         file.write(f"Simulation {simulation_id}: No vehicles reached destination.\n")
    #     print(f"Simulation {simulation_id}: No vehicles reached destination.")

if __name__ == "__main__":
    main(args.simulation_id)
