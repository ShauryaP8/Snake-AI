#snake_env.py

import pygame
import numpy as np
import random
from enum import Enum

#Game settings
GRID_SIZE = 20
CELL_SIZE = 20
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
FPS = 1000 #Speeds up training

class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        #Init snake and food
        self.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = Direction.RIGHT
        self.food = self._place_food()
        self.score = 0
        return self._get_state()
    
    def _place_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE-1), (random.randint(0, GRID_SIZE-1)))
            if food not in self.snake:
                return food
    
    def _get_state(self):
        #Simplified state [Danger left, straight, right, food_left, right, up, down]
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction.value

        #Check dangers
        danger_left = self._is_collision((head_x - dir_y, head_y - dir_x))
        danger_straight = self._is_collision((head_x + dir_x, head_y + dir_y))
        danger_right = self._is_collision((head_x + dir_y, head_y + dir_x))

        #Food direction
        food_x, food_y = self.food
        food_left = food_x < head_x
        food_right = food_x > head_x
        food_up = food_y < head_y
        food_down = food_y > head_y

        return np.array([danger_left, danger_straight, danger_right, food_left, food_right, food_up, food_down], dtype=int)
    
    def _is_collision(self, pos):
        x, y = pos
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True
        if pos in self.snake:
            return True
        return False
    
    def step(self, action):
        #Action: 0=straight, 1=left, 2=right (relative to the current direction)
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if action == 0: #No change
            new_dir = self.direction
        elif action == 1: # turns left
            new_dir = clock_wise[(idx - 1) % 4]
        elif action == 2: #turns right
            new_dir = clock_wise[(idx + 1) % 4]
        self.direction = new_dir

        #move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        #check collision
        if self._is_collision(new_head):
            return self._get_state(), -10, True #Game Over
        
        #Check food
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
            reward = 10
        else:
            self.snake.pop()
            reward = 0
        
        #Small penalty for time to encourage effecieny 
        reward -= 0.1

        return self._get_state(), reward, False
    
    def render(self):
        self.screen.fill((0,0,0))
        #Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0,255,0), (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
            #Draw food
            pygame.draw.rect(self.screen, (255,0,0), (self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
            pygame.display.flip()
            self.clock.tick(FPS)

