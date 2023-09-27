import importlib
import subprocess

# List of required modules
required_modules = [
    "pygame",
]

# Function to check if a module is installed
def is_module_installed(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

# Function to install a module using pip
def install_module(module_name):
    try:
        subprocess.check_call(["pip", "install", module_name])
        return True
    except subprocess.CalledProcessError:
        return False

# Check and install required modules
missing_modules = [module for module in required_modules if not is_module_installed(module)]

if missing_modules:
    print("Installing missing modules...")
    for module in missing_modules:
        if install_module(module):
            print(f"Successfully installed {module}")
        else:
            print(f"Failed to install {module}. Please install it manually.")
else:
    print("All required modules are already installed.")


import pygame
import os
import random
import time
import sys
import math

required_modules = ["pygame",]

def is_module_installed(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def install_module(module_name):
    try:
        subprocess.check_call(["pip", "install", module_name])
        return True
    except subprocess.CalledProcessError:
        return False

missing_modules = [module for module in required_modules if not is_module_installed(module)]

if missing_modules:
    print("Installing missing modules...")
    for module in missing_modules:
        if install_module(module):
            print(f"Successfully installed {module}")
        else:
            print(f"Failed to install {module}. Please install it manually.")
else:
    print("All required modules are already installed.")

pygame.init()
pygame.mixer.init()
font = pygame.font.Font(None, 36)

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Screen Saver")

image_dir = "images"
audio_dir = "audio"

image_filenames = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

current_image_index = 0
image_change_timer = time.time()

audio_filenames = [os.path.join(audio_dir, filename) for filename in os.listdir(audio_dir) if filename.endswith(('.mp3', '.wav', '.ogg'))]

current_audio_index = len(audio_filenames) - 1

def all_audio_played():
    return current_audio_index >= len(audio_filenames)

def play_audio():
    pygame.mixer.music.load(audio_filenames[current_audio_index])
    pygame.mixer.music.play()

class Raindrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def fall(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = random.randint(-100, -10)

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 1)

class Snowflake:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def fall(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y > screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, screen_width)

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 2)

class Blizzard:
    def __init__(self, x, y, speed_x):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.amplitude = random.randint(5, 40)
        self.angle = 0

    def fall(self):
        self.y += random.randint(10, 20)
        self.angle += 0.1
        self.x += self.speed_x
        self.x += self.amplitude * math.sin(self.angle)

        if self.y > screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, screen_width)

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)

class Special:
    def __init__(self, x, y, speed_x):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = random.uniform(2, 5)
        self.rotation = random.uniform(0, 360)
        self.size = random.randint(5, 20)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.angular_speed = random.uniform(-5, 5)

    def fall(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.rotation += self.angular_speed

        if self.y > screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, screen_width)

    def draw(self):
        rotated_image = pygame.transform.rotate(pygame.Surface((self.size, self.size), pygame.SRCALPHA), self.rotation)
        pygame.draw.rect(rotated_image, self.color, (0, 0, self.size, self.size))
        screen.blit(rotated_image, (self.x, self.y))

class Wave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 50)
        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(6)]

    def move(self):
        self.x += random.uniform(-2, 2)
        self.y += random.uniform(-2, 2)

    def draw(self):
        for i in range(6):
            angle = i * math.pi / 3
            x1 = self.x + self.radius * math.cos(angle)
            y1 = self.y + self.radius * math.sin(angle)
            x2 = self.x + self.radius * math.cos(angle + math.pi / 3)
            y2 = self.y + self.radius * math.sin(angle + math.pi / 3)
            pygame.draw.line(screen, self.colors[i], (x1, y1), (x2, y2), 5)

class Firework:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = screen_height
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-10, -5)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.size = random.randint(2, 4)
        self.exploded = False
        self.particles = []

    def update(self):
        if not self.exploded:
            self.x += self.speed_x
            self.y += self.speed_y

            if self.y <= screen_height // 3.5:
                self.explode()

        if self.exploded:
            for particle in self.particles:
                particle.update()
                if particle.life <= 0:
                    self.particles.remove(particle)

    def explode(self):
        self.exploded = True
        num_particles = random.randint(20, 50)
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            particle = Particle(self.x, self.y, angle, speed)
            self.particles.append(particle)

    def draw(self):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        else:
            for particle in self.particles:
                particle.draw()

class Particle:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.speed_x = speed * math.cos(angle)
        self.speed_y = speed * math.sin(angle)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.size = random.randint(2, 4)
        self.life = random.uniform(1, 3)
        self.alpha = 255

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 0.01
        self.alpha = int(self.life / 3 * 255)

    def draw(self):
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, self.color + (self.alpha,), (self.size, self.size), self.size)
        screen.blit(particle_surface, (int(self.x) - self.size, int(self.y) - self.size))

class Firefly:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(0, 50))
        self.size = random.randint(1, 3)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = 0

        if self.y < 0:
            self.y = screen_height
        elif self.y > screen_height:
            self.y = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

fireflies = []
raindrops = []
snowflakes = []
blizzards = []
specials = []
waves = []
fireworks = []

raindrop_speed = 8
raindrop_spawn_frequency = .95
snowflake_speed = 3
snowflake_spawn_frequency = 0.58
blizzard_speed = 10
special_spawn_frequency = 0.18
special_speed = 2
wave_spawn_frequency = 0.1

waiting_for_start = True
running = True
current_mode = "NONE"
mode_change_timer = time.time()

class TextDisplay:
    def __init__(self, text, font_size):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.text_color = (255, 255, 255)
        self.text_surfaces = []
        self.text_rects = []
        self.text_alpha = 255
        self.fade_speed = 1

    def render(self):
        max_line_length = 45  # Adjust the desired line length here
        words = self.text.split()
        lines = []
        current_line = []

        for word in words:
            if sum(len(word) for word in current_line) + len(current_line) + len(word) <= max_line_length:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            self.text_surfaces.append(text_surface)
            text_rect = text_surface.get_rect()
            self.text_rects.append(text_rect)

        total_height = sum([rect.height for rect in self.text_rects])
        current_y = (screen_height - total_height) // 2

        for i in range(len(self.text_surfaces)):
            self.text_rects[i].centerx = screen_width // 2
            self.text_rects[i].top = current_y
            current_y += self.text_rects[i].height

        self.text_alpha = 255

    def update(self):
        if self.text_alpha > 0:
            self.text_alpha -= self.fade_speed
            if self.text_alpha < 0:
                self.text_alpha = 0
            for text_surface in self.text_surfaces:
                text_surface.set_alpha(self.text_alpha)

    def draw(self):
        if self.text_alpha > 0:
            for i in range(len(self.text_surfaces)):
                screen.blit(self.text_surfaces[i], self.text_rects[i])


current_text_display = None
display_filename = False

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_start = False
            running = False
        elif event.type == pygame.KEYDOWN:
            waiting_for_start = False
            pygame.mixer.music.unpause()

    screen.fill((0, 0, 0))
    start_text = font.render("Press any key to start", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                current_image_index = (current_image_index - 1) % len(image_filenames)
                image_change_timer = time.time()
            elif event.key == pygame.K_RIGHT:
                current_image_index = (current_image_index + 1) % len(image_filenames)
                image_change_timer = time.time()

            elif event.key == pygame.K_UP:
                current_audio_index = (current_audio_index + 1) % len(audio_filenames)
                if not all_audio_played():
                    play_audio()
            elif event.key == pygame.K_DOWN:
                current_audio_index = (current_audio_index - 1) % len(audio_filenames)
                if not all_audio_played():
                    play_audio()
            
            # Toggle display_filename when 'f' key is pressed
            elif event.key == pygame.K_f:
                display_filename = not display_filename  # Toggle the state

    if len(image_filenames) > 0:
        if time.time() - image_change_timer > 15:
            current_image_index = (current_image_index + 1) % len(image_filenames)
            image_change_timer = time.time()
    else:
        print("No more images to display. Exiting program.")
        running = False

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(pygame.image.load(image_filenames[current_image_index]), (screen_width, screen_height)), (0, 0))

    if not pygame.mixer.music.get_busy():
        current_audio_index = (current_audio_index + 1) % len(audio_filenames)
        if current_audio_index == -1:
            print("All audio tracks played. Exiting program.")
            running = False
        else:
            play_audio()

    current_image_filename = os.path.basename(image_filenames[current_image_index]).upper()
    if 'RAIN' in current_image_filename:
        current_mode = "RAIN"
    elif 'SNOW' in current_image_filename:
        current_mode = "SNOW"
    elif 'BLIZZARD' in current_image_filename:
        current_mode = "BLIZZARD"
    elif 'SPECIAL' in current_image_filename:
        current_mode = "SPECIAL"
    elif 'WAVE' in current_image_filename:
        current_mode = "WAVE"
    elif 'FIREWORKS' in current_image_filename:
        current_mode = "FIREWORKS"
    elif 'FIREFLY' in current_image_filename:
        current_mode = "FIREFLY"
    else:
        current_mode = "NONE"

    if current_mode == "RAIN":
        if random.random() < raindrop_spawn_frequency:
            x = random.randint(0, screen_width)
            raindrop = Raindrop(x, 0, raindrop_speed)
            raindrops.append(raindrop)

        for raindrop in raindrops:
            raindrop.fall()
            raindrop.draw()
    elif current_mode == "SNOW":
        if random.random() < snowflake_spawn_frequency:
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(0.5, 1.5)
            snowflake = Snowflake(x, y, speed_x, speed_y)
            snowflakes.append(snowflake)

        for snowflake in snowflakes:
            snowflake.fall()
            snowflake.draw()
    elif current_mode == "BLIZZARD":
        if random.random() < raindrop_spawn_frequency:
            x = random.randint(0, screen_width)
            blizzard = Blizzard(x, 0, blizzard_speed)
            blizzards.append(blizzard)

        for blizzard in blizzards:
            blizzard.fall()
            blizzard.draw()
    elif current_mode == "SPECIAL":
        if random.random() < special_spawn_frequency:
            x = random.randint(0, screen_width)
            special = Special(x, 0, special_speed)
            specials.append(special)

        for special in specials:
            special.fall()
            special.draw()
    elif current_mode == "WAVE":
        if random.random() < wave_spawn_frequency:
            x = random.randint(100, screen_width - 100)
            y = random.randint(100, screen_height - 100)
            wave = Wave(x, y)
            waves.append(wave)

        for wave in waves:
            wave.move()
            wave.draw()
    elif current_mode == "FIREWORKS":
        if random.random() < 0.03:
            firework = Firework()
            fireworks.append(firework)

        for firework in fireworks:
            firework.update()
            firework.draw()

    elif current_mode == "FIREFLY":
        if len(fireflies) < 100:
            firefly = Firefly()
            fireflies.append(firefly)

        for firefly in fireflies:
            firefly.move()
            firefly.draw()

    current_image_filename = os.path.basename(image_filenames[current_image_index]).upper()
    if 'TEXT' in current_image_filename:
        filename_parts = current_image_filename.split(';')
        font_size = int(filename_parts[1])
        text = filename_parts[2].split('.')
        current_text_display = TextDisplay(text[0], font_size)
        current_text_display.render()

    if current_text_display is not None:
        current_text_display.update()
        current_text_display.draw()
    
    if display_filename:
        filename_text = os.path.basename(image_filenames[current_image_index])
        filename_surface = font.render(filename_text, True, (255, 255, 255))
        filename_rect = filename_surface.get_rect()
        filename_rect.bottomleft = (0, screen_height)
        screen.blit(filename_surface, filename_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
