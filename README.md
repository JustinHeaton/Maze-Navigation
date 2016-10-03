# Plotting and Navigating a Virtual Maze

## This is the capstone project for Udacity's Machine Learning Engineer Nanodegree

### Description

In this project I programmed a robotic mouse to both plot and navigate a virtual maze environment. Using algorithms and techniques from artificial intelligence for robotics, and shortest path finding algorithms for maze-solving, I was able to develop a model where the robot reads inputs from its sensors, maps out an unknown maze environment, and determines the shortest path to the goal.

### Install

This project requires **python 2.7** to be installed.

### Code

* **robot.py** - This file contains the script which passes instructions to the robot to plot and navigate the virtual maze environment.
* **maze.py** - This script contains the functions which build the maze environment to be navigated by the robot.
* **tester.py** - This is the script which will be run to initiate the robot’s movement through the maze and to test whether the model is successful in completing the project.
* **showmaze.py** - This script can be used to visualize the maze.

### Additional Files

* **test_maze_01.txt** - Contains the specifications for a 12 x 12 maze.
* **test_maze_02.txt** - Contains the specifications for a 14 x 14 maze.
* **test_maze_03.txt** - Contains the specifications for a 16 x 16 maze.
* **Report.pdf** - The report which describes the process that I went to in solving the problem and coding the solution.

### Run

In a terminal or command window, navigate to the top-level project directory Maze-Navigation/ (that contains this README) and run one of the following commands:
```
python tester.py test_maze_01.txt
python tester.py test_maze_02.txt
python tester.py test_maze_03.txt
```

