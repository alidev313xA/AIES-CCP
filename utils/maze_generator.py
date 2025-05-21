import random
import pygame

class Maze:
    def __init__(self, cols, rows, cell_size):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]  # Start with all walls
        # print(len(self.grid))

    # Prims Algorithm to generate a maze (then we added the multi path logic)
    def generate_maze(self):
        
        # 1. start with the grid full of walls
        visited = set()
        wall_list = []
        
        # Start cell in odd coordinates to avoid edge
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = 0
        
        # 2. Choose the random cell to start with, here we chose first cell 
        visited.add((start_x, start_y))

        # Add surrounding walls
        wall_list.extend(self.get_neighbors(start_x, start_y, is_wall=True))

        while wall_list: 
            wx, wy = random.choice(wall_list)

            # 3. Get cells on either side of the wall
            neighbors = self.get_adjacent_cells(wx, wy)
            if len(neighbors) == 2:
                c1, c2 = neighbors
                visited_count = sum([c in visited for c in neighbors])

                if visited_count == 1:
                    # Make wall a passage
                    self.grid[wy][wx] = 0

                    # Mark unvisited cell
                    next_cell = c1 if c1 not in visited else c2
                    nx, ny = next_cell
                    visited.add(next_cell)
                    self.grid[ny][nx] = 0

                    # Add new walls
                    for wall in self.get_neighbors(nx, ny, is_wall=True):
                        if wall not in wall_list:
                            wall_list.append(wall)
            wall_list.remove((wx, wy))
        self.add_multiple_paths(15)
        
    def add_multiple_paths(self, count=20):
        """ Randomly removes walls (not near start/end) to add more paths """
        margin = 4  # Distance margin from start & end
        added = 0
        while added < count:
            x = random.randint(margin, self.cols - margin - 1)
            y = random.randint(margin, self.rows - margin - 1)

            if self.grid[y][x] == 1:
                # Check if it's a wall with 2 opposite paths
                if self.has_path_on_both_sides(x, y):
                    self.grid[y][x] = 0
                    added += 1
        # exit            
        self.grid[self.rows - 2][self.cols - 1] = 0 
        

    def draw(self, screen, tile_img, maze_rect):
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * self.cell_size + maze_rect.x, y * self.cell_size + maze_rect.y, self.cell_size, self.cell_size)
                if self.grid[y][x] == 1:
                    screen.blit(tile_img, rect)  # Wall tile
                else:
                    pygame.draw.rect(screen, (30,30, 30), rect)  # Path (dark gray)
                    
    # ------------------ Helpers ------------------

    def get_neighbors(self, x, y, is_wall=False):
        """ Returns walls or paths 2 cells away in cardinal directions """
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if is_wall:
                    wall_x = x + dx // 2
                    wall_y = y + dy // 2
                    neighbors.append((wall_x, wall_y))
                else:
                    neighbors.append((nx, ny))
        return neighbors

    def get_adjacent_cells(self, x, y):
        """ Return the 2 cells split by wall at (x, y) """
        if x % 2 == 0:
            return [(x - 1, y), (x + 1, y)]
        else:
            return [(x, y - 1), (x, y + 1)]

    def has_path_on_both_sides(self, x, y):
        """ Check if wall has a path on both opposite sides """
        if x > 0 and x < self.cols - 1 and self.grid[y][x - 1] == 0 and self.grid[y][x + 1] == 0:
            return True
        if y > 0 and y < self.rows - 1 and self.grid[y - 1][x] == 0 and self.grid[y + 1][x] == 0:
            return True
        return False
    