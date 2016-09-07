import random

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''


        self.x = maze_dim - 1
        self.y = 0
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.dimx = maze_dim
        self.dimy = maze_dim
        self.start_pos = [self.dimx-1,0]
        self.location = self.start_pos
        self.moves = 0
        self.run = 0
        self.heuristic = [[0 for row in range(0,self.maze_dim)] for col in range(0,self.maze_dim)]
        self.val_grid = [[0 for row in range(0,self.maze_dim)] for col in range(0,self.maze_dim)]
        self.count_grid = [[0 for row in range(1,self.maze_dim +1)] for col in range(1,self.maze_dim +1)]
        self.action_grid = [[0 for row in range(1,self.maze_dim +1)] for col in range(1,self.maze_dim +1)]
        self.arrow_grid = [[0 for row in range(1,self.maze_dim +1)] for col in range(1,self.maze_dim +1)]
        self.goal =[self.maze_dim/2 - 1, self.maze_dim/2]
        x,y = self.location
        self.unique = 0
        self.found_goal = 0

    # Return to start position at the end of round 1.
    def reset(self):
        self.x = self.maze_dim - 1
        self.y = 0
        self.heading = 'up'
        print self.count_grid
        print self.val_grid
        print self.action_grid
        print "Reset!"
        return ('Reset','Reset')

    # Marks whether each cell has been visited or not.
    def count_cell(self):
        x,y = self.location
        if self.count_grid[x][y]  == 0:
            self.count_grid[x][y] = 1
            self.unique += 1 # Count how many unique cells visited
        print 'Unique Cells Visited: {}.'.format(self.unique)
        return self.unique

    # Maps the maze with a value for each cell
    def cellValue(self, sensors):
        x,y = self.location
        self.sensors = sensors
        headings = ['left','up','right','down']
        dir_vals = [8, 1, 2, 4]
        if self.val_grid[x][y] == 0:
            for i in range(len(headings)):
                if self.heading == headings[i]:
                    self.val_grid[x][y] += dir_vals[(i + 2) % 4]
                    if sensors[0] > 0:
                        self.val_grid[x][y] += dir_vals[i-1]
                    if sensors[1] > 0:
                        self.val_grid[x][y] += dir_vals[i]
                    if sensors[2] > 0:
                        self.val_grid[x][y] += dir_vals[(i+1)%4]
        self.val_grid[self.maze_dim-1][0]=1

    # Build the heuristic
    def makeHeuristic(self):
        z = -1
        delta = [[-1,0],[0,1],[1,0],[0,-1]]
        possible = ['up','right','down','left']
        opened = []
        self.goal = [self.maze_dim/2 - 1, self.maze_dim/2]

        x = self.goal[0]
        y = self.goal[1]
        location = (x,y)
        h = 1
        opened.append((location, h))
        opened.append(((x+delta[2][0],y+delta[2][1]),h))
        opened.append(((x+delta[3][0],y+delta[3][1]),h))
        opened.append(((x+delta[2][0],y+delta[3][1]),h))
        self.updateHeuristic((x+delta[2][0],y+delta[2][1]), h)
        self.updateHeuristic((x+delta[3][0],y+delta[3][1]), h)
        self.updateHeuristic((x+delta[2][0],y+delta[3][1]), h)
        self.updateHeuristic(location, h)

        while self.heuristic[self.maze_dim -1][0] == 0 and len(opened) != 0:

            location , h = opened.pop(0)
            possible_actions = self.allowedActions(location)

            if 'up' in possible_actions and self.count_grid[location[0]][location[1]] != 0:
                x2 = location[0] + delta[0][0]
                y2 = location[1] + delta[0][1]
                new_location = x2, y2
                if self.heuristic[x2][y2] == 0 and self.count_grid[location[0]][location[1]] != 0:
                    opened.append((new_location,h +1))
                    self.updateHeuristic(new_location, h+1)
            if 'right' in possible_actions:
                x2 = location[0] + delta[1][0]
                y2 = location[1] + delta[1][1]
                new_location = x2, y2
                if self.heuristic[x2][y2] == 0 and self.count_grid[location[0]][location[1]] != 0:
                    opened.append((new_location,h +1))
                    self.updateHeuristic(new_location, h+1)
            if 'down' in possible_actions:
                x2 = location[0] + delta[2][0]
                y2 = location[1] + delta[2][1]
                new_location = x2, y2
                if self.heuristic[x2][y2] == 0 and self.count_grid[location[0]][location[1]] != 0:
                    opened.append((new_location,h +1))
                    self.updateHeuristic(new_location, h+1)
            if 'left' in possible_actions:
                x2 = location[0] + delta[3][0]
                y2 = location[1] + delta[3][1]
                new_location = x2, y2
                if self.heuristic[x2][y2] == 0:
                    opened.append((new_location,h +1))
                    self.updateHeuristic(new_location, h+1)

    # Update values in heuristic grid.
    def updateHeuristic(self,location,h):
            x,y = location
            self.heuristic[x][y] = h
            #print "heuristic: {}".format(self.heuristic)
            return self.heuristic

    # Identify possible actions in each cell.
    def allowedActions(self, location):
        x,y = location
        allowed_actions = []
        vals = [[1,3,5,7,9,11,13,15],[2,3,6,7,10,11,14,15],
        [4,5,6,7,12,13,14,15],[8,9,10,11,12,13,14,15]]
        possible = ['up','right','down','left']
        for i in range(len(vals)):
            if self.val_grid[x][y] in vals[0]:
                allowed_actions.extend([possible[0]])
            if self.val_grid[x][y] in vals[1]:
                allowed_actions.extend([possible[1]])
            if self.val_grid[x][y] in vals[2]:
                allowed_actions.extend([possible[2]])
            if self.val_grid[x][y] in vals[3]:
                allowed_actions.extend([possible[3]])
            return allowed_actions

    # Shows the optimal move from each position.
    def actionGrid(self):
        vals = [[1,3,5,7,9,11,13,15],[2,3,6,7,10,11,14,15],
        [4,5,6,7,12,13,14,15],[8,9,10,11,12,13,14,15]]
        possible = ['up','right','down','left']
        delta = [[-1,0],[0,1],[1,0],[0,-1]]
        for i in range(len(self.heuristic)):
            for j in range(len(self.heuristic[0])):
                for k in range(len(vals)):
                    if self.val_grid[i][j] in vals[k]:
                        if self.heuristic[i + delta[k][0]][j + delta[k][1]] == self.heuristic[i][j] - 1:
                            self.action_grid[i][j] = possible[k]
        self.arrowGrid()

    # Replaces the strings in action_grid with arrows.
    def arrowGrid(self):
        possible = ['up','right','down','left']
        arrows = ['^','>','v','<']
        for i in range(len(self.action_grid)):
            for j in range(len(self.action_grid[0])):
                for k in range(len(possible)):
                    if self.action_grid[i][j] == possible[k]:
                        self.arrow_grid[i][j] = arrows[k]
        print self.arrow_grid


    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the self.sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing self.sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        countererclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        self.cellValue(sensors)
        self.count_cell()

        goal = [self.maze_dim/2 - 1, self.maze_dim/2]
        if self.x in goal and self.y in goal:
            self.found_goal += 1 #Need to know that the goal has been reached in order to reset.
            if self.found_goal == 1:
                print '##### You have reached the goal!!! Goal Location: {},{}'.format(self.x,self.y)
        if self.run == 0:
            if self.found_goal != 0:
                if self.unique >= ((self.maze_dim**2)) or self.moves == 950:
                    print self.val_grid
                    self.makeHeuristic()
                    print "Heuristic", self.heuristic
                    self.actionGrid()
                    self.reset()
                    self.run += 1
                    return ('Reset', 'Reset')

        moves = ['left','forward','right']
        self.possible_moves = []
        self.sensors = sensors
        for i in range(len(self.sensors)):
            if self.sensors[i] > 0: # A value of zero means there is a wall there.
                self.possible_moves.extend([moves[i]])
        if self.possible_moves == []: #No possible moves means the robot is in a dead end
            rotation = +90
            movement = 0

        moves_up = []
        moves_down = []
        moves_left = []
        moves_right = []
        actions = []
        if self.run == 0:
            if self.heading == 'up':
                if 'right' in self.possible_moves:
                    moves_right.extend(range(1,self.sensors[2]+1 ))
                if 'forward' in self.possible_moves:
                    moves_up.extend(range(1,self.sensors[1] +1))
                if 'left' in self.possible_moves:
                    moves_left.extend(range(1,self.sensors[0] +1))
            elif self.heading == 'right':
                if 'right' in self.possible_moves:
                    moves_down.extend(range(1,self.sensors[2] +1))
                if 'forward' in self.possible_moves:
                    moves_right.extend(range(1,self.sensors[1] +1))
                if 'left' in self.possible_moves:
                    moves_up.extend(range(1,self.sensors[0] +1))
            elif self.heading == 'down':
                if 'right' in self.possible_moves:
                    moves_left.extend(range(1,self.sensors[2] +1))
                if 'forward' in self.possible_moves:
                    moves_down.extend(range(0,self.sensors[1] +1))
                if 'left' in self.possible_moves:
                    moves_right.extend(range(1,self.sensors[0] +1))
            elif self.heading == 'left':
                if 'right' in self.possible_moves:
                    moves_up.extend(range(1,self.sensors[2] +1))
                if 'forward' in self.possible_moves:
                    moves_left.extend(range(1,self.sensors[1] +1))
                if 'left' in self.possible_moves:
                    moves_down.extend(range(1,self.sensors[0] +1))

            if 1 in moves_up:
                if self.count_grid[self.x-1][self.y] != 1:
                    actions.extend([1])
            if 2 in moves_up:
                if self.count_grid[self.x-2][self.y] != 1:
                    actions.extend([11])
            if 3 in moves_up:
                if self.count_grid[self.x-3][self.y] != 1:
                    actions.extend([101])
            if 1 in moves_right:
                if self.count_grid[self.x][self.y +1] != 1:
                    actions.extend([2])
            if 2 in moves_right:
                if self.count_grid[self.x][self.y +2] != 1:
                    actions.extend([12])
            if 3 in moves_right:
                if self.count_grid[self.x][self.y +3] != 1:
                    actions.extend([102])
            if 1 in moves_down:
                if self.count_grid[self.x +1][self.y] != 1:
                    actions.extend([3])
            if 2 in moves_down:
                if self.count_grid[self.x +2][self.y] != 1:
                    actions.extend([13])
            if 3 in moves_down:
                if self.count_grid[self.x +3][self.y] != 1:
                    actions.extend([103])
            if 1 in moves_left:
                if self.count_grid[self.x][self.y -1] != 1:
                    actions.extend([4])
            if 2 in moves_left:
                if self.count_grid[self.x][self.y -2] != 1:
                    actions.extend([14])
            if 3 in moves_left:
                if self.count_grid[self.x][self.y -3] != 1:
                    actions.extend([104])
            print actions

            if actions != []:
                action = random.choice(actions)
                print action
                possible_actions = [1,2,3,4,11,12,13,14,101,102,103,104]
                directions = ['up','right', 'down', 'left']

                for i in range(len(possible_actions)):
                    if possible_actions[i] == action:
                        movement = len(str(possible_actions[i]))
                        direction = directions[i%4]
                    if self.x in self.goal and self.y in self.goal:
                        movement = 1
                    if self.moves < 5:
                        movement = 1

                for i in range(len(directions)):
                    if self.heading == directions[i]:
                        if direction == directions[i]:
                            rotation = 0
                        elif direction == directions[i-1]:
                            rotation = -90
                        elif direction == directions[(i+1)%4]:
                            rotation = +90
            elif self.possible_moves != 0:
                rotations = [-90, 0, +90]
                possible_rotations = []
                for i in range(len(self.sensors)):
                    for j in range(len(self.possible_moves)):
                        if self.possible_moves[j] == moves[i]:
                            possible_rotations.append(rotations[i])
                            rotation = random.choice(possible_rotations)
                            print possible_rotations
                            movement = 1
            else:
                movement = 0
                rotation = +90
                self.isDeadEnd()

        if self.run == 1: #Instructions for movement in the second run
            directions = ['up','right', 'down', 'left']
            delta = [[-1,0],[0,1],[1,0],[0,-1]]
            action = self.action_grid[self.x][self.y]
            for i in range(len(directions)):
                if self.action_grid[self.x][self.y] == directions[i]:
                    if self.action_grid[self.x + delta[i][0]][self.y + delta[i][1]] == directions[i]:
                        if self.action_grid[self.x + (2 * delta[i][0])][self.y + (2 * delta[i][1])] == directions[i]:
                            movement = 3
                        else:
                            movement = 2
                    else:
                        movement = 1
                if self.heading == directions[i]:
                    if action == directions[i]:
                        rotation = 0
                    elif action == directions[i-1]:
                        rotation = -90
                    elif action == directions[(i+1)%4]:
                        rotation = +90


        heading = None
        if self.heading == 'up':
            if rotation == 0:
                heading = 'up'
                self.x -= movement
            elif rotation == -90:
                heading = 'left'
                self.y -= movement
            elif rotation == +90:
                heading = 'right'
                self.y += movement
        elif self.heading == 'right':
            if rotation == 0:
                heading = 'right'
                self.y += movement
            elif rotation == -90:
                heading = 'up'
                self.x -= movement
            elif rotation == +90:
                heading = 'down'
                self.x += movement
        elif self.heading == 'down':
            if rotation == 0:
                heading = 'down'
                self.x += movement
            elif rotation == -90:
                heading = 'right'
                self.y += movement
            elif rotation == +90:
                heading = 'left'
                self.y -= movement
        else:
            if rotation == 0:
                heading = 'left'
                self.y -= movement
            elif rotation == -90:
                heading = 'down'
                self.x += movement
            elif rotation == +90:
                heading = 'up'
                self.x -= movement

        self.heading = heading
        self.location = (self.x, self.y)
        self.moves += 1


        print 'Rotation: {}, Movement: {}, Location: {}, Heading: {}, Moves: {}'.format(rotation, movement, self.location, heading, self.moves)

        return rotation, movement







