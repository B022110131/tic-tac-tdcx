# 🎮 Tic-Tac-Toe Master

An enhanced Streamlit-based Tic-Tac-Toe game with AI opponents, statistics tracking, and a modern user interface.

![Tic-Tac-Toe Master](https://img.shields.io/badge/Game-Tic--Tac--Toe-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=for-the-badge)

## 🌟 Features

### 🎯 Multiple Game Modes
- **Human vs Human**: Classic two-player mode
- **Human vs AI (Easy)**: Play against a random AI opponent
- **Human vs AI (Hard)**: Challenge yourself against an unbeatable AI using the minimax algorithm

### 🎨 Modern UI Design
- Beautiful gradient backgrounds and animations
- Responsive button hover effects
- Color-coded symbols (X in red, O in blue)
- Smooth transitions and pulse animations for winners
- Mobile-friendly responsive design

### 📊 Advanced Statistics
- Track total games played
- Win/loss statistics for both X and O
- Draw count and win percentages
- Game history with move count and duration
- Session-based statistics persistence

### 🖼️ Custom Image Support
- Use your own custom PNG images for X, O, and empty cells
- Automatic fallback to generated images if custom files aren't found
- Optimized image caching for better performance

### ⚡ Smart AI Opponent
- **Easy Mode**: Random move selection for casual play
- **Hard Mode**: Minimax algorithm implementation - truly unbeatable!
- Instant AI responses with proper turn management

## 🚀 Installation

1. **Clone or download** this repository
2. **Install required packages**:
   ```bash
   pip install streamlit pillow
   ```

## 📁 File Structure

```
tic-tac-toe/
├── app.py                # Main game file
├── images/               # Custom images folder (optional)
│   ├── empty.png         # Empty cell image
│   ├── x.png             # X symbol image
│   └── o.png             # O symbol image
└── README.md             # This file
```

## 🎮 How to Run

1. **Navigate to the game directory**:
   ```bash
   cd tic-tac-toe
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** and go to `http://localhost:8501`

## 🎲 How to Play

### Basic Rules
- Get three of your symbols (X or O) in a row, column, or diagonal to win
- Players alternate turns
- The game ends when someone wins or all cells are filled (draw)

### Game Controls
- **Click any empty cell** to make your move
- **Select game mode** from the sidebar dropdown
- **View statistics** in the sidebar panel
- **Click "New Game"** to reset and start over
- **Clear Statistics** to reset all tracked data

### Strategy Tips
- 🎯 Control the center square when possible
- 🛡️ Block your opponent's winning moves
- ⚔️ Create multiple winning opportunities
- 🧠 In Hard AI mode, try to force draws - winning is nearly impossible!

## 🖼️ Custom Images Setup

To use your own images:

1. **Create an `images` folder** in the same directory as `app.py`
2. **Add your PNG files**:
   - `empty.png` - Empty cell background
   - `x.png` - X symbol image
   - `o.png` - O symbol image
3. **Recommended image size**: 100x100 pixels or larger
4. **Supported formats**: PNG files work best

If custom images aren't found, the game automatically generates styled symbols.

## 🛠️ Technical Features

### Dependencies
- **Streamlit**: Web app framework
- **Pillow (PIL)**: Image processing
- **Built-in Python libraries**: datetime, json, io, base64

### AI Implementation
- **Minimax Algorithm**: Perfect play AI that never loses
- **Recursive evaluation**: Looks ahead to all possible game outcomes
- **Optimal move selection**: Chooses the best possible move every time

### Performance Optimizations
- **Image caching**: Custom images cached for faster loading
- **Efficient state management**: Minimal re-renders
- **Memory-friendly**: No external storage dependencies

## 📈 Statistics Tracking

The game tracks comprehensive statistics including:
- **Win/Loss Records**: Separate counts for X and O
- **Win Percentages**: Calculated automatically
- **Game History**: Last few games with details
- **Move Counter**: Track game length
- **Timer**: Game duration tracking
- **Total Games**: Overall session statistics

## 🎨 Customization

### Styling
The game uses custom CSS for styling. You can modify colors, animations, and layout by editing the CSS in the `st.markdown()` sections.

### Game Logic
- Modify AI difficulty in the `get_ai_move()` function
- Adjust winning conditions in `check_winner()`
- Customize statistics in `update_game_stats()`

## 🐛 Troubleshooting

### Common Issues

**Custom images not loading?**
- Check that the `images` folder is in the same directory as `app.py`
- Ensure PNG files are named exactly: `empty.png`, `x.png`, `o.png`
- Verify image files aren't corrupted

**Game not responding?**
- Refresh the browser page
- Check the Streamlit terminal for error messages
- Ensure all dependencies are installed

**Statistics not saving?**
- Statistics are session-based and reset when you close the browser
- This is by design for privacy and simplicity

## 🤝 Contributing

Feel free to fork this project and submit improvements! Some ideas:
- Sound effects for moves and wins
- Online multiplayer support
- More AI difficulty levels
- Tournament mode
- Theme customization

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI implementation using classic minimax algorithm
- Inspired by the timeless game of Tic-Tac-Toe

---

**Enjoy playing Tic-Tac-Toe Master!** 🎮✨

*Can you beat the Hard AI? Give it a try and see!*
