
# 🎮 Maze Escape: AI vs Player Showdown

Welcome to **Maze Escape**, a thrilling game where you, the player, must outwit an intelligent AI-controlled monster inside a dynamic maze. The maze is initially generated using **Prim's Algorithm**, then enhanced with multiple paths to make every escape route uncertain, unpredictable, and challenging!

## 🧠 Game Mechanics

### 🧩 Maze Generation
- The maze starts with **Prim’s Algorithm**, producing a perfect maze (no loops).
- To increase unpredictability and offer more replayability, **extra paths** are added, allowing for multiple potential escape routes.

---

## 👹 Monster AI & FSM Behavior

The monster in the maze is powered by an AI system that uses a **Finite State Machine (FSM)** combined with **Breadth-First Search (BFS)** to track the player.

### 📏 Distance Tracking
- The monster **constantly calculates the distance** between itself and the player using **BFS**.
- Based on the distance, it switches between different **behavioral states** with distinct strategies and movement speeds.

### 🚦 FSM States Overview

| State   | Distance Range       | Behavior                                                                 |
|---------|----------------------|--------------------------------------------------------------------------|
| **Idle**   | `> 20 cells`          | Monster wanders randomly throughout the maze, appearing unaware of the player. |
| **Alert**  | `> 10 and ≤ 20` cells | Monster becomes cautious and increases search efficiency and speed.     |
| **Chase**  | `> 5 and ≤ 10` cells  | Monster locks onto player’s direction and begins actively hunting.      |
| **Frenzy** | `≤ 5 cells`           | Monster goes berserk, using full speed and aggression to corner and capture the player. |

---

## 🏃‍♂️ Player vs Monster

The player must navigate the maze and avoid detection while seeking an escape route. As the monster transitions through its states, the game becomes increasingly intense:

- **Chase Mode:** The monster predicts your movement based on previous paths and closes in with sharp turns.
- **Frenzy Mode:** The monster no longer hesitates — it becomes extremely fast and accurate, using direct BFS paths and aggressive corner-cutting to capture you.


## 🛠️ Built With

- **Python and Pygame** 
- **Custom AI** and **FSM logic**
- **Prim’s Algorithm** for maze generation
- **Breadth-First Search (BFS)** for pathfinding

---

## 🚀 Future Improvements

- Add power-ups (e.g., invisibility, freeze time)
- Multiplayer mode
- Smarter player-tracking using learning-based AI
- Difficulty scaling and customizable monsters

---

