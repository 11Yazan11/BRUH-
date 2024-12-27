import pygame

class Teleporter:
    def __init__(self, game, x, y, id, order):
        self.size = 40
        self.game = game
        self.id = id
        self.order = order
        self.rect = pygame.Rect(x, y, self.size, self.size)

    def update(self, relative_rect):
        pygame.draw.rect(self.game.wn, (0, 0, 0), relative_rect, 16)
        pygame.draw.rect(self.game.wn, (20, 20, 20), relative_rect, 8)
        pygame.draw.rect(self.game.wn, (40, 0, 40), relative_rect, 4)
        pygame.draw.rect(self.game.wn,  (70, 0, 70), relative_rect, 2)
        if self.rect.colliderect(self.game.player.rect) and self.order == 0:
            self.teleport()

    def teleport(self):
        for teleporter in self.game.teleporters:
            if not self==teleporter:
                if teleporter.id == self.id and teleporter.order == 1:
                    self.game.player.rect.x = teleporter.rect.x
                    self.game.player.rect.y = teleporter.rect.y



    def handle_event(self, event):
        pass
