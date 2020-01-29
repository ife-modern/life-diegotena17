from src.constants import *
from src.color import Color
from src.mouse import Mouse
from src.gui import Gui, WidgetAction
from src.grid import Grid
from src.draw import DrawText
import os
import sys
import pygame

class Game(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.display.set_caption("Conway's Game of Life")
        # global objects
        self.color = Color()
        self.mouse = Mouse()
        # surfaces
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen_grid = pygame.Surface(GRID_SIZE)
        self.screen_gui = pygame.Surface(GUI_SIZE)
        # clocks
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)
        self.ticks = pygame.time.get_ticks()
        self.cooldown = 250
        self.gen = 0
        # sprite groups
        self.widgets = pygame.sprite.Group()
        self.cells = pygame.sprite.Group()
        # gui
        self.gui = None
        self.action = None
        self.grid = None
        # flags
        self.running = False
        self.debugging = False
        self.evolving = False
        # images
        self.image_path = os.path.join(os.getcwd(), 'img')
        self.image_cell_path = os.path.join(self.image_path, 'cells')
        self.image_gui_path = os.path.join(self.image_path, 'gui')
        # fonts
        self.font_path = os.path.join(os.getcwd(), 'font')
        self.font_name = os.path.join(self.font_path, 'kenvector_future2.ttf')
        self.draw_text = DrawText()

    def new(self):
        # create the cells and grid
        self.cells = pygame.sprite.Group()
        self.grid = Grid(self)
        self.grid.new_map()
        # create the gui and its widgets
        self.widgets = pygame.sprite.Group()
        self.gui = Gui(self)
        self.gui.load_widgets()
        self.action = WidgetAction(self)

    def evolve(self):
        print('evolving...')
        self.gen+=1
        for cell in self.cells:
            if cell.neighbours:
                cell_count = len(cell.neighbours)
                # 1. Any live cell with fewer than two live neighbours dies,
                # as if by underpopulation.
                # 3. Any live cell with more than three live neighbours dies,
                # as if by overpopulation.
                if cell.live and (cell_count < 2 or cell_count > 3):
                    cell.live = False
                    cell.image = cell.dead_cell
                # 2. Any live cell with two or three live neighbours lives on
                # to the next generation.
                if cell.live and (cell_count == 2 or cell_count == 3):
                    continue
                # 4. Any dead cell with exactly three live neighbours becomes
                # a live cell, as if by reproduction.
                if not cell.live and cell_count == 3:
                    cell.live = True
                    cell.image = cell.live_cell

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_d:
                    self.debugging = not self.debugging
                elif event.key == pygame.K_o:  # open a config
                    pass
                elif event.key == pygame.K_s:  # save a config
                    pass
                elif event.key == pygame.K_r:  # restart current config
                    self.action.event('reset')
                elif event.key == pygame.K_SPACE:  # run current config
                    self.action.event('play')
            self.mouse.motion(event)
            self.mouse.button_down(event)
            self.mouse.button_up(event)

    def update(self):
        self.delta_time = self.clock.tick(FPS) / 1000.0
        self.events()
        self.cells.update()
        self.widgets.update()
        self.action.update()
        if self.evolving:
            now = pygame.time.get_ticks()
            if now - self.ticks > self.cooldown:
                self.ticks = pygame.time.get_ticks()
                self.evolve()
        self.grid.update()

    def draw(self):
        # fill the main screen first
        self.screen.fill(self.color.black)
        # fill, draw, and then blit the GUI
        self.screen_gui.fill(self.color.black)
        self.widgets.draw(self.screen_gui)
        self.action.draw_context()
        self.screen.blit(self.screen_gui, GUI_DEST)
        # fill, draw, and then blit the Grid
        self.screen_grid.fill(self.color.black)
        self.cells.draw(self.screen_grid)
        self.screen.blit(self.screen_grid, GRID_DEST)
		# display generation number
		#self.gen+=1
        self.draw_text.set_font(self.font_name, FONT_SIZE)
        self.draw_text.render("Generation: " + str(self.gen), self.color.green)
        self.draw_text.set_rect((GUI_WIDTH, GUI_HEIGHT), 'bottomright')
        self.draw_text.blit(self.screen)

    def run(self):
        self.running = True
        self.gen=0
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
