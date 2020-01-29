from src.constants import *
from src.cell import Cell


class Grid(object):

    def __init__(self, game):
        self.game = game
        self.map = []

    def new_map(self):
        id = 1
        self.map = []
        for y in range(0, GRID_HEIGHT, BIT_DEPTH):
            row = []
            for x in range(0, GRID_WIDTH, BIT_DEPTH):
                rect = (x, y, BIT_DEPTH, BIT_DEPTH)
                cell = Cell(self.game, rect)
                cell.id = id
                id += 1
                row.append(cell)
            self.map.append(row)

    def add_neighbours(self, cell, row, column):
        # Check the squares surrounding the cell at the given row and column
        for offset_row in range(-1, 2):
            for offset_col in range(-1, 2):
                new_row = row + offset_row
                new_col = column + offset_col
                if 0 <= new_row < ROWS and 0 <= new_col < COLUMNS:
                    neighbour = self.map[new_row][new_col]
                    if neighbour.live and cell.id != neighbour.id and neighbour not in cell.neighbours:
                        cell.neighbours.append(neighbour)
                        #print(f'cell {hex(id(cell))} has cell.neighbours {[hex(id(n)) for n in cell.neighbours]} ')

    @staticmethod
    def remove_dead(cell):
        # clean up dead neighbours
        cell.neighbours[:] = (neighbour for neighbour in cell.neighbours if neighbour.live)

    def update(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                cell = self.map[row][column]
                self.add_neighbours(cell, row, column)
                self.remove_dead(cell)
		

