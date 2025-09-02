import streamlit as st

# Initialize game state
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9  # 9 cells for the Tic-Tac-Toe board
    st.session_state.turn = 'X'         # X always starts
    st.session_state.winner = None

def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # columns
        (0,4,8), (2,4,6)             # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != '':
            return board[a]
    return None

def make_move(i):
    if st.session_state.board[i] == '' and st.session_state.winner is None:
        st.session_state.board[i] = st.session_state.turn
        st.session_state.winner = check_winner(st.session_state.board)
        if st.session_state.winner is None:
            st.session_state.turn = 'O' if st.session_state.turn == 'X' else 'X'

st.title("Tic-Tac-Toe Game")

cols = st.columns(3)
for i in range(9):
    if cols[i%3].button(st.session_state.board[i] or ' ', key=i):
        make_move(i)

if st.session_state.winner:
    st.success(f"🎉 {st.session_state.winner} wins!")
elif '' not in st.session_state.board:
    st.info("It's a draw!")
else:
    st.write(f"Turn: {st.session_state.turn}")

if st.button("Restart Game"):
    st.session_state.board = [''] * 9
    st.session_state.turn = 'X'
    st.session_state.winner = None
