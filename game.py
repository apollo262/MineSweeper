import pygame
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE

MAX = 255
def OR(c1, c2):
    color = [c1[0]+c2[0], c1[1]+c2[1], c1[2]+c2[2]]
    for i, c in enumerate(color):
        if color[i] > MAX:
            color[i] = MAX
    return tuple(color)

def MULTIPLY(c, n):
    color = list(c)
    for i, c in enumerate(color):
        color[i] = color[i]*n
    return tuple(color)

class Color:
    BLACK   = (0, 0, 0)
    RED     = (MAX, 0, 0)
    GREEN   = (0, MAX, 0)
    BLUE    = (0, 0, MAX)
    YELLOW  = OR(RED,GREEN)
    WHITE   = OR(YELLOW,BLUE)
    CYAN    = OR(GREEN,BLUE)
    MAGENTA = OR(RED,BLUE)
    GRAY       = MULTIPLY(WHITE,0.5)
    LIGHT_GRAY = MULTIPLY(WHITE,0.75)
    DARK_GRAY = MULTIPLY(WHITE,0.25)

class Game:
    def __init__(self, width, height, caption, fps=60):
        pygame.init()
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.fps = fps
        self.counter = 0

    def event(self, event):
        pass

    def draw(self):
        pass

    def grid(self, interval=10):
        for x in range(0, self.width, interval):
            pygame.draw.line(self.screen, 0x000000, (x,0), (x,self.height))
        for y in range(0, self.height, interval):
            pygame.draw.line(self.screen, 0x000000, (0,y), (self.width,y))

    def debug(self, message, color=Color.BLACK, fontsize=36):
        font = pygame.font.SysFont(None, fontsize)
        text = font.render(message, True, color)
        self.screen.blit(text, (10, self.height-fontsize))

    def is_quit(self, event):
        if event.type == QUIT:
            return True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
        return False

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if self.is_quit(event):
                    return
                self.event(event)

            self.draw()
            self.counter += 1
            pygame.display.update()
            clock.tick(self.fps)

    def main(self):
        self.loop()
        pygame.quit()

