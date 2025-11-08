TIC TAC TOE

#### Description:

This project is a web-based classic Tic Tac Toe game.
The game features a Player vs.Computer mode with an accessible user interface that uses Harvard’s maroon and gold color scheme for a polished look.


>Includes: python, javascript, HTML, CSS, flask

The project allows players to:
1. Compete against the computer.
2. Keep track of scores for Player Wins, Computer Wins, and Ties on a dynamic scoreboard.
3. Reset the game board without resetting the scores.
4. Experience a responsive and visually appealing design.

---

#### Features:
- **Player vs. Computer Gameplay**: The user plays as "X," while the computer plays as "O." The computer is programmed with basic logic to block the user or take a winning move when possible.
- **Dynamic Scoreboard**: Displays the number of Player Wins, Computer Wins, and Ties.
- **Reset Functionality**: Resets the game board and clears the "Winner" message while keeping the scoreboard intact.
- **Harvard Theme**: A clean UI inspired by Harvard’s maroon and gold branding.
- **Responsive Design**: Optimized for different screen sizes and devices.

---

#### Technologies Used:
- **Python**: Backend logic using Flask.
- **HTML/CSS**: For creating the user interface, styled with a Harvard-inspired design.
- **JavaScript**: Handles user interactions, updates the game state dynamically, and manages the scoreboard in the frontend.
- **Flask**: A Python web framework for handling requests and managing game logic.

---

#### Design Choices:
- **Harvard Theme**: The maroon (`#A41034`) and gold (`#FFD700`) color scheme was chosen to provide an elegant look, aligning with Harvard’s branding.
- **Frontend-Managed Scores**: By storing scores in JavaScript, we ensured scores persist across games but reset upon page refresh.
- **Simple Computer Logic**: The computer prioritizes blocking the player and winning opportunities, creating a challenging yet fun gameplay experience.

---

#### How It Works:
1. **Start a New Game**: Upon loading the page, the player can begin a game against the computer.
2. **Make a Move**: Click on an empty cell to place "X." The computer responds as "O."
3. **View Results**: The winner or a tie is announced below the scoreboard.
4. **Reset Board**: Click "Reset Game" to clear the board and play again without losing the scoreboard’s data.
5. **Refresh Scores**: Refreshing the browser resets the scoreboard.

---

#### Challenges Faced:
- **Score Management**: For a long time, the score persisted even after the page was refreshed, not allowing a new score to ever take place.
- **Styling**: Achieving a professional look took multiple iterations for color, spacing, and typography.
- **Managing Turn Logic**: Preventing bugs such as overwriting moves or skipping turns by validating inputs thoroughly.
- **Game State Synchronization**: Ensuring the frontend and backend states stay in sync during rapid actions like resets or moves.

---

#### Future Enhancements:
- Add a "Player vs. Player" mode for multiplayer gameplay.
- Improve the computer’s logic to make it more competitive.
- Introduce animations and sound effects for a richer user experience.

---

#### Installation and Setup:
1. Clone the repository:

