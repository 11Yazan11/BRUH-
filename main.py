from gameInstance import *



pygame.init()


class Game:
    def __init__(self, window_width, window_height, level=1, building=False):

        # STATIC
        self.wnx = window_width
        self.wny = window_height
        self.lives = 5
        self.bg_color = (60, 55, 55)
        self.wn = pygame.display.set_mode((self.wnx, self.wny))
        self.fps = 60
        self.level = level
        self.building = building
        self.font = pygame.font.Font(size=30)
        self.clock = pygame.time.Clock()
        self.camera = Camera(self, self.wnx, self.wny/2)




        # LEVEL DEPENDING
        self.all_maps = {
            '1':[Bixel(self, x*40, self.wny-40*y, (100, 80, 20)) for x in range(0, self.wnx*2//40+1) for y in range(1, 5)] + \
           [Bixel(self, 320, 400, (100, 100, 100))] + [Bixel(self, 360, 400, (100, 100, 100))] + \
           [Bixel(self, 0, y*40, (100, 80, 20)) for y in range(0, self.wny//40)] + \
           [Bixel(self, self.wnx-40+40*x, y*40, (100, 80, 20)) for y in range(0, self.wny//40) for x in range(0, 10)] + \
           [Bixel(self, 440+x*40, 320, (100, 100, 100)) for x in range(0, 6)] + \
           [Bixel(self, self.wnx-80, 400, (100, 100, 100))] + \
           [Bixel(self, 0+x*40, -40, (100, 80, 20)) for x in range(0, round(self.wnx*1.5)//40)] + \
           [Bixel(self, self.wnx-80, 400, (100, 150, 100))],
            '2':[Bixel(self, x*40, self.wny-40*y, (100, 80, 20)) for x in range(0, self.wnx*2//40) for y in range(1, 5)] + \
                [Bixel(self, self.wnx*2-40+40*x, y*40, (100, 80, 20)) for y in range(0, self.wny//40) for x in range(0, 10)] + \
                [Bixel(self, 0, y*40, (100, 80, 20)) for y in range(-1, self.wny//40)] + \
                [Bixel(self, 320+x*40, 400-x*20, (100, 100, 100)) for x in range(0, 20, 3)] + \
                [Bixel(self, 360+x*40, 400-x*20, (100, 100, 100)) for x in range(0, 20, 3)] + \
                [Bixel(self, 1160, 400-y*40, (50, 0, 0), deadly=True) for y in range(0, 10)] + \
                [Bixel(self, 0+x*40, -80-y*40, (100, 80, 20)) for x in range(0, round(self.wnx*2.5)//40) for y in range(0, 9)] + \
                [Bixel(self, self.wnx*2-80, 440, (100, 150, 100))],
            '3':[Bixel(self, x*40, self.wny-40*y, (100, 80, 20)) for x in range(-10, self.wnx*2//40) for y in range(1, 5)] + \
                [Bixel(self, self.wnx*2-40+40*x, -320 + y*40, (100, 80, 20)) for y in range(0, self.wny//40+8) for x in range(0, 10)] + \
                [Bixel(self, 0, -320 + y*40, (100, 80, 20)) for y in range(0, self.wny//40+8)] + \
                [Bixel(self, 200+x*40, 440+y*40, (100, 0, 0), deadly=True) for y in range(0, 2) for x in range(0, 5)] + \
                [Bixel(self, 400+x*40, 400, (100, 100, 100)) for x in range(0, 11)] + \
                [Bixel(self, 880+x*40, 320, (100, 100, 100)) for x in range(0, 11)] + \
                [Bixel(self, 1320+x*40, 240, (100, 100, 100)) for x in range(0, 11)] + \
                [Bixel(self, 1760, 200, (100, 100, 100))] + \
                [Bixel(self, 1360+x*40, 120, (100, 100, 100)) for x in range(0, 9)] + \
                [Bixel(self, 800+x*40, 40, (100, 100, 100)) for x in range(0, 13)] + \
                [Bixel(self, 600+x*80, -200+x*40, (100, 100, 100)) for x in range(0, 5, 2)] + \
                [Bixel(self, 560+x*80, -200+x*40, (100, 100, 100)) for x in range(0, 5, 2)] + \
                [Bixel(self, 240+x*40, -240, (100, 100, 100)) for x in range(0, 8)] + \
                [Bixel(self, 80, -80, (100, 150, 100))] + \
                [Bixel(self, 0+x*40, -320, (100, 80, 20)) for x in range(round(self.wnx*2.5)//40)],

            '4': [Bixel(self, x*40, self.wny-40*y, (50, 40, 10)) for x in range(-10, self.wnx*3//40) for y in range(1, 5)] + \
                 [Bixel(self, self.wnx*3-40+40*x, -600 + y*40, (50, 40, 10)) for y in range(0, self.wny*4//40+8) for x in range(0, 10)] + \
                 [Bixel(self, 0, -600 + y*40, (50, 40, 10)) for y in range(0, self.wny*4//40+8)] + \
                 
                 [Bixel(self, 40+x*40, -240, (40, 40, 40)) for x in range(0, 8)] + \
                 [Bixel(self, 80+x*40, -160, (40, 40, 40)) for x in range(0, 8)] + \
                 [Bixel(self, 40+x*40, -80, (40, 40, 40)) for x in range(0, 9)] + \
                 #BRUH--
                 [Bixel(self, 480+x*40, -80, (40, 40, 40)) for x in range(0, 9)] + \
                 #BRUH--
                 [Bixel(self, 480+x*40, 360, (40, 40, 40)) for x in range(0, 15)] + \
                 [Bixel(self, 840+x*40, 280, (40, 40, 40)) for x in range(0, 2)] + \
                 [Bixel(self, 1120, -120+y*40, (40, 40, 40)) for y in range(0, 8)] + \
                 [Bixel(self, 800, -80+y*40, (40, 40, 40)) for y in range(0, 2)] + \
                 [Bixel(self, 880, -120+y*40, (40, 40, 40)) for y in range(0, 3)] + \
                 [Bixel(self, 1040+x*40, 240, (40, 40, 40)) for x in range(0, 42)] + \
                 [Bixel(self, 1120+x*40, 160, (40, 40, 40)) for x in range(0, 13)] + \
                 [Bixel(self, 1160+x*40, -120, (20, 0, 0), deadly=True) for x in range(0, 20)] + \
                 [Bixel(self, 1920, -80+y*40, (40, 40, 40)) for y in range(0, 4)] + \
                 [Bixel(self, 1600+x*40, 80, (40, 40, 40)) for x in range(0, 14)] + \
                 [Bixel(self, 1600, 120, (40, 40, 40))] + \
                 [Bixel(self, 2120, 40, (40, 40, 40))] + \
                 
                 
                 
                 [Bixel(self, 40+x*40, 440, (20, 0, 0), deadly=True) for x in range(0, round(self.wnx*3.5)//40)] + \
                 
                 [Bixel(self, 400, -280, (40, 40, 40))] + \
                 [Bixel(self, 400, -320, (40, 40, 40))] + \
                 [Bixel(self, 400, -360, (40, 40, 40))] + \
                 [Bixel(self, 400, -240, (40, 40, 40))] + \

                 [Bixel(self, 440, -360+y*40, (40, 40, 40)) for y in range(0, 20) if y != 6 and y!=2 and y!=1] + \
                 [Bixel(self, 600, -360+y*40, (40, 40, 40)) for y in range(0, 6) if y != 0 and y!=1] + \
                 [Bixel(self, 480, -240, (40, 40, 40))] + \
                 [Bixel(self, 560, -160, (40, 40, 40))] + \
                 
                 [Bixel(self, 640+x*40, -160, (40, 40, 40)) for x in range(0, 14)] + \
                 [Bixel(self, 640, -120, (40, 40, 40))] + \
                 [Bixel(self, 1200, -200, (40, 40, 40))] + \
                 [Bixel(self, 1000, -200, (40, 40, 40))] + \
                 [Bixel(self, 1200+x*40, -160, (40, 40, 40)) for x in range(0, 20) if x%4 == 0] + \
                 [Bixel(self, 1240+x*40, -160, (40, 40, 40)) for x in range(0, 20) if x%4 == 0] + \
                 [Bixel(self, 2040+x*40, 0, (40, 40, 40)) for x in range(0, 10)] + \
                 [Bixel(self, 2400, 0-y*40, (40, 40, 40)) for y in range(0, 10)] + \
                 [Bixel(self, 2400+x*40, -360, (40, 40, 40)) for x in range(0, 9)] + \
                 [Bixel(self, 2240, 0, (40, 40, 40)) for x in range(0, 5)] + \
                 [Bixel(self, 0+x*40, -600-y*40, (50, 40, 10)) for x in range(round(self.wnx*3.5)//40) for y in range(0, 11)] + \
                 [Bixel(self, self.wnx*3-160+x*40, -280+y*160, (40, 40, 40)) for x in range(0, 3) for y in range(0, 4)] + \
                 [Bixel(self, self.wnx*3-360+x*40, -200+y*160, (40, 40, 40)) for x in range(0, 3) for y in range(0, 3)] + \
                 [Bixel(self, self.wnx*3-80, -280, (50, 75, 50))]                  
        }
        self.map = self.all_maps[str(self.level)]

        self.all_teleporters = {"1":[],
                                "2":[],
                                "3":[],                   
                                "4":[Teleporter(self, 2240, -40, "1st", 0), Teleporter(self, 680, -120, "1st", 1)]} 
        
        self.teleporters = self.all_teleporters[str(self.level)]

        self.all_players = {
            "1":Player(self, 40, self.wny-40*7, (100, 100, 0), 5),
            "2":Player(self, 40, self.wny-40*7, (100, 100, 0), 5), 
            "3":Player(self, 40, self.wny-40*7, (100, 100, 0), 5),  
            "4":Player(self, 40, -280, (50, 50, 0), 5)        
        }
        self.player = self.all_players[str(self.level)]

        self.all_texts = {"1":[Text(self, 'Level 1, the basics...', 50, 100, 80, 'white', font="SourGummy-VariableFont_wdth,wght.ttf", center=False), \
                      Text(self, '[Arrow keys] to move, [R] to respawn.', 20, 100, 130, (150, 150, 150), font="SourGummy-VariableFont_wdth,wght.ttf", center=False)],
                          "2":[Text(self, 'Level 2, some more stuff...', 50, 100, 80, 'white', font="SourGummy-VariableFont_wdth,wght.ttf", center=False), \
                      Text(self, '[Arrow keys] to move, [R] to respawn, [SPACE] to freeze.', 20, 100, 130, (150, 150, 150), font="SourGummy-VariableFont_wdth,wght.ttf", center=False)],
                          "3":[Text(self, 'Level 3, RUN!', 50, 90, 90, 'white', font="SourGummy-VariableFont_wdth,wght.ttf", center=False), \
                               Text(self, '', 30, 90, 135, 'red', font="SourGummy-VariableFont_wdth,wght.ttf", center=False, timer=True, maxtime=150), \
                               Text(self, '[Arrow keys] to move', 20, 90, 170, (150, 150, 150), font="SourGummy-VariableFont_wdth,wght.ttf", center=False)],
                          "4":[Text(self, 'Level 4, fall into darkness...', 50, 90, -500, 'white', font="SourGummy-VariableFont_wdth,wght.ttf", center=False), \
                               Text(self, '[Arrow keys] to move.', 20, 90, -430, (150, 150, 150), font="SourGummy-VariableFont_wdth,wght.ttf", center=False)],
        }
        self.texts = self.all_texts[str(self.level)] 


        self.all_flags = {"1":Flag(self, self.wnx-80, 400-40),
                          "2":Flag(self, self.wnx*2-80, 400),
                          "3":Flag(self, 80, -120),
                          "4":Flag(self, self.wnx*3-80, -320)}
        self.flag = self.all_flags[str(self.level)]


        self.all_sounds = {"1":Sound("echoes-of-the-past-from-album-liminal-spaces-197000.mp3", loop=True),
                           "2":Sound("backrooms-endless-maze-of-yellow-walls-226061.mp3", loop=True),
                           "3":Sound("RUN_FOR_IT.mp3.mpeg", loop=True), 
                           "4": Sound("summer-1993-from-album-liminal-spaces-224214.mp3", loop=True)}
        self.sound = self.all_sounds[str(self.level)]
        self.sound.play()
        

    def screenRendering(self):
        self.clock.tick(self.fps)
        pygame.display.flip()
        if self.level == 4:
            self.bg_color = (10, 10, 10)
        else:
            self.bg_color = (60, 55, 55)

        self.wn.fill(self.bg_color)
        pygame.display.set_caption(f'2D PLATFORMER | FPS: {self.fps} | LIVES: {self.lives}')

    
    def mapUpdater(self):
        for bixel in self.map:
            bixel.update(self.camera.apply(bixel))

    def textUpdater(self):
        for text in self.texts:
            text.update(self.camera.apply(text))
        

    
    def teleporterUpdater(self):
        for teleporter in self.teleporters:
            teleporter.update(self.camera.apply(teleporter))
    



    def actionUpdater(self):
        self.camera.update(self.player)
        self.textUpdater()
        self.mapUpdater()
        self.teleporterUpdater()
        self.flag.update((self.camera.apply(self.flag).x, self.camera.apply(self.flag).y))
        self.player.update(self.camera.apply(self.player))

        


        self.map = self.all_maps[str(self.level)]
        self.player = self.all_players[str(self.level)]
        self.texts = self.all_texts[str(self.level)] 
        self.flag = self.all_flags[str(self.level)]
        self.telporters = self.all_teleporters[str(self.level)]



    def eventUpdater(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.building:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            for bixel in self.map:
                bixel.handle_event(event)
            self.player.handle_event(event)
            self.sound.handle_event(event)
            for teleporter in self.teleporters:
                teleporter.handle_event(event)
            if event.type == pygame.QUIT:
                return False
        return True

    def run(self):
        while True:
            self.screenRendering()
            if not self.eventUpdater():
                return
            self.actionUpdater()

if __name__ == "__main__":
    game = Game(920, 600, level=4)  # You can adjust these if your screen is too small of can afford more size. Just keep the ratio please.
    game.run()

pygame.quit()

#BEST SCORE FROM YAZAN ON LEVEL 4 IS 41:70
    
        