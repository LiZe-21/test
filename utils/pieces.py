import numpy as np
import random
tetrominoes = {
    'I': [
        np.array([[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]]),
        np.array([[0,0,1,0], [0,0,1,0], [0,0,1,0], [0,0,1,0]])
    ],
    'O': [
        np.array([[0,1,1,0], [0,1,1,0], [0,0,0,0], [0,0,0,0]])
    ],
    'T': [
        np.array([[0,1,0], [1,1,1], [0,0,0]]),
        np.array([[0,1,0], [0,1,1], [0,1,0]]),
        np.array([[0,0,0], [1,1,1], [0,1,0]]),
        np.array([[0,1,0], [1,1,0], [0,1,0]])
    ],
    'S': [
        np.array([[0,1,1], [1,1,0], [0,0,0]]),
        np.array([[0,1,0], [0,1,1], [0,0,1]])
    ],
    'Z': [
        np.array([[1,1,0], [0,1,1], [0,0,0]]),
        np.array([[0,0,1], [0,1,1], [0,1,0]])
    ],
    'J': [
        np.array([[1,0,0], [1,1,1], [0,0,0]]),
        np.array([[0,1,1], [0,1,0], [0,1,0]]),
        np.array([[0,0,0], [1,1,1], [0,0,1]]),
        np.array([[0,1,0], [0,1,0], [1,1,0]])
    ],
    'L': [
        np.array([[0,0,1], [1,1,1], [0,0,0]]),
        np.array([[0,1,0], [0,1,0], [0,1,1]]),
        np.array([[0,0,0], [1,1,1], [1,0,0]]),
        np.array([[1,1,0], [0,1,0], [0,1,0]])
    ]
}
class Piece:
    def __init__(self, shape_key=None):
        if shape_key is None:
            shape_key = random.choice(list(tetrominoes.keys()))
        self.shape_key = shape_key
        self.rotations = tetrominoes[shape_key]
        self.rotation_index = 0
        self.matrix = self.rotations[self.rotation_index]
        # 색상(렌더링 시 이용)
        self.color = {
            'I': (0,255,255), 'O': (255,255,0), 'T': (128,0,128),
            'S': (0,255,0), 'Z': (255,0,0), 'J': (0,0,255), 'L': (255,165,0)
        }[shape_key]

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.matrix = self.rotations[self.rotation_index]

    def reset(self):
        # 새로운 랜덤 블록으로 교체
        self.__init__()
