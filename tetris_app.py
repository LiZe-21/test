import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw
from utils.pieces import Piece
from utils.board import Board

# 페이지 설정
st.set_page_config(page_title="Streamlit Tetris", layout="wide")

# 세션 초기화
if 'board' not in st.session_state:
    st.session_state.board = Board()
if 'piece' not in st.session_state:
    st.session_state.piece = Piece()
if 'pos' not in st.session_state:
    st.session_state.pos = [0, 3]
if 'last_drop' not in st.session_state:
    st.session_state.last_drop = time.time()

# 컨트롤 패널
st.title("Streamlit Tetris")
col1, col2 = st.columns([1,4])
with col1:
    if st.button('Rotate'):
        new_piece = st.session_state.piece
        new_piece.rotate()
        if st.session_state.board.collision(new_piece, st.session_state.pos):
            new_piece.rotate()  # 충돌 시 롤백
    if st.button('Left'):
        st.session_state.pos[1] -= 1
        if st.session_state.board.collision(st.session_state.piece, st.session_state.pos):
            st.session_state.pos[1] += 1
    if st.button('Right'):
        st.session_state.pos[1] += 1
        if st.session_state.board.collision(st.session_state.piece, st.session_state.pos):
            st.session_state.pos[1] -= 1
    if st.button('Down'):
        st.session_state.pos[0] += 1
    if st.button('Drop'):
        # 바닥까지 즉시
        while not st.session_state.board.collision(st.session_state.piece, st.session_state.pos):
            st.session_state.pos[0] += 1
        st.session_state.pos[0] -= 1

# 자동 낙하 속도
drop_interval = st.slider('Drop Speed (sec)', 0.1, 1.0, 0.5, 0.1)

# 자동 낙하
if time.time() - st.session_state.last_drop > drop_interval:
    st.session_state.pos[0] += 1
    st.session_state.last_drop = time.time()

# 충돌 시 처리
if st.session_state.board.collision(st.session_state.piece, st.session_state.pos):
    # 위로 롤백
    st.session_state.pos[0] -= 1
    st.session_state.board.lock_piece(st.session_state.piece, st.session_state.pos)
    # 새 조각 생성
    st.session_state.piece = Piece()
    st.session_state.pos = [0, 3]
    if st.session_state.board.collision(st.session_state.piece, st.session_state.pos):
        st.session_state.board.game_over = True

# 그리드 렌더링 함수
def render_board(board: Board, piece: Piece, pos) -> Image:
    cell_size = 20
    img = Image.new('RGB', (board.cols*cell_size, board.rows*cell_size), color=(0,0,0))
    draw = ImageDraw.Draw(img)
    # 고정된 블록
    for r in range(board.rows):
        for c in range(board.cols):
            color = tuple(map(int, board.grid[r,c]))
            if any(color):
                x0, y0 = c*cell_size, r*cell_size
                draw.rectangle([x0, y0, x0+cell_size, y0+cell_size], fill=color)
    # 현재 블록
    shape = piece.matrix
    h, w = shape.shape
    for i in range(h):
        for j in range(w):
            if shape[i,j]:
                r, c = pos[0]+i, pos[1]+j
                x0, y0 = c*cell_size, r*cell_size
                draw.rectangle([x0, y0, x0+cell_size, y0+cell_size], fill=piece.color)
    return img

# 화면 출력
col2.image(render_board(st.session_state.board, st.session_state.piece, st.session_state.pos), use_column_width=True)
st.write(f"Score: {st.session_state.board.score}")
if st.session_state.board.game_over:
    st.error("Game Over!")
    if st.button('Restart'):
        st.session_state.board.reset()
        st.session_state.piece = Piece()
        st.session_state.pos = [0,3]
        st.session_state.board.game_over = False
