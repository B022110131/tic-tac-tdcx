import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Tic-Tac-Toe Master",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .game-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
    }
    
    .winner-announcement {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        animation: pulse 2s infinite;
        margin: 1rem 0;
    }
    
    .draw-announcement {
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        margin: 1rem 0;
    }
    
    .current-turn {
        background: linear-gradient(45deg, #98FB98, #32CD32);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stButton > button {
        width: 100%;
        height: 100px;
        font-size: 0px;
        border: 3px solid #2E86AB;
        border-radius: 15px;
        background: white;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(46, 134, 171, 0.3);
    }
    
    .game-board {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced features
def initialize_game_state():
    if 'board' not in st.session_state:
        st.session_state.board = [''] * 9
    if 'turn' not in st.session_state:
        st.session_state.turn = 'X'
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'stats' not in st.session_state:
        st.session_state.stats = {'X': 0, 'O': 0, 'draws': 0, 'total_games': 0}
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'Human vs Human'
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = 'Classic'
    if 'move_count' not in st.session_state:
        st.session_state.move_count = 0
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = datetime.now()

# Create dynamic images for X and O
def create_symbol_image(symbol, size=(100, 100), bg_color='white', symbol_color='black'):
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", size[0]//2)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position for centering
    bbox = draw.textbbox((0, 0), symbol, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    if symbol == 'X':
        # Draw X with red color and some style
        draw.text((x, y), symbol, fill='#E74C3C', font=font)
        # Add some decoration
        draw.rectangle([10, 10, size[0]-10, size[1]-10], outline='#E74C3C', width=3)
    elif symbol == 'O':
        # Draw O with blue color and some style
        draw.text((x, y), symbol, fill='#3498DB', font=font)
        # Add some decoration
        draw.ellipse([10, 10, size[0]-10, size[1]-10], outline='#3498DB', width=3)
    
    return img

# Load custom images with fallback to generated ones
@st.cache_data
def load_custom_images():
    try:
        empty_img = Image.open("images/empty.png")
        x_img = Image.open("images/x.png")
        o_img = Image.open("images/o.png")
        return empty_img, x_img, o_img, True
    except (FileNotFoundError, Exception) as e:
        st.warning("Custom images not found. Using generated images instead.")
        return None, None, None, False

def get_image(symbol):
    empty_img, x_img, o_img, custom_images_loaded = load_custom_images()
    
    if custom_images_loaded:
        # Use your custom images
        if symbol == 'X':
            return x_img
        elif symbol == 'O':
            return o_img
        else:
            return empty_img
    else:
        # Fallback to generated images
        if symbol == 'X':
            return create_symbol_image('X', bg_color='#FFE5E5', symbol_color='#E74C3C')
        elif symbol == 'O':
            return create_symbol_image('O', bg_color='#E5F3FF', symbol_color='#3498DB')
        else:
            return create_symbol_image('', bg_color='#F8F9FA')

# Enhanced winner checking with winning line detection
def check_winner(board):
    winning_combinations = [
        (0,1,2), (3,4,5), (6,7,8),  # Rows
        (0,3,6), (1,4,7), (2,5,8),  # Columns
        (0,4,8), (2,4,6)            # Diagonals
    ]
    
    for combo in winning_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] != '':
            return board[a], combo
    return None, None

# AI opponent with different difficulty levels
def get_ai_move(board, difficulty='Easy'):
    empty_positions = [i for i, cell in enumerate(board) if cell == '']
    
    if difficulty == 'Easy':
        # Random move
        import random
        return random.choice(empty_positions)
    
    elif difficulty == 'Hard':
        # Minimax algorithm
        def minimax(board, depth, is_maximizing):
            winner, _ = check_winner(board)
            if winner == 'O':
                return 10 - depth
            elif winner == 'X':
                return depth - 10
            elif '' not in board:
                return 0
            
            if is_maximizing:
                best_score = float('-inf')
                for i in empty_positions:
                    if board[i] == '':
                        board[i] = 'O'
                        score = minimax(board, depth + 1, False)
                        board[i] = ''
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in empty_positions:
                    if board[i] == '':
                        board[i] = 'X'
                        score = minimax(board, depth + 1, True)
                        board[i] = ''
                        best_score = min(score, best_score)
                return best_score
        
        best_move = None
        best_score = float('-inf')
        
        for i in empty_positions:
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                best_move = i
        
        return best_move
    
    return empty_positions[0] if empty_positions else None

# Game statistics and history
def update_game_stats(winner):
    st.session_state.stats['total_games'] += 1
    if winner:
        st.session_state.stats[winner] += 1
    else:
        st.session_state.stats['draws'] += 1
    
    # Add to game history
    game_duration = (datetime.now() - st.session_state.game_start_time).seconds
    st.session_state.game_history.append({
        'game_number': st.session_state.stats['total_games'],
        'winner': winner or 'Draw',
        'moves': st.session_state.move_count,
        'duration': game_duration,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Reset game function
def reset_game():
    st.session_state.board = [''] * 9
    st.session_state.turn = 'X'
    st.session_state.winner = None
    st.session_state.move_count = 0
    st.session_state.game_start_time = datetime.now()

# Main game interface
def main():
    initialize_game_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎮 Tic-Tac-Toe Master</h1>', unsafe_allow_html=True)
    
    # Sidebar for game settings
    with st.sidebar:
        st.header("⚙️ Game Settings")
        
        # Game mode selection
        game_mode = st.selectbox(
            "Select Game Mode",
            ["Human vs Human", "Human vs AI (Easy)", "Human vs AI (Hard)"],
            index=0,
            key="game_mode_select"
        )
        
        # Update game mode if changed
        if game_mode != st.session_state.difficulty:
            st.session_state.difficulty = game_mode
            # Reset game when mode changes
            reset_game()
            if 'game_ended' in st.session_state:
                del st.session_state.game_ended
            st.rerun()
        
        # Display game mode info
        st.info(f"🎮 Mode: {st.session_state.difficulty}")
        
        # Display statistics
        st.header("📊 Game Statistics")
        st.metric("Total Games", st.session_state.stats['total_games'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("X Wins", st.session_state.stats['X'], 
                     delta=f"{st.session_state.stats['X']}/{st.session_state.stats['total_games'] or 1:.1%}")
        with col2:
            st.metric("O Wins", st.session_state.stats['O'], 
                     delta=f"{st.session_state.stats['O']}/{st.session_state.stats['total_games'] or 1:.1%}")
        
        st.metric("Draws", st.session_state.stats['draws'])
        
        # Game history
        if st.session_state.game_history:
            st.header("📜 Recent Games")
            for game in st.session_state.game_history[-3:]:  # Show last 3 games
                st.text(f"Game {game['game_number']}: {game['winner']} ({game['moves']} moves)")
        
        # Clear statistics button
        if st.button("🗑️ Clear Statistics"):
            st.session_state.stats = {'X': 0, 'O': 0, 'draws': 0, 'total_games': 0}
            st.session_state.game_history = []
            st.rerun()
    
    # Game status display
    current_game_time = (datetime.now() - st.session_state.game_start_time).seconds
    
    # Game board container
    with st.container():
        st.markdown('<div class="game-board">', unsafe_allow_html=True)
        
        # Display current game info
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.winner:
                st.markdown(
                    f'<div class="winner-announcement">🎉 {st.session_state.winner} Wins! 🎉</div>',
                    unsafe_allow_html=True
                )
                # Update stats when game ends
                if 'game_ended' not in st.session_state:
                    update_game_stats(st.session_state.winner)
                    st.session_state.game_ended = True
                    
            elif '' not in st.session_state.board:
                st.markdown(
                    '<div class="draw-announcement">🤝 It\'s a Draw! 🤝</div>',
                    unsafe_allow_html=True
                )
                # Update stats for draw
                if 'game_ended' not in st.session_state:
                    update_game_stats(None)
                    st.session_state.game_ended = True
            else:
                st.markdown(
                    f'<div class="current-turn">Current Turn: {st.session_state.turn} | Move: {st.session_state.move_count} | Time: {current_game_time}s</div>',
                    unsafe_allow_html=True
                )
        
        # Game board
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                img = get_image(st.session_state.board[idx])
                
                # Button for making moves
                if cols[col].button("", key=f"btn_{idx}"):
                    if st.session_state.board[idx] == '' and st.session_state.winner is None:
                        # Make player move
                        st.session_state.board[idx] = st.session_state.turn
                        st.session_state.move_count += 1
                        
                        # Check for winner
                        winner, winning_combo = check_winner(st.session_state.board)
                        st.session_state.winner = winner
                        
                        # If no winner and it's AI turn
                        if not winner and "AI" in st.session_state.difficulty:
                            if st.session_state.turn == 'X':  # Human plays X, AI plays O
                                st.session_state.turn = 'O'
                                
                                # AI makes move after a short delay simulation
                                if '' in st.session_state.board:
                                    ai_difficulty = 'Easy' if 'Easy' in st.session_state.difficulty else 'Hard'
                                    ai_move = get_ai_move(st.session_state.board, ai_difficulty)
                                    
                                    if ai_move is not None:
                                        st.session_state.board[ai_move] = 'O'
                                        st.session_state.move_count += 1
                                        
                                        # Check for winner after AI move
                                        winner, winning_combo = check_winner(st.session_state.board)
                                        st.session_state.winner = winner
                                        
                                        if not winner:
                                            st.session_state.turn = 'X'
                        else:
                            # Human vs Human mode
                            if not winner:
                                st.session_state.turn = 'O' if st.session_state.turn == 'X' else 'X'
                        
                        st.rerun()
                
                # Display the current state of the cell
                cols[col].image(img, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Game controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 New Game", use_container_width=True):
            reset_game()
            if 'game_ended' in st.session_state:
                del st.session_state.game_ended
            st.rerun()
    
    # Instructions
    with st.expander("📖 How to Play"):
        st.write("""
        **Objective:** Get three of your symbols (X or O) in a row, column, or diagonal.
        
        **Game Modes:**
        - **Human vs Human:** Take turns with a friend
        - **Human vs AI (Easy):** Play against a random AI
        - **Human vs AI (Hard):** Challenge yourself against an unbeatable AI
        
        **Tips:**
        - Control the center square when possible
        - Block your opponent's winning moves
        - Create multiple winning opportunities
        
        **Statistics:** Track your wins, losses, and game history in the sidebar!
        """)

if __name__ == "__main__":
    main()