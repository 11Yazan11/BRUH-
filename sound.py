import pygame

class Sound:
    def __init__(self, sound_file, volume=None, autoplay=False, loop=False):
        """
        Initializes a Sound object.
        
        Args:
            sound_file (str): Path to the sound file.
            autoplay (bool): Whether to play the sound immediately on initialization.
            loop (bool): Whether the sound should loop indefinitely.
        """
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(sound_file)
        self.autoplay = autoplay
        self.loop = loop

        if volume is not None:
            self.set_volume(volume)

        if self.autoplay:
            self.play()

    def play(self):
        """Plays the sound."""
        loops = -1 if self.loop else 0
        self.sound.play(loops=loops)

    def stop(self):
        """Stops the sound."""
        self.sound.stop()

    def set_volume(self, volume):
        """
        Sets the volume of the sound.
        
        Args:
            volume (float): Volume level (0.0 to 1.0).
        """
        self.sound.set_volume(volume)

    def handle_event(self, event):
        """
        Handles a Pygame event related to sound playback.
        
        Args:
            event (pygame.event.Event): Pygame event to handle.
        """
        pass
