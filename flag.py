import pygame

class Flag:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('flag.png').convert_alpha(), (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))  
    def update(self, relative_pos):
        self.game.wn.blit(self.image, (relative_pos[0], relative_pos[1]))
        if self.handle_event() == 'collision':
            self.handle_transition()
    def handle_event(self):
        if self.game.player.rect.colliderect(pygame.Rect(self.x+self.rect.w/4, self.y+self.rect.h/2, self.rect.w/2, self.rect.h/2)):
            return 'collision'
        
    def handle_transition(self):
        pygame.time.delay(30)
        fade_surface = pygame.Surface((self.game.wnx, self.game.wny))
        fade_surface.fill((0, 0, 0))
        self.nice_text = pygame.font.Font(font='SourGummy-VariableFont_wdth,wght.ttf', size=30).render("Nice, here is another level for you!", True, (200, 200, 200))

        # Gradually increase the alpha value of the surface to create a fade effect
        for alpha in range(0, 256, 5):  # Change step size for faster/slower transition
            fade_surface.set_alpha(alpha)
            self.game.wn.blit(fade_surface, (0, 0))
            self.game.wn.blit(self.nice_text, (self.game.wnx/2 - self.nice_text.get_width()/2, self.game.wny/2 - self.nice_text.get_height()/2))
            pygame.display.flip()
            pygame.time.delay(30)  # Control the speed of the fade

        # Transition logic (level up)
        self.game.level += 1
        self.game.sound.stop()
        self.game.sound = self.game.all_sounds[str(self.game.level)]
        self.game.sound.play()
        self.game.teleporters = self.game.all_teleporters[str(self.game.level)]
        self.game.wn.fill((10, 10, 10))  # Clear the screen for the next level

        # Fade back in (optional)
        for alpha in range(255, -1, -5):
            fade_surface.set_alpha(alpha)
            self.game.wn.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

