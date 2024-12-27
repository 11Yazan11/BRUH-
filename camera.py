import pygame
class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera = pygame.Rect(0, 0, width, height)
        self.world_width = game.wnx*4  # Width of the game world
        self.world_height = game.wny+100   # Height of the game world

    def apply(self, entity, rect=False):
        """Adjust an entity's position relative to the camera."""
        return entity.rect.move(self.camera.topleft) if not rect else entity.move(self.camera.topleft)

    def update(self, target):
        """Center the camera on the target, while clamping to the map."""
        # Define a dead zone rectangle
        dead_zone_width = self.game.wnx // 2  # Width of the dead zone
        dead_zone_height = 50  # Height of the dead zone
        dead_zone = pygame.Rect(
            self.game.wnx // 2 - dead_zone_width // 2,  # Center horizontally
            320,  # Dead zone starts at y=320
            dead_zone_width,
            dead_zone_height,
        )

        # Get the player's position relative to the camera
        player_screen_x = target.rect.centerx + self.camera.x
        player_screen_y = target.rect.centery 

        # Adjust camera position horizontally if the player moves outside the dead zone
        if player_screen_x < dead_zone.left:
            self.camera.x += dead_zone.left - player_screen_x
        elif player_screen_x > dead_zone.right:
            self.camera.x += dead_zone.right - player_screen_x

        if player_screen_y < 320:  # Player visually "rises above" 400
                self.camera.y += dead_zone.top - player_screen_y

        # Clamp the camera so it doesn't go outside the map
        self.camera.x = max(-(self.world_width - self.game.wnx), min(0, self.camera.x))
        self.camera.y = self.camera.y/2


