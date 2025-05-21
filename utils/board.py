import numpy as np
from utils.pieces import Piece

class Board:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols, 3), dtype=int)  # RGB 컬러 그리드
        self.score = 0
        self.game_over = False

    def collision(self, piece: Piece, pos):
        r, c = pos
        shape = piece.matrix
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    rr, cc = r + i, c + j
                    if rr < 0 or rr >= self.rows or cc < 0 or cc >= self.cols:
                        return True
                    if any(self.grid[rr, cc]):
                        return True
        return False

    def lock_piece(self, piece: Piece, pos):
        r, c = pos
        shape = piece.matrix
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    self.grid[r+i, c+j] = piece.color
        self.clear_lines()

    def clear_lines(self):
        full_rows = [i for i in range(self.rows) if all(self.grid[i].any(axis=1))]
        for row in full_rows:
            self.grid[1:row+1] = self.grid[0:row]
            self.grid[0] = 0
        self.score += len(full_rows) * 100

    def reset(self):
        self.grid.fill(0)
        self.score = 0
        self.game_over = False
