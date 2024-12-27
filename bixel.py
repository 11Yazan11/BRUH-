import pygame

class Bixel:
    def __init__(self, game, x, y, color, deadly=False):
        """Color is a tuple or list or rgb value only."""
        self.size = 40
        self.game = game
        self.color = color
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.deadly = deadly

    def update(self, relative_rect):
        pygame.draw.rect(self.game.wn, self.color, relative_rect)
        pygame.draw.rect(self.game.wn, self.darken_color(self.color), relative_rect, 4)
        pygame.draw.rect(self.game.wn, self.brigthen_color(self.color), relative_rect, 2)


    def brigthen_color(self, color):
        """Brightens the given RGB color by increasing its values, clamped to a maximum of 255."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Increase each component by a fixed value, clamped to a maximum of 255
        brightened_color = tuple(min(c + 50, 255) for c in color)
        return brightened_color
    
    def darken_color(self, color):
        """Darkens the given RGB color by increasing its values, clamped to a minimum of 0."""
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError("Color must be a tuple or list with three elements representing RGB values.")
    
        # Decrease each component by a fixed value, clamped to a minimum of 0
        darkened_color = tuple(max(c - 50, 0) for c in color)
        return darkened_color



    def handle_event(self, event):
        pass

    def destroy(self):
        pass
