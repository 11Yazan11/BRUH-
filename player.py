import pygame # type: ignore


class Player:
    def __init__(self, game, x, y, color, speed, commands={'LEFT': pygame.K_LEFT, 'RIGHT': pygame.K_RIGHT, 'JUMP': pygame.K_UP, 'RESPAWN': pygame.K_r, 'FREEZE':pygame.K_SPACE}):
        self.game = game
        self.x = x
        self.y = y
        self.size = 40
        self.color = color
        self.commands = commands
        self.speed = speed
        self.gravity = 9.81 / self.game.fps
        self.jump_strength = -10 #-10 # Initial upward velocity for a jump
        self.velocity_y = 0  # Current vertical velocity
        self.velocity_x = 0
        self.air_resistance = 0.009  # Air resistance (drag)
        self.ground_friction = 0.15  # Friction coefficient for ground sliding
        self.air_friction = 0.009
        self.elasticity = 0.8  # Coefficient of restitution (bounciness)
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.ground_level = self.get_ground_y(self.game.map) # Ground level based on window height
        self.grounded = False
        self.ground_bounce_img = pygame.transform.scale(pygame.image.load('animations/bounce.png').convert_alpha(), (30, 30))
        self.bounce_effects = []
        self.ground_block_level = None

    def isValid(self, bixels):
        tester_rect = self.rect.copy()
        tester_rect.x += self.velocity_x  # Update the test rectangle based on horizontal velocity
        nearest = []

        for bixel in bixels:
            # Check if bixel is horizontally aligned with the player
            if (tester_rect.right > bixel.rect.left and tester_rect.left < bixel.rect.right) and \
            (tester_rect.bottom > bixel.rect.top and tester_rect.top < bixel.rect.bottom):  # Check for vertical overlap
                # Detect collisions on the left side
                if tester_rect.right > bixel.rect.left and tester_rect.left < bixel.rect.left:
                    nearest.append(('left', bixel.rect, bixel.deadly))
                # Detect collisions on the right side
                if tester_rect.left < bixel.rect.right and tester_rect.right > bixel.rect.right:
                    nearest.append(('right', bixel.rect, bixel.deadly))

        if not nearest:
            return True
        else:
            # Sort the nearest bixels by distance from the player's x-coordinate
            def distance_to_player(item):
                direction, bixel_rect, deadly = item
                return abs(self.rect.x - bixel_rect.x)

            nearest_bixel = min(nearest, key=distance_to_player)
            direction, bixel_rect, deadly = nearest_bixel

            # Resolve collision by stopping player movement at the edge of the bixel
            if deadly:
                respawn_event = pygame.event.Event(pygame.USEREVENT, {"action": "respawn"})
                pygame.event.post(respawn_event)
                self.die_partial()
                return False
            elif direction == 'left':
                self.rect.x = bixel_rect.left - self.rect.w 
            elif direction == 'right':
                self.rect.x = bixel_rect.right  # Stop at the left edge of the bixel

            return False


    def isValidJump(self, bixels):
        tester_rect = self.rect.copy()
        tester_rect.y += self.velocity_y
        nearest = []
        for bixel in bixels:
            if (tester_rect.right > bixel.rect.left and tester_rect.left < bixel.rect.right) and \
            (tester_rect.bottom > bixel.rect.top and tester_rect.top < bixel.rect.bottom):
                if (tester_rect.top <= bixel.rect.bottom) and (tester_rect.bottom > bixel.rect.bottom):
                    nearest.append(bixel)
        if not nearest:
            return True
        else:
            def distance_to_player(item):
                nr_bixel = item
                return abs(self.rect.y - nr_bixel.rect.y)

            nearest_bixel = min(nearest, key=distance_to_player)
            self.rect.y = nearest_bixel.rect.y + nearest_bixel.rect.h

            return False



    
    def get_ground_y(self, bixels):
        """Finds nearest object under player, between his x and x+width, and in his vertical axis."""
        nearest = None
        for bixel in reversed(bixels):
            if bixel.rect.x+bixel.rect.w>self.rect.x and bixel.rect.x<self.rect.x+self.rect.w:  # Check if object is horizontally under player
                if bixel.rect.y >= self.rect.y+self.rect.h:  # Make sure object is below the player
                    if nearest is None or bixel.rect.y < nearest.rect.y:  # Find the closest object
                        nearest = bixel
        
        if nearest:
            self.ground_block_level = nearest
            return nearest.rect.y
        
        else:
            return self.game.wny - self.size  # If no object found, return the default ground level
        

        
    def die_partial(self):
        self.game.lives -= 1
        if self.game.lives <= 0:
            return
        pygame.time.delay(30)
        fade_surface = pygame.Surface((self.game.wnx, self.game.wny))
        fade_surface.fill((0, 0, 0))
        self.nice_text = pygame.font.Font(font='SourGummy-VariableFont_wdth,wght.ttf', size=30).render("You Died LOL", True, (90, 0, 0))

        # Gradually increase the alpha value of the surface to create a fade effect
        for alpha in range(0, 256, 5):  # Change step size for faster/slower transition
            self.game.wn.blit(fade_surface, (0, 0))
            self.game.wn.blit(self.nice_text, (self.game.wnx/2 - self.nice_text.get_width()/2, self.game.wny/2 - self.nice_text.get_height()/2))
            pygame.display.flip()
            pygame.time.delay(40)  # Control the speed of the fade

        for alpha in range(255, -1, -5):
            self.game.wn.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)


                


    def update(self, relative_rect):

        # Collision with the ground
        if self.rect.y+self.velocity_y >= self.ground_level:
            if self.ground_block_level.deadly:
                respawn_event = pygame.event.Event(pygame.USEREVENT, {"action": "respawn"})
                pygame.event.post(respawn_event)
                self.die_partial()
            

            self.rect.y = self.ground_level
            self.velocity_y = -self.velocity_y * self.elasticity  # Bounce back with reduced energy
            
            self.grounded = True
            # Stop tiny oscillations when nearly at rest
            if abs(self.velocity_y) < 0.2:
                self.velocity_y = 0
            else:
                self.bounce_effects.append({'x':relative_rect.centerx, 'y':relative_rect.y+relative_rect.h, 'time':0})
                

        else:
            self.grounded = False


        self.ground_level = self.get_ground_y(self.game.map)-self.size

        # Apply gravity
        self.velocity_y += self.gravity

        # Apply air resistance
        self.velocity_y -= self.air_resistance * self.velocity_y * abs(self.velocity_y)

        # Update vertical position
        if self.isValidJump(self.game.map):
            self.rect.y += self.velocity_y
        else:
            self.velocity_y = 0
        

        if self.grounded:
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - self.ground_friction)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + self.ground_friction)
        else:
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - self.air_friction)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + self.air_friction)


        if self.isValid(self.game.map):
            self.rect.x += self.velocity_x
        else:
            self.velocity_x *= -1
               
     



        # Draw the player
        pygame.draw.rect(self.game.wn, self.color, relative_rect)
        pygame.draw.rect(self.game.wn, (150, 150, 0), relative_rect, 10)
        pygame.draw.rect(self.game.wn, (20, 20, 20), relative_rect, 4)
        for effect in self.bounce_effects:
            self.ground_bounce_img_rect = self.ground_bounce_img.get_rect(topleft=(effect["x"]-15, effect["y"]-15))
            self.game.wn.blit(self.ground_bounce_img, (self.ground_bounce_img_rect.x, self.ground_bounce_img_rect.y))
            effect["time"] += 1
            if effect["time"] >= 10:
                self.bounce_effects.remove(effect)

        # Check for horizontal movement inputs
        self.check_moving_keys()

    def check_moving_keys(self):
        pressed = pygame.key.get_pressed()
        for (k, value) in self.commands.items():
            if pressed[value]:
                self.move(k)

    def handle_event(self, event):
        # Handle jumping
        if event.type == pygame.KEYDOWN and event.key == self.commands.get('JUMP'):
            if self.rect.y == self.ground_level:  # Allow jump only if on the ground
                self.velocity_y = self.jump_strength

        if event.type == pygame.KEYDOWN and event.key == self.commands.get('FREEZE') and self.game.level == 2:
                self.velocity_x = 0

        if (event.type == pygame.KEYDOWN and event.key == self.commands.get('RESPAWN') and self.game.level != 3 and self.game.level != 4) or (event.type == pygame.USEREVENT and event.action == "respawn"):
            self.velocity_y = 0  
            self.velocity_x = 0
            self.air_resistance = 0.01  # Air resistance (drag)
            self.ground_friction = 0.2  # Friction coefficient for ground sliding
            self.elasticity = 0.8  # Coefficient of restitution (bounciness)
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            self.ground_level = self.get_ground_y(self.game.map) # Ground level based on window height
            self.grounded = False


    def move(self, dir):
        if self.grounded:
            if dir == "LEFT":
                v = self.velocity_x
                self.velocity_x = -self.speed
                if not self.isValid(self.game.map):
                    self.velocity_x = 0
            if dir == "RIGHT":
                v = self.velocity_x
                self.velocity_x = self.speed
                if not self.isValid(self.game.map):
                    self.velocity_x = 0

    def destroy(self):
        pass
