import pygame
import random
import sys
import os
import time

#Challenge: ChatGPT Generated Videogame
#Objective: learn how to interact with ChatGPT to make the best out of generative AI in code development.
#This simple videogame has been generated almost completely by ChatGPT3.5 with little human fixes when stuck in a error loop.



WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WHITE = (255, 255, 255)
RED = (255, 0, 0)

 
POWERUP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("ChatGPT-generated-game\powerup.png")), (50, 50))
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("ChatGPT-generated-game\music.mp3"))
pygame.mixer.music.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join("ChatGPT-generated-game\player", f"tile00{i}.png")), (30, 30)) for i in range(0, 10)]
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.lives = 3
        self.invulnerable = True
        self.invulnerable_timer = time.time() + 3
        self.powerup_active = False
        self.powerup_timer = 0


    def update(self, dx, dy):
        # Cycling through animation frames
        self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
        self.image = self.animation_frames[self.frame_index]

        if time.time() > self.invulnerable_timer:
            self.invulnerable = False

        if self.powerup_active and time.time() > self.powerup_timer:
            self.deactivate_powerup()
            
        
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.rect.height))
 
    def decrease_lives(self):
        self.lives -= 1

    def reset_position(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def activate_powerup(self):
        self.powerup_active = True
        self.powerup_timer = time.time() + 5  # Power-up lasts for 5 seconds
        self.animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join("ChatGPT-generated-game\player", f"tile00{i}.png")), (15, 15)) for i in range(0, 10)]
    
    def deactivate_powerup(self):
        self.powerup_active = False
        self.animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join("ChatGPT-generated-game\player", f"tile00{i}.png")), (30, 30)) for i in range(0, 10)]

    

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join("ChatGPT-generated-game\enemy", f"tile00{i}.png")), (60, 40)) for i in range(0, 6)]
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, WINDOW_HEIGHT - self.rect.height)
        self.speed = [random.choice([-2, 2]), random.choice([-2, 2])]

    def update(self, *args):
        # Cycling through animation frames
        self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
        self.image = self.animation_frames[self.frame_index]
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.speed[1] = -self.speed[1]
    
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = POWERUP_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, WINDOW_HEIGHT - self.rect.height)

def draw_lives_timer(screen, font, lives, timer):
    lives_text = font.render(f"Lives: {lives} - Timer: {timer}", True, WHITE)

    # Calculate the position to center the text horizontally
    text_width, text_height = font.size(f"Lives: {lives} - Time: {timer}")
    x_position = (screen.get_width() - text_width) // 2

    screen.blit(lives_text, (x_position, 10))


def draw_retry_button(screen, font):
    retry_text = font.render("Retry", True, WHITE)
    retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    pygame.draw.rect(screen, RED, retry_rect, border_radius=5)
    screen.blit(retry_text, retry_rect)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D Game")

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    retry_font = pygame.font.Font(None, 50)

    running = True
    retry_button = False
    i = 0
    frozen = False
    
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time_seconds = (current_time - start_time) // 1000

        
        clock.tick(20)
        if not retry_button:
            draw_lives_timer(screen, font, player.lives, elapsed_time_seconds)  # Pass the timer to draw_lives 
        if retry_button:
            if not frozen:
                frozen = True
                frozentime = elapsed_time_seconds
            
            draw_lives_timer(screen, font, player.lives, frozentime)   
            player.kill()
            for obstacle in obstacles:
                obstacle.kill()
            for powerup in powerups:
                powerup.kill()
            pygame.mixer.music.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and retry_button:
                # Riavvia il gioco cliccando su "Retry"
                start_time = pygame.time.get_ticks()
                i = 0
                current_time = 0
                frozen = False
                player = Player()
                all_sprites.add(player)
                player.lives = 3
                player.reset_position()
                for obstacle in obstacles:
                    obstacle.kill()
                for powerup in powerups:
                    powerup.kill()
                retry_button = False

        if i == 0:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
            i = 1
            for _ in range(20):
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)

            for _ in range(5):  # Add 5 power-ups
                powerup = Powerup()
                all_sprites.add(powerup)
                powerups.add(powerup)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

        all_sprites.update(dx, dy)
        obstacles.update()
        powerups.update()

        if not player.invulnerable and pygame.sprite.spritecollide(player, obstacles, False):
            player.decrease_lives()
            player.invulnerable = True
            player.invulnerable_timer = time.time() + 3

            if player.lives <= 0:
                retry_button = True

        # Check for collision with power-ups
        powerup_collisions = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_collisions:
            player.activate_powerup()

        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        obstacles.draw(screen)
        powerups.draw(screen)

      

        if retry_button:
            draw_retry_button(screen, retry_font)

    

    pygame.mixer.music.stop()

    pygame.quit()
    sys.exit("Game Over")

if __name__ == "__main__":
    main()
