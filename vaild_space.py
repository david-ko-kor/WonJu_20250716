import random

# 필요한 조각 정보와 클래스 정의
S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
shapes = [S] # 간단한 예제를 위해 S 조각만 사용
shape_colors = [(0, 230, 115)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[0]
        self.rotation = 0

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

# --- 함수 사용 예제 ---
new_piece = get_shape()
print(f"생성된 조각의 모양: {new_piece.shape}")
print(f"변환된 조각의 좌표: {convert_shape_format(new_piece)}")
