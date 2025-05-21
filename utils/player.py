import pygame

class Player:
    def __init__(self, x, y, cell_size, image_path='assets/Player/player_walk_1.png'):
        self.x, self.y = x, y   # Grid position
        self.cell_size = cell_size
        self.load_image(image_path)
        self.rect = self.image.get_rect()
        self.move_cooldown = 0  # Prevents multiple moves per key press
        self.move_delay = 0
        
    def load_image(self, path):
        """Load and scale player image"""
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.cell_size - 2, self.cell_size - 2))
        except:
            # Fallback if image missing
            self.image = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
            self.image.fill((0, 255, 0))  # Green square
    
    def handle_input(self, event, maze):
        """Call this in your event loop (not update())"""
        if event.type == pygame.KEYDOWN:
            if self.move_cooldown <= 0:
                moved = False
                if event.key == pygame.K_LEFT:
                    moved = self._try_move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    moved = self._try_move(1, 0, maze)
                elif event.key == pygame.K_UP:
                    moved = self._try_move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    moved = self._try_move(0, 1, maze)
                
                if moved:
                    self.move_cooldown = self.move_delay
    
    def update(self, dt):
        """Call this every frame"""
        if self.move_cooldown > 0:
            self.move_cooldown -= dt

    def _try_move(self, dx, dy, maze):
        """Validate and execute movement"""
        new_x, new_y = self.x + dx, self.y + dy
        if (0 <= new_x < maze.cols and 
            0 <= new_y < maze.rows and 
            maze.grid[new_y][new_x] == 0):
            self.x, self.y = new_x, new_y
            return True
        return False
    
    def draw(self, screen, maze_rect):
        """Draw player at grid position with padding"""
        screen_x = maze_rect.x + self.x * self.cell_size + 1
        screen_y = maze_rect.y + self.y * self.cell_size + 1
        screen.blit(self.image, (screen_x, screen_y))
