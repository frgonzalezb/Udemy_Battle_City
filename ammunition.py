import pygame
import game_config as gc


class Bullet(pygame.sprite.Sprite):

    def __init__(
            self,
            assets,
            groups,
            owner,
            position,
            direction
            ) -> None:

        super().__init__()

        self.assets = assets
        self.group = groups

        # Groups for collision detection
        self.tanks = self.group['All_Tanks']
        self.bullet_group = self.group['Bullets']

        # Bullet position and direction
        self.pos_x, self.pos_y = position
        self.direction = direction

        # Bullet attributes
        self.owner = owner

        # Bullet images
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        # Add bullet to bullets group
        self.bullet_group.add(self)

    def update(self) -> None:
        # Bullet movement
        self.move()
        # Check if bullet has reached the edge of the screen
        self.collide_edge_of_screen()

    def draw(self, window) -> None:
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.RGB_GREEN, self.rect, 1)

    def move(self) -> None:
        """
        Moves the bullet in the direction indicated in the init method.
        """
        speed = gc.TANK_SPEED * 3

        if self.direction == 'Up':
            self.pos_y -= speed
        elif self.direction == 'Down':
            self.pos_y += speed
        elif self.direction == 'Left':
            self.pos_x -= speed
        elif self.direction == 'Right':
            self.pos_x += speed

        self.rect.center = (self.pos_x, self.pos_y)

    def collide_edge_of_screen(self) -> None:
        """
        Check for collision with screen edge.
        """
        if (
            self.rect.top <= gc.SCREEN_BORDER_TOP or
            self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or
            self.rect.left <= gc.SCREEN_BORDER_LEFT or
            self.rect.right >= gc.SCREEN_BORDER_RIGHT
        ):
            self.update_owner()
            self.kill()

    def update_owner(self) -> None:
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
