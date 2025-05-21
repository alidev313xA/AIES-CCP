import pygame
import random
from collections import deque 

class Monster:
    def __init__(self, x, y, cell_size, image_path='assets/Monster/monster.png'):
        self.x, self.y = int(x), int(y)
        self.cell_size = cell_size
        self.load_image(image_path)
        self.rect = self.image.get_rect()
        
        # Movement properties
        self.move_progress = 0.0
        self.speeds = {
            "idle": 2.8,    # cells per second
            "alert": 3.3,
            "chase": 3.8,
            "frenzy": 4.8
        }
        self.state = "idle"
        self.path = []

    def load_image(self, path):
        """Load and scale monster image"""
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.cell_size - 1, self.cell_size - 1))
        except:
            # Fallback if image missing
            self.image = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
            self.image.fill((255, 0, 0))  # Red square

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def update_state(self, player_pos):
        distance = self.manhattan_distance((self.x, self.y), player_pos)
        if distance > 15: self.state = "idle"
        elif distance > 10: self.state = "alert"
        elif distance > 5: self.state = "chase"
        else: self.state = "frenzy"

    def update(self, maze, player_pos, delta_time):
        self.update_state(player_pos)
        
        if not self.path or self.manhattan_distance(self.path[-1], player_pos) > 3:
            self.path = self.bfs_path(maze, (self.x, self.y), player_pos)
        
        if self.path:
            target_x, target_y = self.path[0]
            if (self.x, self.y) == (target_x, target_y):
                self.path.pop(0)
                self.move_progress = 0.0
            else:
                self.move_progress += self.speeds[self.state] * delta_time
                if self.move_progress >= 1.0:
                    self.x, self.y = target_x, target_y
                    self.move_progress = 0.0

    def bfs_path(self, maze, start, target):
        queue= deque([start])
        visited = {start: None}
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        
        while queue:
            current = queue.popleft()
            if current == target: break
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < maze.cols and 0 <= ny < maze.rows 
                    and maze.grid[ny][nx] == 0 
                    and (nx, ny) not in visited):
                    visited[(nx, ny)] = current
                    queue.append((nx, ny))
        
        path = []
        if target in visited:
            current = target
            while current != start:
                path.append(current)
                current = visited[current]
            path.reverse()
        return path

    def draw(self, screen, maze_rect):
        if self.path and self.move_progress > 0:
            tx, ty = self.path[0]
            render_x = self.x + (tx - self.x) * self.move_progress
            render_y = self.y + (ty - self.y) * self.move_progress
        else:
            render_x, render_y = self.x, self.y
        
        screen.blit(
            self.image,
            (maze_rect.x + render_x * self.cell_size,
             maze_rect.y + render_y * self.cell_size)
        )