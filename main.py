import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shield import Shield


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    shields = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Shield.containers = (shields, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    

    dt = 0

    score = 0
    last_shield_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        for obj in updatable:
            obj.update(dt)

        
        for obj in drawable:
            obj.draw(screen)    

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                print(f"Score: {score}")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 1


                # After your existing collision checks
        for shield in shields:
            for asteroid in asteroids:
                if asteroid.collides_with(shield):
                    asteroid.kill()  # Destroy asteroid completely (no split)
                    shield.tier -= 1  # Decrease shield tier
                    if shield.tier <= 0:  # Only kill shield if at lowest tier
                        shield.kill()
                    break


        if score > 0 and score % 100 == 0 and score != last_shield_score:
             # Create new shield or upgrade existing one
            if not shields:  # if no shield exists yet
                shield = Shield(player.position.x, player.position.y)
                shield.active = True
            else:
                for shield in shields:
                    shield.tier += 1  # Upgrade existing shield
            if shield.tier > 3:  # Optional: cap at tier 3
                shield.tier = 3
            last_shield_score = score  # Update the last_shield_score

        # Update shield position in a separate loop
        for shield in shields:
            shield.position = player.position

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
