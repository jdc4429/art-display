import importlib
import subprocess
import pygame
import os
import random
import time
import sys
import math
import cv2
import time; time.sleep(5)

required_modules = ["pygame","cv2",]

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

class PlayVideo:
    def __init__(self, video_dir):
        self.video_dir = video_dir
#        self.video_files = sorted([os.path.join(video_dir, filename) for filename in os.listdir(video_dir) if filename.endswith('.mp4')])
        self.video_files = sorted([os.path.join(video_dir, filename) for filename in os.listdir(video_dir) if filename.endswith(('.mp4', '.jpg'))])

        self.current_video_index = 0
        self.video_playing = False
        self.video_capture = None

    def play_next_video(self):
        if self.video_playing:
            return

        if self.current_video_index < len(self.video_files):
            self.video_playing = True
            self.load_and_play_video(self.video_files[self.current_video_index])
            self.current_video_index += 1
            if self.video_files[self.current_video_index - 1].lower().endswith('.jpg'):
                image_change_timer = time.time()
                self.video_playing = False

        else:
            self.current_video_index = 0
            print("All video files have been played.")
            # Handle what to do when all video files have been played

    def load_and_play_video(self, video_file):
        self.video_capture = cv2.VideoCapture(video_file)

    def update(self):
        if self.video_playing:
            if self.video_capture.isOpened():
                ret, frame = self.video_capture.read()
                if ret:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    frame = cv2.flip(frame, 0)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = pygame.surfarray.make_surface(frame)
                    frame = pygame.transform.scale(frame, (screen_width, screen_height))
                    screen.blit(frame, (0, 0))
                else:
                    self.video_playing = False
                    self.video_capture.release()
                    self.play_next_video()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    font = pygame.font.Font(None, 36)

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Art Display")

png_files = ""
image_dir = "images"
audio_dir = "audio"
video_dir = "images"  # Directory containing .mp4 video files

image_filenames = sorted([os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.mp4'))])

all_files = image_filenames

video_player = PlayVideo(video_dir)

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
        self.size = random.randint(1, 3)  # Vary the size of raindrops
        self.color = (200, 200, 200)  # White or silver reflecting color

    def fall(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = random.randint(-100, -10)
            self.size = random.randint(1, 3)  # Reset size when raindrop reaches the bottom

    def draw(self):
        # Draw raindrop as a white or silver ellipse
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.size, self.size))

class Snowflake:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load(os.path.join(png_files, "snowflake-16p-w.png")).convert_alpha()  # Replace "snowflake.png" with your snowflake image filename
        self.image = pygame.transform.scale(self.image, (random.randint(10, 20), random.randint(10, 20)))  # Vary the size of snowflakes
        self.angle = 0
        self.angular_speed = random.uniform(-0.1, 0.1)  # Add angular speed for rotation

    def fall(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += self.angular_speed  # Rotate the snowflake

        if self.y > screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, screen_width)

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image
        screen.blit(rotated_image, (self.x, self.y))

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


class LargeSnowflake:
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
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

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
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.angle = 0
        self.angular_speed = random.uniform(-0.1, 0.1)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += self.angular_speed  # Rotate the wave

        if self.x < -self.radius or self.x > screen_width + self.radius \
                or self.y < -self.radius or self.y > screen_height + self.radius:
            # Reset the wave if it goes off-screen
            self.x = random.randint(0, screen_width)
            self.y = random.randint(0, screen_height)
            self.radius = random.randint(10, 50)
            self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(6)]
            self.speed_x = random.uniform(-2, 2)
            self.speed_y = random.uniform(-2, 2)
            self.angle = 0
            self.angular_speed = random.uniform(-0.1, 0.1)

    def draw(self):
        for i in range(6):
            angle = i * math.pi / 3 + self.angle  # Apply rotation
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
        self.image = pygame.image.load(os.path.join(png_files, "firefly.png")).convert_alpha()
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)
        self.flicker_interval = random.uniform(0.1, 0.5)  # Adjust the flicker interval as desired
        self.flicker_timer = time.time()

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

    def flicker(self):
        current_time = time.time()
        if current_time - self.flicker_timer >= self.flicker_interval:
            self.flicker_timer = current_time
            self.image.set_alpha(random.randint(100, 255))  # Change the alpha value for flickering

    def draw(self):
        self.flicker()
        screen.blit(self.image, (int(self.x), int(self.y)))


class Bubble:
    def __init__(self, x, y, speed, size='17p'):
        self.size = size
        self.image = pygame.image.load(f'bubble-{self.size}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def rise(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.rect.top = screen_height

    def draw(self):
        screen.blit(self.image, self.rect)

class BUBBLEMAX:
    def __init__(self):
        self.bubbles = []
        self.bubble_spawn_frequency = {
            '17p': 0.2,
            '38p': 0.1,
            '75p': 0.05,
        }

        # Create large 75p bubbles
        for _ in range(5):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            bubble = Bubble(x, y, random.uniform(1, 3), size='75p')
            self.bubbles.append(bubble)

        # Create more 38p bubbles
        for _ in range(10):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            bubble = Bubble(x, y, random.uniform(1, 3), size='38p')
            self.bubbles.append(bubble)

        # Create lots of 17p bubbles
        for _ in range(30):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            bubble = Bubble(x, y, random.uniform(1, 3), size='17p')
            self.bubbles.append(bubble)

    def update(self):
        for bubble in self.bubbles:
            bubble.rise()

    def draw(self):
        for bubble in self.bubbles:
            bubble.draw()

class FIRE:
    def __init__(self):
        self.frame_duration = 50  # Adjust the duration between frames as needed
        self.last_frame_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.frames = []
        frame_dir = "fire_frames"  # Directory containing the frames

        # Load individual frames
        frame_files = [f for f in os.listdir(frame_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        frame_files.sort()  # Sort the frame files to ensure correct order
        for filename in frame_files:
            frame = pygame.image.load(os.path.join(frame_dir, filename)).convert_alpha()
            self.frames.append(frame)

        # Calculate the number of flame animations needed to cover the screen width
        num_animations = screen_width // self.frames[0].get_width() + 1
        self.animation_rects = []

        # Create multiple copies of the flame animation, placing them side by side
        for i in range(num_animations):
            animation_rect = self.frames[0].get_rect()
            animation_rect.midbottom = (i * animation_rect.width + animation_rect.width // 2, screen_height)
            self.animation_rects.append(animation_rect)

    def update(self):
        # Update the animation frame for each copy
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_frame_time = current_time

    def draw(self):
        # Draw the animated fire effect for each copy
        for animation_rect in self.animation_rects:
            screen.blit(self.frames[self.frame_index], animation_rect)

class STARFIELD:
    def __init__(self, num_stars):
        self.num_stars = num_stars
        self.stars = []
        self.star_image = pygame.image.load("star.png").convert_alpha()
        self.generate_stars()

    def generate_stars(self):
        center_x = screen_width // 2
        center_y = screen_height // 2
        for _ in range(self.num_stars):
            x = center_x
            y = center_y
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)  # Adjust the speed as needed
            self.stars.append((x, y, angle, speed))

    def update(self):
        for i in range(len(self.stars)):
            x, y, angle, speed = self.stars[i]
            x += speed * math.cos(angle)
            y += speed * math.sin(angle)
            if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
                # Reset the star if it goes off-screen
                x = screen_width // 2
                y = screen_height // 2
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 4)
            self.stars[i] = (x, y, angle, speed)

    def draw(self, screen):
        for x, y, _, _ in self.stars:
            size = random.randint(1, 3)
            star_image = pygame.transform.scale(self.star_image, (size, size))
            screen.blit(star_image, (int(x), int(y)))

class Heart:
    def __init__(self, x, speed, size='sml'):
        self.size = size
        self.image = pygame.image.load(f'heart-{self.size}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, 0)
        self.speed = speed
        self.amplitude = random.randint(5, 10)
        self.angle = 0

    def fall(self):
        self.rect.y += self.speed
        self.rect.x += self.amplitude * math.sin(self.angle)
        self.angle += random.uniform(-0.1, 0.1)

    def is_offscreen(self):
        return self.rect.y > screen_height

    def draw(self):
        screen.blit(self.image, self.rect)

class HEARTMAX:
    def __init__(self):
        self.hearts = []
        self.heart_spawn_frequency = {
            'sml': 0.2,
            'med': 0.1,
            'lrg': 0.05,
        }

        self.spawn_timer = time.time()

    def update(self):
        current_time = time.time()

        if current_time - self.spawn_timer >= random.uniform(0.1, 0.5):
            x = random.randint(0, screen_width)
            size = random.choice(['sml', 'med', 'lrg'])
            heart = Heart(x, random.uniform(1, 3), size)
            self.hearts.append(heart)
            self.spawn_timer = current_time

        for heart in self.hearts:
            heart.fall()

        # Remove hearts that are off-screen
        self.hearts = [heart for heart in self.hearts if not heart.is_offscreen()]

    def draw(self):
        for heart in self.hearts:
            heart.draw()

heartmax = HEARTMAX()
starfield = STARFIELD(100)
fire_border = FIRE()
bubblemax = BUBBLEMAX()
bubbles = []  # List to store bubble objects
bubble_spawn_frequency = 0.1  # Adjust the frequency of bubble spawn
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

# Added below lines to skip key press
waiting_for_start = False
pygame.mixer.music.unpause()

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_start = False
            running = False
        elif event.type == pygame.KEYDOWN:
            waiting_for_start = False
            pygame.mixer.music.unpause()

    screen.fill((0, 0, 0))
    #start_text = font.render("Press any key to start", True, (255, 255, 255))
    #start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    #screen.blit(start_text, start_text_rect)
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

    # Add code to remove any text on the screen
    current_text_display = None
    current_mode = "NONE"

    if len(image_filenames) > 0:
        current_image_filename = os.path.basename(image_filenames[current_image_index]).upper()
        if current_image_filename.lower().endswith('.mp4') and not video_player.video_playing:
            # If it's an MP4 video file and no video is currently playing, play the video.
            video_player.play_next_video()
        if video_player.video_playing:
            # If a video is currently playing, check if it has ended.
            if not video_player.video_capture.isOpened():
                video_player.video_playing = False
                video_player.video_capture.release()
                current_image_index = (current_image_index + 1) % len(image_filenames)
                image_change_timer = time.time()
        else:
            # If no video is playing, switch to the next image after 10 seconds.
            # Could also disable the timer in order to just run manually
            if time.time() - image_change_timer > 10:
                current_image_index = (current_image_index + 1) % len(image_filenames)
                image_change_timer = time.time()

    current_image_filename = os.path.basename(image_filenames[current_image_index]).upper()
    if current_image_filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # Display image file
        image = pygame.image.load(image_filenames[current_image_index])
        screen.blit(pygame.transform.scale(image, (screen_width, screen_height)), (0, 0))
    else:
        # Display video using your PlayVideo class
        video_player.update()

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
    elif 'HEXSPIN' in current_image_filename:
        current_mode = "HEXSPIN"
    elif 'FIREWORKS' in current_image_filename:
        current_mode = "FIREWORKS"
    elif 'FIREFLY' in current_image_filename:
        current_mode = "FIREFLY"
    elif 'FLAME' in current_image_filename:
        current_mode = "FLAME"
    elif 'BUBBLES' in current_image_filename:
        current_mode = "BUBBLES"
    elif 'BUBBLEMAX' in current_image_filename:
        current_mode = "BUBBLEMAX"
    elif 'HEARTMAX' in current_image_filename:
        current_mode = "HEARTMAX"
    elif 'STARFIELD' in current_image_filename:
        current_mode = "STARFIELD"
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
    elif current_mode == "HEXSPIN":
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

    if current_mode == "BUBBLES":
        if random.random() < bubble_spawn_frequency:
            x = random.randint(0, screen_width)
            bubble = Bubble(x, screen_height, random.uniform(1, 5))
            bubbles.append(bubble)

        for bubble in bubbles:
            bubble.rise()
            bubble.draw()

    if current_mode == "BUBBLEMAX":
        bubblemax.update()
        bubblemax.draw()

    if current_mode == "HEARTMAX":
        heartmax.update()
        heartmax.draw()


    if current_mode == "FLAME":
        fire_border.update()
        fire_border.draw()

    if current_mode == "STARFIELD":
        starfield.update()
        starfield.draw(screen)



    current_image_filename = os.path.basename(image_filenames[current_image_index]).upper()
    if current_image_filename.lower().endswith('.mp4'):
        video_player.play_next_video()
        video_player.update()

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
