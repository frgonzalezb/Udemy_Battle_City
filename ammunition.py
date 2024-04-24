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
        self.tank_group = self.group['all_tanks']
        self.bullet_group = self.group['bullets']

        # Bullet position and direction
        self.pos_x, self.pos_y = position
        self.direction = direction

        # Bullet attributes
        self.owner = owner

        # Bullet images
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        # Get bullet mask
        self.mask = pygame.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface()

        # Add bullet to bullets group
        self.bullet_group.add(self)

    def update(self) -> None:
        # Bullet movement
        self.move()
        # Check if bullet has reached the edge of the screen
        self.check_bullet_on_screen_border_collision()
        # Check for bullet collision with tank
        self.check_bullet_on_tank_collision()
        # Check for bullet collision between bullets
        self.check_bullet_on_bullet_collision()
        # Check for bullet collision with destructable tile
        self.check_bullet_on_obstacle_collision()

    def draw(self, window) -> None:
        window.blit(self.image, self.rect)
        # window.blit(self.mask_image, self.rect)
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

    def check_bullet_on_screen_border_collision(self) -> None:
        """
        Checks for collision with screen border.
        """
        if (
            self.rect.top <= gc.SCREEN_BORDER_TOP or
            self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or
            self.rect.left <= gc.SCREEN_BORDER_LEFT or
            self.rect.right >= gc.SCREEN_BORDER_RIGHT
        ):
            self.update_owner()
            self.kill()

    def check_bullet_on_tank_collision(self) -> None:
        """
        Checks if the bullet collides with a tank.
        """
        tank_collisions = pygame.sprite.spritecollide(
            self,
            self.tank_group,
            False
        )

        for tank in tank_collisions:
            if self.owner == tank or tank.is_spawning:
                continue
            if pygame.sprite.collide_mask(self, tank):
                # Player tank bullet collided with another player tank!
                if not self.owner.is_enemy and not tank.is_enemy:
                    self.update_owner()
                    tank.paralyze_tank(gc.TANK_PARALYSIS)
                    self.kill()
                    break
                # Player bullet has collided with enemy tank
                if (
                    (not self.owner.is_enemy and tank.is_enemy) or
                    (self.owner.is_enemy and not tank.is_enemy)
                ):
                    self.update_owner()
                    if not self.owner.is_enemy:
                        self.owner.scores.append(
                            gc.TANK_CRITERIA[tank.level]['score']
                        )
                        print(self.owner.scores)  # dbg
                    tank.destroy_tank()
                    self.kill()
                    break

    def check_bullet_on_bullet_collision(self) -> None:
        """
        Check for collisions with other bullets and destroy self once
        detected.
        """
        bullet_hit = pygame.sprite.spritecollide(
            self,
            self.bullet_group,
            False
        )

        if len(bullet_hit) == 1:
            return

        for bullet in bullet_hit:
            if bullet == self:
                continue
            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break

    def check_bullet_on_obstacle_collision(self):
        obstacle_collision = pygame.sprite.spritecollide(
            self,
            self.group['destructable_tiles'],
            False
        )
        for obstacle in obstacle_collision:
            obstacle.handle_bullet_hit(self)

    def update_owner(self) -> None:
        """
        Checks and updates the fire rate for tanks. As in the original
        game, each tank should shoot just one bullet at a time.
        """
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1
