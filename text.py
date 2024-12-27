import pygame #type:ignore

class Text:
    def __init__(self, game, text, size, x, y, color, font='', center=True, timer=False, maxtime=None, lives=None):
        self.game = game
        self.center = center
        self.font = pygame.font.Font(font=font if font else None, size=size)
        self.rendered_text = self.font.render(text, True, color)
        self.x = x - self.rendered_text.get_width()/2 if self.center else x 
        self.y = y - self.rendered_text.get_height()/2
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.text = text
        self.color = color
        self.lives = lives
        self.max_time = maxtime
        self.timer = 0 if timer else None
        self.og_timer = timer if timer else None

    def update(self, relative_rect=None):
        if self.lives is not None:
            self.rendered_text = self.font.render(' + ' + '+ '*(self.game.lives-1), True, self.color)
        if relative_rect is None:
            relative_rect = self.rect
        self.game.wn.blit(self.rendered_text, (relative_rect.x, relative_rect.y))
        self.handle_timer()
        if self.game.lives <= 0:
            self.die_total(location="frompartial")
            
        


    def die_total(self, location):
        self.game.all_players["1"].rect = pygame.Rect(40, self.game.wny-40*7, 40, 40)
        self.game.all_players["2"].rect = pygame.Rect(40, self.game.wny-40*7, 40, 40)
        self.game.all_players["3"].rect = pygame.Rect(40, self.game.wny-40*7, 40, 40)
        self.game.all_players["4"].rect = pygame.Rect(40, -280, 40, 40)
        if location=="frompartial":
            self.game.lives = 5
            self.timer = self.og_timer

        for player in self.game.all_players.values():
            player.velocity_y = 0  
            player.velocity_x = 0
            player.grounded = False

        self.game.level = 1
        self.game.sound.stop()
        self.game.sound = self.game.all_sounds[str(self.game.level)]
        self.game.sound.play()

        self.game.player = self.game.all_players[str(self.game.level)]
        self.game.teleporter = self.game.all_teleporters[str(self.game.level)]
        self.game.player.velocity_y = 0  
        self.game.player.velocity_x = 0
        self.game.player.grounded = False
        pygame.time.delay(30)
        fade_surface = pygame.Surface((self.game.wnx, self.game.wny))
        fade_surface.fill((0, 0, 0))
        self.nice_text = pygame.font.Font(font='SourGummy-VariableFont_wdth,wght.ttf', size=30).render("It's over mate, now restart it all...", True, (90, 0, 0)) if location != "frompartial" else pygame.font.Font(font='SourGummy-VariableFont_wdth,wght.ttf', size=30).render("Looks like you've died too much: lives reset but levels too...", True, (90, 0, 0))

        # Gradually increase the alpha value of the surface to create a fade effect
        if location == "frompartial":
            for alpha in range(255, -1, -5):  # Change step size for faster/slower transition
                fade_surface.set_alpha(alpha)
                self.game.wn.blit(fade_surface, (0, 0))
                self.game.wn.blit(self.nice_text, (self.game.wnx/2 - self.nice_text.get_width()/2, self.game.wny/2 - self.nice_text.get_height()/2))
                pygame.display.flip()
                pygame.time.delay(100)  # Control the speed of the fade
        else:
            for alpha in range(0, 256, 5):  # Change step size for faster/slower transition
                self.game.wn.blit(fade_surface, (0, 0))
                self.game.wn.blit(self.nice_text, (self.game.wnx/2 - self.nice_text.get_width()/2, self.game.wny/2 - self.nice_text.get_height()/2))
                pygame.display.flip()
                pygame.time.delay(50)  # Control the speed of the fade

        
 
    
    
    def handle_timer(self):
        if self.timer is None:
            return
        self.timer += 1/self.game.fps
        self.rendered_text = self.font.render(f'{self.text} Timer: {round(self.timer)} / {self.max_time}', True, self.color)

        if self.timer >= self.max_time:
            self.die_total(location=None)
            self.timer = 0
    
