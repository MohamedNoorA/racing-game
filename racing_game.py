import pygame
import random
import sys
from pathlib import Path
from game_manager import GameManager

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
GRASS_GREEN = (34, 139, 34)  # Forest Green for grass

# List of enemy car colors (RGB hex values)
ENEMY_COLORS = [
    "#0000FF",  # Blue
    "#00FF00",  # Green
    "#800080",  # Purple
    "#FFA500",  # Orange
    "#008080",  # Teal
]

# Create images directory if it doesn't exist
current_dir = Path.cwd()
images_dir = current_dir / "images"
images_dir.mkdir(exist_ok=True)

# Function to create and save SVG files
def save_svg_file(filename, svg_content):
    file_path = images_dir / filename
    with open(file_path, 'w') as f:
        f.write(svg_content)
    return file_path

# Red car SVG content
red_car_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 320">
  <!-- Car Body -->
  <path d="M60 80 L50 120 L50 260 L150 260 L150 120 L140 80 Z" fill="#FF0000" stroke="#000000" stroke-width="2"/>
  <!-- Windshield -->
  <path d="M70 100 L70 140 L130 140 L130 100 Z" fill="#87CEEB" stroke="#000000" stroke-width="2"/>
  <!-- Headlights -->
  <circle cx="70" cy="270" r="10" fill="#FFFF00" stroke="#000000" stroke-width="1"/>
  <circle cx="130" cy="270" r="10" fill="#FFFF00" stroke="#000000" stroke-width="1"/>
  <!-- Wheels -->
  <rect x="40" y="180" width="20" height="40" rx="5" fill="#000000"/>
  <rect x="140" y="180" width="20" height="40" rx="5" fill="#000000"/>
  <!-- Windows -->
  <path d="M60 140 L60 170 L140 170 L140 140 Z" fill="#87CEEB" stroke="#000000" stroke-width="1"/>
  <!-- Details -->
  <rect x="95" y="200" width="10" height="30" fill="#333333"/>
  <rect x="90" y="80" width="20" height="10" fill="#333333"/>
</svg>'''

# Function to generate enemy car SVG with different colors
def generate_enemy_car_svg(color):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 320">
  <!-- Car Body -->
  <path d="M60 80 L50 120 L50 260 L150 260 L150 120 L140 80 Z" fill="{color}" stroke="#000000" stroke-width="2"/>
  <!-- Windshield -->
  <path d="M70 100 L70 140 L130 140 L130 100 Z" fill="#87CEEB" stroke="#000000" stroke-width="2"/>
  <!-- Headlights -->
  <circle cx="70" cy="270" r="10" fill="#FFFFFF" stroke="#000000" stroke-width="1"/>
  <circle cx="130" cy="270" r="10" fill="#FFFFFF" stroke="#000000" stroke-width="1"/>
  <!-- Wheels -->
  <rect x="40" y="180" width="20" height="40" rx="5" fill="#000000"/>
  <rect x="140" y="180" width="20" height="40" rx="5" fill="#000000"/>
  <!-- Windows -->
  <path d="M60 140 L60 170 L140 170 L140 140 Z" fill="#87CEEB" stroke="#000000" stroke-width="1"/>
  <!-- Details -->
  <rect x="95" y="200" width="10" height="30" fill="#333333"/>
  <rect x="90" y="80" width="20" height="10" fill="#333333"/>
</svg>'''

# Save SVG files
red_car_path = save_svg_file("red_car.svg", red_car_svg)

# Save all enemy car colors
enemy_car_paths = []
enemy_car_surfaces = []
for i, color in enumerate(ENEMY_COLORS):
    enemy_svg = generate_enemy_car_svg(color)
    path = save_svg_file(f"enemy_car_{i}.svg", enemy_svg)
    enemy_car_paths.append(path)

# Helper function to load SVG as a pygame surface
def load_svg_as_surface(svg_path, size):
    try:
        # First try to use pygame's built-in image loading
        image = pygame.image.load(svg_path)
        return pygame.transform.scale(image, size)
    except pygame.error:
        # If that fails, create a simple colored rectangle as fallback
        surface = pygame.Surface(size, pygame.SRCALPHA)
        if "red" in str(svg_path):
            pygame.draw.rect(surface, RED, (0, 0, size[0], size[1]))
        else:
            # Use a default color for enemy cars based on the filename
            color_index = 0
            for i, color_name in enumerate(ENEMY_COLORS):
                if f"enemy_car_{i}" in str(svg_path):
                    color_index = i
                    break
            
            # Convert hex color to RGB
            color_hex = ENEMY_COLORS[color_index].lstrip('#')
            color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            
            pygame.draw.rect(surface, color_rgb, (0, 0, size[0], size[1]))
        
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, size[0], size[1]), 2)
        return surface

# Load player car image
try:
    player_car = load_svg_as_surface(red_car_path, (50, 80))
except Exception as e:
    print(f"Error loading player car image: {e}")
    # Create simple fallback car surface
    player_car = pygame.Surface((50, 80), pygame.SRCALPHA)
    pygame.draw.rect(player_car, RED, (0, 0, 50, 80))
    pygame.draw.rect(player_car, (0, 0, 0), (0, 0, 50, 80), 2)

# Load enemy car images
try:
    for path in enemy_car_paths:
        enemy_surface = load_svg_as_surface(path, (50, 80))
        enemy_car_surfaces.append(enemy_surface)
except Exception as e:
    print(f"Error loading enemy car images: {e}")
    # Create simple fallback car surfaces for each color
    for color_hex in ENEMY_COLORS:
        enemy_surface = pygame.Surface((50, 80), pygame.SRCALPHA)
        color_hex = color_hex.lstrip('#')
        color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        pygame.draw.rect(enemy_surface, color_rgb, (0, 0, 50, 80))
        pygame.draw.rect(enemy_surface, (0, 0, 0), (0, 0, 50, 80), 2)
        enemy_car_surfaces.append(enemy_surface)

# Road setup
road_x = WIDTH // 4
road_width = WIDTH // 2
lane_width = road_width // 3

# Initialize game manager
game_manager = GameManager()

# Initial speeds from level 0
current_speeds = game_manager.get_current_speeds()
player_speed = current_speeds["player_speed"]

# Player Car
player_x = road_x + lane_width * 1.5 - 25
player_y = HEIGHT - 100

# Fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 64)
menu_font = pygame.font.SysFont(None, 48)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Car class
class Car:
    def __init__(self, x, y, min_speed, max_speed):
        self.x = x
        self.y = y
        self.image_index = random.randint(0, len(enemy_car_surfaces) - 1)
        self.image = enemy_car_surfaces[self.image_index]
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed = random.randint(min_speed, max_speed)
        self.width = 50
        self.height = 80

    def move(self, min_speed, max_speed):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -100
            self.x = road_x + lane_width * (random.randint(0, 2) + 0.5) - 25
            self.min_speed = min_speed
            self.max_speed = max_speed
            self.speed = random.randint(min_speed, max_speed)
            # Change car color when it respawns
            self.image_index = random.randint(0, len(enemy_car_surfaces) - 1)
            self.image = enemy_car_surfaces[self.image_index]
            return True
        return False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Create enemy cars
def create_cars(min_speed, max_speed):
    return [Car(road_x + lane_width * (random.randint(0, 2) + 0.5) - 25, 
               random.randint(-HEIGHT, -100),
               min_speed, max_speed) for _ in range(3)]

cars = create_cars(
    current_speeds["enemy_min_speed"], 
    current_speeds["enemy_max_speed"]
)

# Collision detection
def check_collision(player_x, player_y, cars):
    player_rect = pygame.Rect(player_x, player_y, 50, 80)
    for car in cars:
        car_rect = car.get_rect()
        if player_rect.colliderect(car_rect):
            return True
    return False

# Reset game
def reset_game():
    global player_x, player_y, cars, game_state, player_speed
    
    game_manager.reset_game()
    current_speeds = game_manager.get_current_speeds()
    
    player_x = road_x + lane_width * 1.5 - 25
    player_y = HEIGHT - 100
    player_speed = current_speeds["player_speed"]
    
    cars = create_cars(
        current_speeds["enemy_min_speed"], 
        current_speeds["enemy_max_speed"]
    )
    
    game_state = PLAYING

# Draw grass pattern - added function to create more interesting grass
def draw_grass(x, width, height):
    # Base grass color
    pygame.draw.rect(screen, GRASS_GREEN, (x, 0, width, height))
    
    # Add some random grass tufts for texture
    for _ in range(100):
        tuft_x = random.randint(x, x + width - 5)
        tuft_y = random.randint(0, height - 5)
        tuft_height = random.randint(3, 8)
        # Slightly darker green for variation
        tuft_color = (random.randint(20, 30), random.randint(120, 150), random.randint(20, 30))
        pygame.draw.line(screen, tuft_color, (tuft_x, tuft_y + tuft_height), (tuft_x, tuft_y), 2)

# Draw menu screen
def draw_menu():
    screen.fill(WHITE)
    
    # Draw road and grass for background in menu
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))
    
    # Draw grass on both sides
    draw_grass(0, road_x, HEIGHT)
    draw_grass(road_x + road_width, WIDTH - (road_x + road_width), HEIGHT)
    
    # Semi-transparent overlay for menu text
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))
    screen.blit(overlay, (0, 0))
    
    # Title
    title_text = title_font.render("Racing Game", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    
    # High score
    high_score_text = font.render(f"High Score: {game_manager.high_score}", True, BLACK)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 200))
    
    # Menu options
    start_text = menu_font.render("Press SPACE to Start", True, GREEN)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 300))
    
    quit_text = font.render("Press Q to Quit", True, RED)
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 380))
    
    # Instructions
    instructions = [
        "Use LEFT and RIGHT arrows to move",
        "Avoid the enemy cars",
        "Score increases as you dodge cars",
        "Speed increases as your score goes up"
    ]
    
    y_pos = 450
    for instruction in instructions:
        instruction_text = font.render(instruction, True, BLACK)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, y_pos))
        y_pos += 30

# Draw game over screen
def draw_game_over():
    # Keep the game screen visible underneath
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Game over title
    game_over_text = title_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 150))
    
    # Score
    score_text = menu_font.render(f"Your Score: {game_manager.current_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
    
    # High score
    high_score_text = menu_font.render(f"High Score: {game_manager.high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 300))
    
    # Restart option
    restart_text = menu_font.render("Press R to Restart", True, GREEN)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 380))
    
    # Quit option
    quit_text = menu_font.render("Press Q to Quit", True, RED)
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 430))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            # Menu state controls
            if game_state == MENU:
                if event.key == pygame.K_SPACE:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
            
            # Game over state controls
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
    
    # Menu state
    if game_state == MENU:
        draw_menu()
    
    # Playing state
    elif game_state == PLAYING:
        # Control player car
        keys = pygame.key.get_pressed()

        # Move left and right (ensuring the car stays within lanes)
        if keys[pygame.K_LEFT] and player_x > road_x:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < road_x + road_width - 50:
            player_x += player_speed

        # Move up (ensure the car doesn't go above the screen)
        if keys[pygame.K_UP] and player_y > 50:
            player_y -= player_speed

        # Move down (ensure the car doesn't go below the screen)
        if keys[pygame.K_DOWN] and player_y < HEIGHT - 100:
            player_y += player_speed
            
        # Check for collision
        if check_collision(player_x, player_y, cars):
            game_manager.set_game_over()
            game_state = GAME_OVER
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw grass on both sides of the road
        draw_grass(0, road_x, HEIGHT)
        draw_grass(road_x + road_width, WIDTH - (road_x + road_width), HEIGHT)
        
        # Draw road
        pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))
        
        # Draw lane markings
        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, YELLOW, (road_x + lane_width - 5, i, 10, 20))
            pygame.draw.rect(screen, YELLOW, (road_x + lane_width * 2 - 5, i, 10, 20))
        
        # Get current speeds based on score
        current_speeds = game_manager.get_current_speeds()
        player_speed = current_speeds["player_speed"]
        
        # Move and draw cars
        for car in cars:
            if car.move(current_speeds["enemy_min_speed"], current_speeds["enemy_max_speed"]):
                # Update score when car is successfully avoided
                level = game_manager.update_score(game_manager.current_score + 1)
            car.draw()
        
        # Draw player car
        screen.blit(player_car, (player_x, player_y))
        
        # Display score and level
        score_text = font.render(f"Score: {game_manager.current_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        high_score_text = font.render(f"High Score: {game_manager.high_score}", True, BLACK)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))
        
        level_text = font.render(f"Level: {game_manager.current_level + 1}", True, BLACK)
        screen.blit(level_text, (10, 50))
        
        speed_text = font.render(f"Speed: {current_speeds['player_speed']}", True, BLACK)
        screen.blit(speed_text, (WIDTH - speed_text.get_width() - 10, 50))
    
    # Game over state
    elif game_state == GAME_OVER:
        draw_game_over()
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()