import pygame
import random
import math
import time
from pygame import mixer

from utils.maze_generator import Maze
from utils.player import Player
from utils.monster import Monster
    
class Game:
    def __init__(self):
        pygame.init()
        mixer.init()  # Initialize sound mixer
         
         # Text system setup
        self.BG_COLOR = (30, 30, 50)  # Dark blue background
        self.TEXT_COLOR = (255, 215, 0)  # Gold text
        self.font_large = pygame.font.SysFont('Orbitron', 60)
        self.font_medium = pygame.font.SysFont('Orbitron', 40) 
        self.font_small = pygame.font.SysFont('Orbitron', 20)
        self.final_time = 0
            
        # Screen setup
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 700    
        self.CELL_SIZE = 20
        self.MAZE_HEIGHT = 600
        self.MAZE_WIDTH =  600
        self.MAZE_COLS = (self.MAZE_WIDTH + self.CELL_SIZE)  // self.CELL_SIZE  # 800 / 20 = 40 cols
        self.MAZE_ROWS = (self.MAZE_HEIGHT + self.CELL_SIZE) // self.CELL_SIZE  # 600 / 20 = 30 rows
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.maze_rect = pygame.Rect(0, 0, self.MAZE_WIDTH, self.MAZE_HEIGHT)
        self.maze_rect.center = (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)
        self.tile_img = pygame.image.load('assets/tiles/tiles_1.png').convert_alpha()
        self.tile_img = pygame.transform.scale(self.tile_img, (self.CELL_SIZE, self.CELL_SIZE))
        self.last_frame_time = time.time()
        self.DEBUG_MODE = False  # Set to True to see collision boxes
            
        pygame.display.set_caption("Maze Escape: Monster Chase")
        
        # Game states
        self.state = "menu"  # menu -> loading -> gameplay -> gameover
        self.game_result = None  # "escaped" or "caught"
        
        # Resources
        self.font_large = pygame.font.SysFont("Arial", 60)
        self.font_medium = pygame.font.SysFont("Arial", 30)
        self.font_small = pygame.font.SysFont("Arial", 20)
        
        # Sound placeholders
        self.sounds = {
            "bg_music": 'sounds/music.wav',
            "growl": None,     # "assets/sounds/growl.wav"
            "scream": None,     # "assets/sounds/scream.wav"
            "win": None         # "assets/sounds/win.wav"
        }
        
        # Game tips
        self.tips = [
            "Monsters get faster the closer you are!",
            "Check your path before moving!",
            "The exit is always in the bottom-right corner",
            "Quick escapes give better scores!"
        ]
        
        # Game elements (initialized later)
        self.player =  Player(1, 1, self.CELL_SIZE)  # Start position (1,1)
        self.monster = Monster( x=random.randint(3, self.MAZE_COLS-2), y=random.randint(3, self.MAZE_ROWS-2), cell_size = self.CELL_SIZE)
        self.maze = Maze(self.MAZE_COLS, self.MAZE_ROWS, self.CELL_SIZE)
        self.start_time = 0
    
    
    
    def load_image(self, path, size=None):
        """Load and optionally scale an image"""
        try:
            img = pygame.image.load('assets/Player/player_walk_1.png').convert_alpha()
            return pygame.transform.scale(img, (size, size)) if size else img
        except:
            # Fallback colored square
            surf = pygame.Surface((size, size)) if size else pygame.Surface((50, 50))
            surf.fill((255, 0, 255))  # Magenta = missing asset
            return surf    
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60)/1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                     self.player.handle_input(event, self.maze)
                            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu" and self.play_button.collidepoint(event.pos):
                        self.state = "loading"
                        self.loading_progress = 0
                        self.loading_tip = random.choice(self.tips)
                        self.loading_start_time = time.time()
                    
                    elif self.state == "gameover" and self.restart_button.collidepoint(event.pos):
                        self.reset_game()
            
            # Updates
            self.player.update(dt)
            self.monster.update(self.maze, (self.player.x, self.player.y), dt)
                
            # State updates
            if self.state == "menu":
                self.update_menu()
            elif self.state == "loading":
                self.update_loading()
            elif self.state == "gameplay":
                self.update_gameplay()
            elif self.state == "gameover":
                self.update_gameover()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

    # --- State Methods ---
    def update_menu(self):
        """Main menu screen"""
        self.screen.fill((30, 30, 50))
        
        # Title
        title = self.font_large.render("Monster-Maze AI Game", True, (255, 215, 0))
        self.screen.blit(title, (self.SCREEN_WIDTH//2 - title.get_width()//2, 200))
        
        # Play button
        self.play_button = pygame.Rect(0, 0, 200, 60)
        self.play_button.center = (self.SCREEN_WIDTH//2, 400)
        pygame.draw.rect(self.screen, (0, 180, 0), self.play_button, border_radius=10)
        play_text = self.font_medium.render("PLAY", True, (255, 255, 255))
        self.screen.blit(play_text, (self.play_button.centerx - play_text.get_width()//2, 
                                    self.play_button.centery - play_text.get_height()//2))

    def update_loading(self):
        """Loading screen with progress bar"""
        self.screen.fill((20, 20, 40))
        
        # Update progress (0-100 over 3 seconds)
        elapsed = time.time() - self.loading_start_time
        self.loading_progress = min(100, int(elapsed / 2 * 100))
        
        # Progress bar
        bar_width = 200
        pygame.draw.rect(self.screen, (50, 50, 70), (self.SCREEN_WIDTH//2 - bar_width//2, 300, bar_width, 30))
        pygame.draw.rect(self.screen, (0, 200, 100), (self.SCREEN_WIDTH//2 - bar_width//2, 300, bar_width * self.loading_progress//100, 30))
        
        # Progress text
        progress_text = self.font_small.render(f"{self.loading_progress}%", True, (255, 255, 255))
        self.screen.blit(progress_text, (self.SCREEN_WIDTH//2 - progress_text.get_width()//2, 340))
        
        # Random tip
        tip_text = self.font_small.render(self.loading_tip, True, (200, 200, 200))
        self.screen.blit(tip_text, (self.SCREEN_WIDTH//2 - tip_text.get_width()//2, 400))
        
        # Complete loading
        if self.loading_progress >= 100:
            self.initialize_game()
            self.state = "gameplay"
            self.start_time = time.time()
            # Play BG music if available
            if self.sounds["bg_music"]:
                mixer.music.load(self.sounds["bg_music"])
                mixer.music.play(-1)  # Loop indefinitely

    def update_gameplay(self):
        """Main game screen with all gameplay logic"""
        
        # Calculate delta time properly
        current_time = time.time()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Update monster (chase logic)
        self.monster.update(self.maze, (self.player.x, self.player.y), delta_time)
        
        # Draw everything
        self.maze.draw(self.screen, self.tile_img, self.maze_rect)
        self.player.draw(self.screen, self.maze_rect)
        self.monster.draw(self.screen, self.maze_rect)
        # Display timer (centered above maze)
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        # Create timer text
        timer_text = self.font_medium.render(
            f"TIME: {minutes:02d}:{seconds:02d}", 
            True, 
            (255, 255, 255)  # White text
        )

        # Calculate centered position
        timer_x = self.maze_rect.centerx - timer_text.get_width() // 2
        timer_y = self.maze_rect.top - 40  # 40 pixels above maze

        # Draw with background for readability
        pygame.draw.rect(
            self.screen, 
            (255, 255, 255),  # Same as maze bg
            (timer_x - 10, timer_y - 5, 
            timer_text.get_width() + 20, 
            timer_text.get_height() + 10)
        )
        self.screen.blit(timer_text, (timer_x, timer_y))
                                        
        # Collision detection (using Rect)
        player_rect = pygame.Rect(
            self.maze_rect.x + self.player.x * self.CELL_SIZE,
            self.maze_rect.y + self.player.y * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE
        )
        
        monster_rect = pygame.Rect(
            self.maze_rect.x + self.monster.x * self.CELL_SIZE,
            self.maze_rect.y + self.monster.y * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE
        )
        
        # Check collisions
        if player_rect.colliderect(monster_rect):
            if self.sounds["scream"]:
                self.sounds["scream"].play()
            self.end_game("caught")
        
        # Win condition (reached exit)
        elif (self.player.x, self.player.y) == (self.maze.cols-1, self.maze.rows-2):
            self.final_time = time.time() - self.start_time
            if self.sounds["win"]:
                self.sounds["win"].play()
            self.end_game("escaped")
        
        # Optional: Visual debug for collision boxes
        if self.DEBUG_MODE:
            pygame.draw.rect(self.screen, (255, 0, 0), player_rect, 1)
            pygame.draw.rect(self.screen, (0, 0, 255), monster_rect, 1)

    def update_gameover(self):
        """Game over screen (win/lose)"""
        self.screen.fill((0, 0, 30))
        
        # Result message
        if self.game_result == "escaped":
            msg = self.font_large.render("ESCAPE SUCCESS!", True, (0, 255, 0))
            sub_msg = self.font_medium.render("Can you beat your time?", True, (200, 255, 200))
            # Play win sound if available
            if self.sounds["win"]:
                mixer.Sound.play(self.sounds["win"])
        else:
            msg = self.font_large.render("YOU WERE CAUGHT!", True, (255, 0, 0))
            sub_msg = self.font_medium.render("The monster got you...", True, (255, 200, 200))
            # Play scream sound if available
            if self.sounds["scream"]:
                mixer.Sound.play(self.sounds["scream"])
            
        self.screen.blit(msg, (self.SCREEN_WIDTH//2 - msg.get_width()//2, 200))
        self.screen.blit(sub_msg, (self.SCREEN_WIDTH//2 - sub_msg.get_width()//2, 280))
        
        if self.game_result == "escaped":
            minutes = int(self.final_time) // 60
            seconds = int(self.final_time) % 60
            time_text = self.font_medium.render(
                f"Escaped in: {minutes:02d}:{seconds:02d}",  # Formatted time
                True, 
                (255, 255, 0)
            )
            self.screen.blit(time_text, (self.SCREEN_WIDTH//2 - time_text.get_width()//2, 350))
                    
        # Restart button
        self.restart_button = pygame.Rect(0, 0, 200, 60)
        self.restart_button.center = (self.SCREEN_WIDTH//2, 450)
        pygame.draw.rect(self.screen, (0, 150, 200), self.restart_button, border_radius=10)
        restart_text = self.font_medium.render("RESTART", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.restart_button.centerx - restart_text.get_width() // 2, 
                                       self.restart_button.centery - restart_text.get_height() // 2))
        minutes = int(time.time()) // 60
        seconds = int(time.time()) % 60
       
       
    # --- Game Logic ---
    def initialize_game(self):
        """Initialize game objects"""
        self.start_time = time.time()
        self.maze = Maze(self.MAZE_COLS, self.MAZE_ROWS, self.CELL_SIZE)
        self.maze.generate_maze()
        
        # Place player at start (1,1)
        self.player = Player(1, 1, self.CELL_SIZE)
        
        # Place monster randomly
        monster_x, monster_y = random.randint(3, self.MAZE_COLS - 2), random.randint(3, self.MAZE_ROWS - 2)
        while self.maze.grid[monster_y][monster_x] == 1 or math.hypot(monster_x - 1, monster_y - 1) < 10:
            monster_x, monster_y = random.randint(3, self.MAZE_COLS - 2), random.randint(3, self.MAZE_ROWS - 2)

        self.monster = Monster(monster_x, monster_y, self.CELL_SIZE)
        
        # Play growl sound if available
        if self.sounds["growl"]:
            mixer.Sound.play(self.sounds["growl"])

    def end_game(self, result):
        """Transition to game over screen"""
        self.state = "gameover"
        self.game_result = result
        mixer.music.stop()  # Stop background music

    def reset_game(self):
        """Reset game state"""
        self.start_time = time.time()
        self.state = "menu"
        self.game_result = None
        