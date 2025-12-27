import pygame
from pprint import pprint
from math import ceil


def hex_to_rgb(hex):
    return tuple(int(hex.strip("#")[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
  return ('#' + '{:02X}' * 3).format(r, g, b)

def get_gradient_steps(c1_center:list, c2_center:list, step_size:float) -> int:
    x_diff = abs(c1_center[0] - c2_center[0])
    y_diff = abs(c1_center[1] - c2_center[1])
    steps_horizontal = ceil(x_diff / step_size)
    steps_vertical = ceil(y_diff / step_size)
    return steps_horizontal + steps_vertical

def get_1d_gradient_map(color_1:tuple, color_2:tuple, max_steps:int) -> dict:
    color_diff = tuple(left - right for left, right in zip(color_1, color_2))
    step_diff = tuple((diff/max_steps for diff in color_diff))
    
    gradient = {}
    for distance in range(max_steps):
        gradient[f"{distance},{max_steps-distance}"] = tuple(int(color_1[j] - (distance * step_diff[j])) for j in range(3))
    return gradient

def get_2d_gradient_map(color_1:tuple, color_2:tuple, max_steps:int) -> dict:
    gradient_map = {}
    for c1_dist in range(max_steps):
        for c2_dist in range(max_steps):
            if c1_dist == 0:
                c1_weight = 1
                c2_weight = 0
            elif c2_dist == 0:
                c1_weight = 0
                c2_weight = 1
            else:
                # total_dist = c1_dist + c2_dist
                # c1_weight = c2_dist / total_dist
                # c2_weight = c1_dist / total_dist
                c1_weight = c2_dist / c1_dist
                c2_weight = c1_dist / c2_dist
            print(f"{c1_dist} | {c2_dist} --> {c1_weight} / {c2_weight}")
            color_values = []
            for i in range(3):
                val = (color_1[i] * c1_weight + color_2[i] * c2_weight) / (c1_weight + c2_weight)
                # if total_distance > distance_steps:
                #     val *= (1 - ((total_distance - distance_steps) / max_steps))
                pos_val = max(0, val)
                color_values.append(int(pos_val))
            
            gradient_map[f"{c1_dist},{c2_dist}"] = tuple(color_values)
    return gradient_map

# def get_2d_gradient_map(color_1:tuple, color_2:tuple, distance_steps:int, max_steps:int) -> dict:
#     gradient_map = {}
#     for c1_dist in range(max_steps):
#         c1_weight = max_steps - c1_dist
#         for c2_dist in range(max_steps):
#             color_values = []
#             total_distance = c1_dist + c2_dist
#             c2_weight = max_steps - c2_dist
#             for i in range(3):
#                 val = (color_1[i] * c1_weight + color_2[i] * c2_weight) / (c1_weight + c2_weight)
#                 if total_distance > distance_steps:
#                     val *= (1 - ((total_distance - distance_steps) / max_steps))
#                 pos_val = max(0, val)
#                 color_values.append(int(pos_val))
            
#             gradient_map[f"{c1_dist},{c2_dist}"] = tuple(color_values)
#     return gradient_map

def distance_from_centers(c1_center:list, c2_center:list, point:list, step_size:float) -> tuple[int,int]:
    dist_c1 = ceil(abs(c1_center[0] - point[0]) / step_size) + ceil(abs(c1_center[1] - point[1]) / step_size)
    dist_c2 = ceil(abs(c2_center[0] - point[0]) / step_size) + ceil(abs(c2_center[1] - point[1]) / step_size)
    return (dist_c1, dist_c2)

def steps_from_centers(c1_center:list[int], c2_center:list[int], step_size:float, row:int, col:int):
    steps_x_c1 = (c1_center[0] - step_size*col) ** 2
    steps_y_c1 = (c1_center[1] - step_size*row) ** 2 
    steps_c1 = int((steps_x_c1 + steps_y_c1)**(1/2) / step_size)
    # steps_c1 = int((steps_x_c1**2 + steps_y_c1**2)**0.5)
    steps_x_c2 = (c2_center[0] - step_size*(col + 1)) ** 2
    steps_y_c2 = (c2_center[1] - step_size*(row + 1)) ** 2
    steps_c2 = int((steps_x_c2 + steps_y_c2)**(1/2) / step_size)
    # steps_c2 = int((steps_x_c2**2 + steps_y_c2**2)**0.5)
    return (steps_c1, steps_c2)

if __name__ == "__main__":
    WIDTH = 600
    HEIGHT = 600
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Pygame Window")

    COLOR_1 = hex_to_rgb("#720353")
    # COLOR_2 = hex_to_rgb("#000000")
    COLOR_2 = hex_to_rgb("#0654B9")
    GRADIENT_DIM = 10
    MAX_STEPS = GRADIENT_DIM * 2
    SQUARE_SIZE = min(WIDTH, HEIGHT) / GRADIENT_DIM
    
    c1_center = [0,0]
    # c1_center = [400,300]
    c2_center = [WIDTH, HEIGHT]
    
    gradient_steps = get_gradient_steps(c1_center, c2_center, SQUARE_SIZE)
    gradient_map_1d = get_1d_gradient_map(COLOR_1, COLOR_2, MAX_STEPS)
    gradient_map_2d = get_2d_gradient_map(COLOR_1, COLOR_2, MAX_STEPS)
    
    # pprint(gradient_map_1d)
    # print()
    # pprint(gradient_map_2d)
    # exit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    c1_center = list(event.pos)
                elif event.button == 3:  # Right click  
                    c2_center = list(event.pos)
                else:
                    continue
                gradient_steps = get_gradient_steps(c1_center, c2_center, SQUARE_SIZE)
                gradient_map_1d = get_1d_gradient_map(COLOR_1, COLOR_2, gradient_steps)
                gradient_map_2d = get_2d_gradient_map(COLOR_1, COLOR_2, MAX_STEPS)

        screen.fill((0, 0, 0))  # Fill the screen with black
        
        for row in range(GRADIENT_DIM):
            for col in range(GRADIENT_DIM):
                rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE)
                
                # pygame.draw.rect(screen, gradient_map_1d[f"{row + col},{MAX_STEPS-row-col}"], rect)
                
                dist = steps_from_centers(c1_center, c2_center, SQUARE_SIZE, row, col)
                pygame.draw.rect(screen, gradient_map_2d[f"{dist[0]},{dist[1]}"], rect)
                
                # print(f"{row} | {col} --> {dist}")
        
        pygame.display.flip()
    pygame.quit()